"""Structural gate independent of semantic judging."""

from __future__ import annotations

from typing import Any

from ..schema import validate_result


def evaluate_structure(result: Any) -> dict[str, Any]:
    errors = validate_result(result)
    return {"passed": not errors, "errors": errors}

