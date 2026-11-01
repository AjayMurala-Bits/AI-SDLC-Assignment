"""Candidate semantic scorer with independently verifiable judge evidence.

This module is intentionally not wired into the live runner during the
experiment.  It preserves the existing rubric and thresholds while refusing
to convert an unverifiable judge allegation into PASS.
"""

from __future__ import annotations

import math
import re
from typing import Any

SCORER_VERSION = "semantic-integrity-v1"
_FIELD_PART = re.compile(r"^\.([A-Za-z_][A-Za-z0-9_]*)")
_INDEX_PART = re.compile(r"^\[([0-9]+)\]")


def _resolve_path(result: dict[str, Any], path: str) -> Any:
    if not isinstance(path, str) or not path:
        raise ValueError("evidence_path must be a non-empty JSON path")
    if path.startswith("application_result"):
        path = "$" + path[len("application_result") :]
    if not path.startswith("$"):
        raise ValueError("evidence_path must start with $")
    current: Any = result
    remainder = path[1:]
    while remainder:
        match = _FIELD_PART.match(remainder) or _INDEX_PART.match(remainder)
        if not match:
            raise ValueError(f"invalid evidence_path: {path}")
        key = match.group(1) if match.re is _FIELD_PART else None
        index = match.group(1) if match.re is _INDEX_PART else None
        if key is not None:
            if not isinstance(current, dict) or key not in current:
                raise ValueError(f"evidence_path does not exist: {path}")
            current = current[key]
        else:
            if not isinstance(current, list) or int(index) >= len(current):
                raise ValueError(f"evidence_path does not exist: {path}")
            current = current[int(index)]
        remainder = remainder[match.end() :]
    return current


def _span_occurs_at_path(result: dict[str, Any], path: str, span: str) -> bool:
    value = _resolve_path(result, path)
    if not isinstance(span, str) or not span:
        raise ValueError("evidence_span must be a non-empty exact quote")
    if isinstance(value, str):
        return span in value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return any(span in item for item in value)
    raise ValueError("evidence_path must identify a string or string-list field")


def _verify_allegations(
    allegations: list[Any], application_result: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    verified: list[dict[str, Any]] = []
    unverified: list[dict[str, Any]] = []
    integrity_errors: list[str] = []
    for number, allegation in enumerate(allegations):
        if not isinstance(allegation, dict):
            error = f"unsupported_claims[{number}] must be an object with claim, evidence_span and evidence_path"
            integrity_errors.append(error)
            unverified.append({"allegation": allegation, "reason": error})
            continue
        span = allegation.get("evidence_span")
        path = allegation.get("evidence_path")
        claim = allegation.get("claim")
        try:
            if not isinstance(claim, str) or not claim.strip():
                raise ValueError("claim must be a non-empty string")
            if not _span_occurs_at_path(application_result, path, span):
                raise ValueError("evidence_span does not occur at evidence_path")
        except ValueError as exc:
            error = f"unsupported_claims[{number}] evidence integrity error: {exc}"
            integrity_errors.append(error)
            unverified.append({"allegation": allegation, "reason": str(exc)})
        else:
            verified.append(allegation)
    return verified, unverified, integrity_errors


def score_semantic_with_integrity(
    judge_result: dict[str, Any],
    rubric: dict[str, Any],
    application_result: dict[str, Any],
) -> dict[str, Any]:
    """Score with unchanged thresholds and explicit judge-evidence integrity."""
    errors: list[str] = []
    dimensions = ("faithfulness", "coverage", "uncertainty_usefulness")
    scores: dict[str, int] = {}
    for name in dimensions:
        value = judge_result.get(name)
        if not isinstance(value, int) or not 0 <= value <= 4:
            errors.append(f"{name} must be an integer from 0 to 4")
        else:
            scores[name] = value
    allegations = judge_result.get("unsupported_claims")
    if not isinstance(allegations, list):
        errors.append("unsupported_claims must be an array")
        allegations = []
    verified, unverified, integrity_errors = _verify_allegations(allegations, application_result)
    errors.extend(integrity_errors)
    if verified:
        errors.append("verified unsupported claims are a mandatory grounding failure")
    if not errors:
        normalized = (0.40 * scores["faithfulness"] + 0.35 * scores["coverage"] + 0.25 * scores["uncertainty_usefulness"]) / 4
        passed = normalized >= 0.80 and scores["faithfulness"] >= 3 and scores["coverage"] >= 3
    else:
        normalized = 0.0
        passed = False
    return {
        "passed": passed,
        "scores": scores,
        "normalized_score": normalized,
        "unsupported_claims": allegations,
        "verified_unsupported_claims": verified,
        "unverified_judge_allegations": unverified,
        "evidence_integrity_errors": integrity_errors,
        "errors": errors,
        "rubric_version": rubric.get("version", "unspecified"),
        "scorer_version": SCORER_VERSION,
    }


def required_semantic_passes(n_semantic: int) -> int:
    return math.ceil(0.90 * n_semantic)
