import tempfile
import unittest
from pathlib import Path

from movie_review_summarizer.application import summarize_file
from movie_review_summarizer.provider import ProviderError
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

