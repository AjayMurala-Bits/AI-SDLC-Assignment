"""One local NEG-001 diagnostic that preserves raw and parsed response evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from movie_review_summarizer.provider import ProviderConfig, OllamaProvider, InvalidProviderOutput, ProviderError, sanitized_provider_diagnostic
from movie_review_summarizer.schema import success_schema, validate_result


def _run_id() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def _usage(response: Any) -> dict[str, int] | None:
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    values: dict[str, int] = {}
    for target, names in {
        "input_tokens": ("input_tokens", "prompt_tokens"),
        "output_tokens": ("output_tokens", "completion_tokens"),
        "total_tokens": ("total_tokens",),
    }.items():
        for name in names:
            value = getattr(usage, name, None)
            if isinstance(value, int) and value >= 0:
                values[target] = value
                break
    return values or None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path.cwd()
    dataset = json.loads((root / "evals" / "dataset.json").read_text(encoding="utf-8"))
    case = next(item for item in dataset["cases"] if item["id"] == "NEG-001")
    config = ProviderConfig.from_environment()
    if config.provider != "ollama" or config.model != "llama3.2:latest":
        raise RuntimeError("diagnostic requires Ollama llama3.2:latest configuration")
    provider = OllamaProvider(
        config,
        (root / "prompts" / "summarize.txt").read_text(encoding="utf-8"),
        (root / "prompts" / "judge.txt").read_text(encoding="utf-8"),
    )
    report: dict[str, Any] = {
        "run_id": _run_id(),
        "diagnostic_type": "single-application-request-raw-response",
        "case_id": "NEG-001",
        "mode": "local-ollama-diagnostic",
        "judge_calls": 0,
        "full_evaluation": False,
        "sanitized_configuration": config.sanitized(),
        "input_review": case["input_review"],
        "expected": case["expected"],
        "request_contract": {
            "endpoint": config.base_url,
            "operation": "chat.completions.create",
            "response_format": {"type": "json_object"},
            "max_tokens": config.max_output_tokens,
        },
        "schema": success_schema(),
        "raw_response_content": None,
        "parsed_json": None,
        "application_result": None,
        "schema_validation_errors": [],
        "token_usage": None,
        "provider_error": None,
    }
    try:
        response = provider._client_or_raise().chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": provider.summarize_prompt},
                {"role": "user", "content": case["input_review"]},
            ],
            max_tokens=config.max_output_tokens,
            response_format={"type": "json_object"},
        )
        report["token_usage"] = _usage(response)
        choices = getattr(response, "choices", []) or []
        message = getattr(choices[0], "message", None) if choices else None
        raw = getattr(message, "content", None)
        report["raw_response_content"] = raw if isinstance(raw, str) else None
        try:
            parsed = json.loads(raw)
            report["parsed_json"] = parsed
            errors = validate_result(parsed)
            report["schema_validation_errors"] = errors
            report["application_result"] = parsed if not errors else {"error": {"type": "invalid_model_output", "message": "; ".join(errors)}}
            report["status"] = "success" if not errors else "application_validation_failure"
        except (TypeError, json.JSONDecodeError) as exc:
            report["schema_validation_errors"] = ["malformed JSON: " + type(exc).__name__]
            report["application_result"] = {"error": {"type": "invalid_model_output", "message": "model returned invalid JSON"}}
            report["status"] = "malformed_json"
    except (InvalidProviderOutput, ProviderError) as exc:
        report["provider_error"] = sanitized_provider_diagnostic(exc)
        report["status"] = "provider_failure"
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": report["run_id"], "status": report["status"], "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
