"""Controlled NEG-001 A/B diagnostic for Ollama JSON modes."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from movie_review_summarizer.provider import OllamaProvider, ProviderConfig, sanitized_provider_diagnostic
from movie_review_summarizer.schema import success_schema, validate_result


def _run_id() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds").replace(":", "-")


def _usage(response: Any) -> dict[str, int] | None:
    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    result: dict[str, int] = {}
    for target, names in {
        "input_tokens": ("input_tokens", "prompt_tokens"),
        "output_tokens": ("output_tokens", "completion_tokens"),
        "total_tokens": ("total_tokens",),
    }.items():
        for name in names:
            value = getattr(usage, name, None)
            if isinstance(value, int) and value >= 0:
                result[target] = value
                break
    return result or None


def _run(mode: str, output: Path) -> None:
    root = Path.cwd()
    dataset = json.loads((root / "evals" / "dataset.json").read_text(encoding="utf-8"))
    case = next(item for item in dataset["cases"] if item["id"] == "NEG-001")
    config = ProviderConfig.from_environment()
    if config.provider != "ollama" or config.model != "llama3.2:latest":
        raise RuntimeError("A/B diagnostic requires Ollama llama3.2:latest")
    provider = OllamaProvider(
        config,
        (root / "prompts" / "summarize.txt").read_text(encoding="utf-8"),
        (root / "prompts" / "judge.txt").read_text(encoding="utf-8"),
    )
    schema = success_schema()
    response_format: dict[str, Any]
    if mode == "json_object":
        response_format = {"type": "json_object"}
    else:
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "movie_review_summary",
                "strict": True,
                "schema": schema,
            },
        }
    report: dict[str, Any] = {
        "run_id": _run_id(),
        "diagnostic_type": "neg-001-controlled-ab",
        "experiment": "A-baseline-json-object" if mode == "json_object" else "B-schema-enforcement",
        "case_id": "NEG-001",
        "judge_calls": 0,
        "full_evaluation": False,
        "sanitized_configuration": config.sanitized(),
        "input_review": case["input_review"],
        "expected_sentiment": case["expected"]["deterministic"]["sentiment"],
        "schema": schema,
        "request_configuration": {
            "endpoint": config.base_url,
            "operation": "chat.completions.create",
            "model": config.model,
            "max_tokens": config.max_output_tokens,
            "retries": config.retries,
            "response_format": response_format,
        },
        "raw_response_content": None,
        "parsed_json": None,
        "sentiment_value": None,
        "schema_validation_errors": [],
        "schema_valid": False,
        "sentiment_matches_expected": False,
        "token_usage": None,
        "compatibility_error": None,
    }
    try:
        response = provider._client_or_raise().chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": provider.summarize_prompt},
                {"role": "user", "content": case["input_review"]},
            ],
            max_tokens=config.max_output_tokens,
            response_format=response_format,
        )
        report["token_usage"] = _usage(response)
        choices = getattr(response, "choices", []) or []
        message = getattr(choices[0], "message", None) if choices else None
        raw = getattr(message, "content", None)
        report["raw_response_content"] = raw if isinstance(raw, str) else None
        try:
            parsed = json.loads(raw)
            report["parsed_json"] = parsed
            if isinstance(parsed, dict):
                report["sentiment_value"] = parsed.get("sentiment")
            errors = validate_result(parsed)
            report["schema_validation_errors"] = errors
            report["schema_valid"] = not errors
            report["sentiment_matches_expected"] = report["sentiment_value"] == report["expected_sentiment"]
            report["status"] = "pass" if report["schema_valid"] else "application_validation_failure"
        except (TypeError, json.JSONDecodeError) as exc:
            report["schema_validation_errors"] = ["malformed JSON: " + type(exc).__name__]
            report["status"] = "malformed_json"
    except Exception as exc:
        report["compatibility_error"] = {
            "exception_type": type(exc).__name__,
            "sanitized_diagnostic": sanitized_provider_diagnostic(exc),
        }
        report["status"] = "schema_request_compatibility_failure" if mode == "json_schema" else "provider_failure"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"experiment": report["experiment"], "status": report["status"], "output": str(output)}))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("json_object", "json_schema"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    _run(args.mode, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
