"""Rubric scoring and mandatory unsupported-claim gate."""

from __future__ import annotations

import math
from typing import Any


def score_semantic(judge_result: dict[str, Any], rubric: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    dimensions = ("faithfulness", "coverage", "uncertainty_usefulness")
    scores: dict[str, int] = {}
    for name in dimensions:
        value = judge_result.get(name)
        if not isinstance(value, int) or not 0 <= value <= 4:
            errors.append(f"{name} must be an integer from 0 to 4")
        else:
            scores[name] = value
    unsupported = judge_result.get("unsupported_claims")
    if not isinstance(unsupported, list):
        errors.append("unsupported_claims must be an array")
        unsupported = []
    if not errors:
        normalized = (0.40 * scores["faithfulness"] + 0.35 * scores["coverage"] + 0.25 * scores["uncertainty_usefulness"]) / 4
        passed = (
            normalized >= 0.80
            and scores["faithfulness"] >= 3
            and scores["coverage"] >= 3
            and len(unsupported) == 0
        )
    else:
        normalized = 0.0
        passed = False
    if unsupported:
        errors.append("unsupported claims are a mandatory grounding failure")
    return {
        "passed": passed and not errors,
        "scores": scores,
        "normalized_score": normalized,
        "unsupported_claims": unsupported,
        "errors": errors,
        "rubric_version": rubric.get("version", "unspecified"),
    }


def required_semantic_passes(n_semantic: int) -> int:
    return math.ceil(0.90 * n_semantic)

