"""Schema and deterministic limit validation for application results."""

from __future__ import annotations

import re
from typing import Any

SUCCESS_KEYS = {
    "summary",
    "sentiment",
    "positive_aspects",
    "negative_aspects",
    "recommendation",
}
SENTIMENTS = {"positive", "negative", "mixed", "unclear"}
FAILURE_TYPES = {
    "invalid_input",
    "empty_input",
    "insufficient_evidence",
    "model_failure",
    "invalid_model_output",
    "evaluation_failure",
}


def word_count(value: str) -> int:
    return len(value.split())


def sentence_count(value: str) -> int:
    groups = re.findall(r"[^.!?]*[.!?]+", value)
    remainder = re.sub(r"[^.!?]*[.!?]+", "", value).strip()
    return len(groups) + (1 if remainder else 0)


def validate_result(result: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["result must be a JSON object"]

    if set(result) == {"error"}:
        error = result.get("error")
        if not isinstance(error, dict):
            return ["error must be an object"]
        if set(error) != {"type", "message"}:
            errors.append("failure error must contain exactly type and message")
        if error.get("type") not in FAILURE_TYPES:
            errors.append("failure type is not allowed")
        if not isinstance(error.get("message"), str) or not error.get("message", "").strip():
            errors.append("failure message must be a non-empty string")
        return errors

    if set(result) != SUCCESS_KEYS:
        errors.append("success result must contain exactly the five required fields")
        return errors

    summary = result.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("summary must be a non-empty string")
    elif word_count(summary) > 80 or sentence_count(summary) > 3:
        errors.append("summary exceeds the 80-word or 3-sentence limit")

    if result.get("sentiment") not in SENTIMENTS:
        errors.append("sentiment is invalid")

    for field in ("positive_aspects", "negative_aspects"):
        values = result.get(field)
        if not isinstance(values, list) or not 0 <= len(values) <= 5:
            errors.append(f"{field} must contain zero to five strings")
            continue
        for value in values:
            if not isinstance(value, str) or not value.strip() or word_count(value) > 12:
                errors.append(f"{field} contains an invalid aspect")

    recommendation = result.get("recommendation")
    if not isinstance(recommendation, str) or not recommendation.strip():
        errors.append("recommendation must be a non-empty string")
    elif word_count(recommendation) > 30:
        errors.append("recommendation exceeds the 30-word limit")
    return errors


def success_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["summary", "sentiment", "positive_aspects", "negative_aspects", "recommendation"],
        "properties": {
            "summary": {"type": "string"},
            "sentiment": {"type": "string", "enum": sorted(SENTIMENTS)},
            "positive_aspects": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
            "negative_aspects": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
            "recommendation": {"type": "string"},
        },
    }

