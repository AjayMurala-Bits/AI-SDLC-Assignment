"""One-case live application diagnostic; never invokes the judge or full runner."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from movie_review_summarizer.provider import (
    InvalidProviderOutput,
    ProviderError,
    provider_from_environment,
    sanitized_provider_diagnostic,
)
from movie_review_summarizer.schema import validate_result


def _run_id() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--dataset", default="evals/dataset.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    dataset = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    case = next((item for item in dataset["cases"] if item["id"] == args.case_id), None)
    if case is None or case.get("id") != "POS-001":
        raise ValueError("diagnostic is restricted to POS-001")
    if case.get("class") != "semantic" or not case.get("input_review"):
        raise ValueError("POS-001 is not a valid semantic review case")

    config, provider = provider_from_environment(
        Path("prompts/summarize.txt").read_text(encoding="utf-8"),
        Path("prompts/judge.txt").read_text(encoding="utf-8"),
    )
    telemetry: dict[str, int] = {}
    report: dict[str, object] = {
        "run_id": _run_id(),
        "diagnostic_type": "single-application-request",
        "case_id": "POS-001",
        "mode": "live-diagnostic",
        "judge_calls": 0,
        "full_dataset_runner": False,
        "sanitized_configuration": config.sanitized(),
        "provider_error": None,
        "token_usage": None,
        "result": None,
        "schema_errors": [],
    }
    try:
        result = provider.summarize(case["input_review"], telemetry)
        report["result"] = result
        report["schema_errors"] = validate_result(result)
        report["status"] = "success" if not report["schema_errors"] else "invalid_model_output"
    except InvalidProviderOutput as exc:
        report["status"] = "invalid_model_output"
        report["result"] = {"error": {"type": "invalid_model_output", "message": str(exc)}}
        report["provider_error"] = sanitized_provider_diagnostic(exc)
    except ProviderError as exc:
        report["status"] = "model_failure"
        report["result"] = {"error": {"type": "model_failure", "message": str(exc)}}
        report["provider_error"] = sanitized_provider_diagnostic(exc)
    finally:
        report["token_usage"] = telemetry or None

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": report["run_id"], "status": report["status"], "output": str(output)}))
    return 0 if report["status"] in {"success", "invalid_model_output", "model_failure"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
