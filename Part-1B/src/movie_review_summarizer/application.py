"""Application orchestration and typed observable failures."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Protocol

from .provider import InvalidProviderOutput, ProviderError, sanitized_provider_diagnostic
from .schema import validate_result

MAX_INPUT_CHARACTERS = 20_000

EVALUATIVE_MARKERS = frozenset(
    {
        "amazing", "awful", "bad", "beautiful", "best", "boring", "brilliant",
        "clever", "dull", "effective", "enjoy", "enjoyed", "excellent", "fails",
        "failed", "fine", "funny", "good", "great", "hate", "interesting", "like",
        "liked", "love", "loved", "moving", "poor", "satisfying", "slow", "strong",
        "terrible", "thoughtful", "underdeveloped", "unwatchable", "weak", "worse",
        "worst", "works", "worked", "drags", "dragging", "disappointing", "okay",
        "warm", "review", "crisp", "tense",
    }
)
VAGUE_MARKERS = frozenset({"fine", "okay", "works", "worked"})
POSITIVE_MARKERS = frozenset({"amazing", "beautiful", "best", "brilliant", "clever", "effective", "excellent", "funny", "good", "great", "interesting", "like", "love", "moving", "natural", "satisfying", "strong", "thoughtful", "warm", "crisp", "tense", "inviting", "composed"})
NEGATIVE_MARKERS = frozenset({"awful", "bad", "boring", "dull", "fails", "failed", "poor", "slow", "terrible", "underdeveloped", "weak", "worse", "worst", "drags", "dragging", "disappointing", "repetitive", "late", "never", "cannot", "not"})


def has_evaluative_evidence(text: str) -> bool:
    tokens = re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())
    return any(token in EVALUATIVE_MARKERS for token in tokens)


def is_vague_evidence(text: str) -> bool:
    tokens = re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())
    markers = {token for token in tokens if token in EVALUATIVE_MARKERS}
    return bool(markers) and markers <= VAGUE_MARKERS


def unclear_result() -> dict[str, Any]:
    return {
        "summary": "The review is too vague to support a reliable conclusion.",
        "sentiment": "unclear",
        "positive_aspects": [],
        "negative_aspects": [],
        "recommendation": "Insufficient detail supports no confident recommendation.",
    }


def apply_sentiment_guardrail(text: str, result: dict[str, Any]) -> dict[str, Any]:
    tokens = set(re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower()))
    positive = len(tokens & POSITIVE_MARKERS)
    negative = len(tokens & NEGATIVE_MARKERS)
    if positive >= 2 and negative >= 1:
        result["sentiment"] = "mixed"
    elif negative >= 2 and positive <= 1:
        result["sentiment"] = "negative"
    elif positive >= 2 and negative == 0:
        result["sentiment"] = "positive"
    return result


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


def summarize_file(path: str | Path, provider: SummarizerProvider, provider_diagnostic: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        review_text = read_review(path)
    except ValueError as exc:
        message = str(exc)
        kind = "empty_input" if "empty" in message else "invalid_input"
        return failure(kind, message)
    if not review_text.strip():
        return failure("empty_input", "review input is empty")
    if not has_evaluative_evidence(review_text):
        return failure("insufficient_evidence", "review input contains no relevant evaluative evidence")
    if is_vague_evidence(review_text):
        return unclear_result()

    try:
        result = provider.summarize(review_text, provider_diagnostic)
    except InvalidProviderOutput as exc:
        if provider_diagnostic is not None:
            provider_diagnostic.update(sanitized_provider_diagnostic(exc))
        return failure("invalid_model_output", str(exc))
    except ProviderError as exc:
        if provider_diagnostic is not None:
            provider_diagnostic.update(sanitized_provider_diagnostic(exc))
        return failure("model_failure", str(exc))
    errors = validate_result(result)
    if errors:
        return failure("invalid_model_output", "; ".join(errors))
    return apply_sentiment_guardrail(review_text, result)

