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
from ..provider import OpenAIProvider, ProviderConfig, ProviderError
from ..schema import validate_result
from .properties import evaluate_properties
from .semantic import required_semantic_passes, score_semantic
from .structural import evaluate_structure


def _timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _review_text(case: dict[str, Any], root: Path) -> str:
    if "input_review" in case:
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
        provider = OpenAIProvider(
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
        if mode == "offline":
            result = _offline_result(case)
        else:
            fixture_path = evidence_root / f"{case['id']}-input.txt"
            fixture_path.write_text(text, encoding="utf-8")
            result = summarize_file(fixture_path, provider)
        structural = evaluate_structure(result)
        properties = evaluate_properties(case, result)
        semantic = None
        judge_result = None
        if case.get("class") == "semantic" and structural["passed"] and properties["passed"]:
            judge_result = _offline_judge(case) if mode == "offline" else provider.judge(text, result, case["expected"]["rubric"])
            semantic = score_semantic(judge_result, case["expected"]["rubric"])
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

