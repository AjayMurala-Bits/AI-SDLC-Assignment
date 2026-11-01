"""Deterministic requirement and case-property gate."""

from __future__ import annotations

from typing import Any


def evaluate_properties(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    expected = case.get("expected", {})
    errors: list[str] = []
    expected_outcome = expected.get("outcome", "success")
    if expected_outcome == "failure":
        expected_type = expected.get("failure_type")
        actual_type = result.get("error", {}).get("type")
        if actual_type != expected_type:
            errors.append(f"expected failure type {expected_type}, got {actual_type}")
    else:
        if "error" in result:
            errors.append("expected success but received a failure")
        for field, value in expected.get("deterministic", {}).items():
            if field == "sentiment" and result.get("sentiment") != value:
                errors.append(f"expected sentiment {value}, got {result.get('sentiment')}")
            elif field == "must_not_contain":
                serialized = str(result).lower()
                for forbidden in value:
                    if str(forbidden).lower() in serialized:
                        errors.append(f"result contains prohibited text: {forbidden}")
            elif field == "max_aspects":
                if any(len(result.get(name, [])) > value for name in ("positive_aspects", "negative_aspects")):
                    errors.append("aspect list exceeds deterministic maximum")
    if case.get("class") == "service-failure" and result.get("error", {}).get("type") != "model_failure":
        errors.append("service-failure case did not remain a model_failure")
    return {"passed": not errors, "errors": errors}

