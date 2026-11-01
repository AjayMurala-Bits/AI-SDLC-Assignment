"""Application orchestration and typed observable failures."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from .provider import InvalidProviderOutput, ProviderError
from .schema import validate_result

MAX_INPUT_CHARACTERS = 20_000


class SummarizerProvider(Protocol):
    def summarize(self, review_text: str) -> dict[str, Any]: ...


def failure(error_type: str, message: str) -> dict[str, Any]:
    return {"error": {"type": error_type, "message": message}}


def read_review(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        raise ValueError("review file is missing or unreadable")
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        raise ValueError("review file is not valid UTF-8") from exc
    if len(text) > MAX_INPUT_CHARACTERS:
        raise ValueError("review input exceeds the 20,000-character limit")
    return text


def summarize_file(path: str | Path, provider: SummarizerProvider) -> dict[str, Any]:
    try:
        review_text = read_review(path)
    except ValueError as exc:
        message = str(exc)
        kind = "empty_input" if "empty" in message else "invalid_input"
        return failure(kind, message)
    if not review_text.strip():
        return failure("empty_input", "review input is empty")

    try:
        result = provider.summarize(review_text)
    except InvalidProviderOutput as exc:
        return failure("invalid_model_output", str(exc))
    except ProviderError as exc:
        return failure("model_failure", str(exc))
    errors = validate_result(result)
    if errors:
        return failure("invalid_model_output", "; ".join(errors))
    return result

