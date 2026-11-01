"""Offline/live evaluation orchestration and timestamped evidence output."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..application import failure, summarize_file
from ..provider import OllamaProvider, OpenAIProvider, ProviderConfig, ProviderError, sanitized_provider_diagnostic
from ..schema import validate_result
from .properties import evaluate_properties
from .semantic import required_semantic_passes, score_semantic
from .structural import evaluate_structure


def _timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _review_text(case: dict[str, Any], root: Path) -> str:
    if case.get("input_review") is not None:
        return str(case["input_review"])
    fixture = case.get("input_fixture", {})
    if fixture.get("type") == "missing_file":
        return ""
    if fixture.get("type") == "empty":
        return ""
    if fixture.get("type") == "oversized":
        return "x" * 20_001
    if fixture.get("type") == "invalid_utf8":
        return "\ufffd invalid encoding fixture"
    return str(fixture.get("text", ""))


def _verify_frozen_dataset(dataset_path: Path, dataset: dict[str, Any]) -> None:
    """Reject any approved dataset whose bytes differ from the approved lock."""
    if dataset.get("freeze_status") != "approved":
        return
    lock_path = dataset_path.with_name("dataset.lock.json")
    if not lock_path.exists():
        raise RuntimeError("approved dataset lock is missing; frozen dataset cannot be used")
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    actual_hash = _sha256(dataset_path)
    if lock.get("dataset_version") != dataset.get("dataset_version"):
        raise RuntimeError("approved dataset version does not match the dataset lock")
    if lock.get("dataset_sha256") != actual_hash:
        raise RuntimeError("approved dataset hash does not match the frozen dataset lock")


def _offline_result(case: dict[str, Any]) -> dict[str, Any]:
    expected = case.get("expected", {})
    if expected.get("outcome") == "failure":
        return failure(expected.get("failure_type", "evaluation_failure"), "offline fixture result")
    return expected["offline_output"]


def _offline_judge(case: dict[str, Any]) -> dict[str, Any]:
    return case["expected"].get("offline_judge", {
        "faithfulness": 4,
        "coverage": 4,
        "uncertainty_usefulness": 4,
        "unsupported_claims": [],
        "rationale": "offline fixture judge result",
    })


def run(dataset_path: Path, root: Path, mode: str) -> dict[str, Any]:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    _verify_frozen_dataset(dataset_path, dataset)
    if dataset.get("freeze_status") != "approved" and mode == "live":
        raise RuntimeError("dataset approval/freeze is pending; live mode is blocked")
    run_id = _timestamp()
    evidence_root = root / "evidence" / "evaluation-results" / run_id
    evidence_root.mkdir(parents=True, exist_ok=True)
    n_semantic = sum(case.get("class") == "semantic" for case in dataset["cases"])
    case_results: list[dict[str, Any]] = []
    provider = None
    if mode == "live":
        config = ProviderConfig.from_environment()
        adapter = OllamaProvider if config.provider == "ollama" else OpenAIProvider
        provider = adapter(
            config,
            (root / "prompts" / "summarize.txt").read_text(encoding="utf-8"),
            (root / "prompts" / "judge.txt").read_text(encoding="utf-8"),
        )
        sanitized_config = config.sanitized()
    else:
        sanitized_config = {
            "mode": "offline-mock",
            "live_api_calls": False,
            "generation_access_tested": False,
            "billing_tested": False,
            "retries": 0,
        }
    for case in dataset["cases"]:
        text = _review_text(case, root)
        fixture_mode = "offline-mock" if mode == "offline" else "input-fixture"
        simulated = mode == "offline"
        provider_diagnostic: dict[str, Any] = {}
        judge_diagnostic: dict[str, Any] = {}
        if mode == "offline":
            result = _offline_result(case)
        else:
            fixture = case.get("input_fixture", {})
            if case.get("class") == "service-failure":
                result = failure("model_failure", "simulated service failure fixture")
                fixture_mode = "simulated-service-failure"
                simulated = True
            elif case.get("category") == "malformed-model-output":
                result = failure("invalid_model_output", "simulated malformed model output fixture")
                fixture_mode = "simulated-malformed-output"
                simulated = True
            else:
                fixture_path = evidence_root / f"{case['id']}-input.txt"
                if fixture.get("type") == "missing_file":
                    # Deliberately do not create the path.
                    fixture_path = evidence_root / f"{case['id']}-missing.txt"
                elif fixture.get("type") == "invalid_utf8":
                    fixture_path.write_bytes(b"\xff\xfe invalid encoding fixture")
                else:
                    fixture_path.write_text(text, encoding="utf-8")
                result = summarize_file(fixture_path, provider, provider_diagnostic)
                if provider_diagnostic:
                    fixture_mode = "live-provider"
        structural = evaluate_structure(result)
        properties = evaluate_properties(case, result)
        semantic = None
        judge_result = None
        if case.get("class") == "semantic" and structural["passed"] and properties["passed"]:
            if mode == "offline":
                judge_result = _offline_judge(case)
                semantic = score_semantic(judge_result, case["expected"]["rubric"])
            else:
                try:
                    judge_result = provider.judge(text, result, case["expected"]["rubric"])
                    semantic = score_semantic(judge_result, case["expected"]["rubric"])
                except ProviderError as exc:
                    judge_diagnostic.update(sanitized_provider_diagnostic(exc))
                    semantic = {
                        "passed": False,
                        "scores": {},
                        "normalized_score": 0.0,
                        "unsupported_claims": [],
                        "errors": ["judge call failed"],
                        "rubric_version": case["expected"]["rubric"].get("version", "unspecified"),
                    }
        case_results.append({
            "run_id": run_id,
            "case_id": case["id"],
            "category": case["category"],
            "mode": mode,
            "result": result,
            "structural": structural,
            "properties": properties,
            "judge": judge_result,
            "semantic": semantic,
            "fixture_mode": fixture_mode,
            "simulated": simulated,
            "provider_error": provider_diagnostic or None,
            "judge_error": judge_diagnostic or None,
        })
    semantic_results = [item for item in case_results if item["semantic"] is not None]
    mandatory_failure = any(
        not item[gate]["passed"]
        for item in case_results
        for gate in ("structural", "properties")
    ) or any(not item["semantic"]["passed"] for item in semantic_results)
    required = required_semantic_passes(n_semantic)
    semantic_passes = sum(item["semantic"]["passed"] for item in semantic_results)
    overall = not mandatory_failure and semantic_passes >= required
    report = {
        "run_id": run_id,
        "mode": mode,
        "dataset_version": dataset["dataset_version"],
        "dataset_sha256": _sha256(dataset_path),
        "sanitized_configuration": sanitized_config,
        "n_semantic": n_semantic,
        "required_semantic_passes": required,
        "semantic_passes": semantic_passes,
        "mandatory_failure": mandatory_failure,
        "overall": "PASS" if overall else "FAIL",
        "cases": case_results,
    }
    (evidence_root / "run.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("offline", "live"), default="offline")
    parser.add_argument("--dataset", default="evals/dataset.json")
    args = parser.parse_args(argv)
    root = Path.cwd()
    try:
        report = run(root / args.dataset, root, args.mode)
    except (OSError, ValueError, ProviderError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "mode": args.mode}))
        return 1
    print(json.dumps({"run_id": report["run_id"], "mode": report["mode"], "overall": report["overall"]}))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

