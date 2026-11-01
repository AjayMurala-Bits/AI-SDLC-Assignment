"""Offline-only provider mocks. These must never be used as live evidence."""

from __future__ import annotations

from typing import Any


class FakeProvider:
    def __init__(self, result: dict[str, Any] | None = None, error: Exception | None = None) -> None:
        self.result = result or {
            "summary": "A concise grounded summary.",
            "sentiment": "positive",
            "positive_aspects": ["Clear performances"],
            "negative_aspects": [],
            "recommendation": "Consider it if this style appeals to you.",
        }
        self.error = error
        self.calls = 0

    def summarize(self, review_text: str, telemetry: dict[str, Any] | None = None) -> dict[str, Any]:
        self.calls += 1
        if self.error:
            raise self.error
        return self.result

