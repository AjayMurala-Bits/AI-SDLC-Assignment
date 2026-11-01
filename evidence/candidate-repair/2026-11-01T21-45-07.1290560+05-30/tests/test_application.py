import tempfile
import unittest
from pathlib import Path

from movie_review_summarizer.application import summarize_file
from movie_review_summarizer.provider import ProviderError, sanitized_provider_diagnostic
from tests.mocks import FakeProvider


class ApplicationTests(unittest.TestCase):
    def test_offline_mock_is_one_call_and_successful(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.txt"
            path.write_text("A warm review.", encoding="utf-8")
            provider = FakeProvider()
            result = summarize_file(path, provider)
        self.assertNotIn("error", result)
        self.assertEqual(provider.calls, 1)

    def test_empty_input_does_not_call_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.txt"
            path.write_text("  ", encoding="utf-8")
            provider = FakeProvider()
            result = summarize_file(path, provider)
        self.assertEqual(result["error"]["type"], "empty_input")
        self.assertEqual(provider.calls, 0)

    def test_provider_failure_is_typed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.txt"
            path.write_text("A review.", encoding="utf-8")
            result = summarize_file(path, FakeProvider(error=ProviderError("offline failure")))
        self.assertEqual(result["error"]["type"], "model_failure")

    def test_provider_diagnostic_is_sanitized_and_separate_from_failure_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.txt"
            path.write_text("A review.", encoding="utf-8")
            diagnostic = {}
            result = summarize_file(path, FakeProvider(error=ProviderError("secret detail", {"category": "rate_limit", "status_code": 429, "error_code": "rate_limit_exceeded"})), diagnostic)
        self.assertEqual(result["error"].keys(), {"type", "message"})
        self.assertEqual(diagnostic, {"category": "rate_limit", "status_code": 429, "error_code": "rate_limit_exceeded"})

    def test_missing_file_remains_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.txt"
            result = summarize_file(path, FakeProvider())
        self.assertEqual(result["error"]["type"], "invalid_input")

    def test_non_review_text_returns_insufficient_evidence_without_provider_call(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "irrelevant.txt"
            path.write_text("The blue bicycle has two wheels and a bell.", encoding="utf-8")
            provider = FakeProvider()
            result = summarize_file(path, provider)
        self.assertEqual(result["error"]["type"], "insufficient_evidence")
        self.assertEqual(provider.calls, 0)

    def test_vague_evaluative_text_reaches_provider_for_unclear_result(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vague.txt"
            path.write_text("It was fine; some parts worked and some did not.", encoding="utf-8")
            unclear = {
                "summary": "The review is too vague to support a reliable conclusion.",
                "sentiment": "unclear",
                "positive_aspects": [],
                "negative_aspects": [],
                "recommendation": "Insufficient evidence supports no confident recommendation.",
            }
            provider = FakeProvider(result=unclear)
            result = summarize_file(path, provider)
        self.assertEqual(result["sentiment"], "unclear")
        self.assertEqual(provider.calls, 0)

