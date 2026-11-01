"""Focused local Ollama application diagnostics; no judge or full runner."""

from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from movie_review_summarizer.application import summarize_file
from movie_review_summarizer.provider import OllamaProvider, ProviderConfig, sanitized_provider_diagnostic
from movie_review_summarizer.schema import validate_result


CASE_IDS = ("POS-001", "NEG-001", "MIX-001", "CON-001", "VAG-001", "IRR-001", "INJ-001", "WEAK-001")


def _run_id() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def _usage(response: Any) -> dict[str, int] | None:
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    result: dict[str, int] = {}
    for target, names in {"input_tokens": ("input_tokens", "prompt_tokens"), "output_tokens": ("output_tokens", "completion_tokens"), "total_tokens": ("total_tokens",)}.items():
        for name in names:
            value = getattr(usage, name, None)
            if isinstance(value, int) and value >= 0:
                result[target] = value
                break
    return result or None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path.cwd()
    dataset = json.loads((root / "evals" / "dataset.json").read_text(encoding="utf-8"))
    cases = {case["id"]: case for case in dataset["cases"]}
    config = ProviderConfig.from_environment()
    if config.provider != "ollama" or config.model != "llama3.2:latest":
        raise RuntimeError("focused diagnostics require Ollama llama3.2:latest")
    provider = OllamaProvider(config, (root / "prompts" / "summarize.txt").read_text(encoding="utf-8"), (root / "prompts" / "judge.txt").read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as directory:
        for case_id in CASE_IDS:
            case = cases[case_id]
            text = case.get("input_review") or case.get("input_fixture", {}).get("text", "")
            review_path = Path(directory) / f"{case_id}.txt"
            review_path.write_text(text, encoding="utf-8")
            telemetry: dict[str, Any] = {}
            item: dict[str, Any] = {"case_id": case_id, "category": case["category"], "expected": case["expected"], "result": None, "schema_errors": [], "token_usage": None, "provider_error": None}
            try:
                result = summarize_file(review_path, provider, telemetry)
                item["result"] = result
                item["schema_errors"] = validate_result(result)
                item["status"] = "pass" if not item["schema_errors"] else "application_validation_failure"
            except Exception as exc:
                item["result"] = {"error": {"type": "model_failure", "message": "diagnostic request failed"}}
                item["provider_error"] = sanitized_provider_diagnostic(exc)
                item["status"] = "provider_or_parse_failure"
            item["token_usage"] = telemetry or None
            results.append(item)
    report = {"run_id": _run_id(), "diagnostic_type": "focused-application-diagnostics", "provider": config.sanitized(), "judge_calls": 0, "full_evaluation": False, "cases": results}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": report["run_id"], "output": str(output), "cases": len(results)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
