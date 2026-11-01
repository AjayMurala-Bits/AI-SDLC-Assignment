import unittest

from movie_review_summarizer.provider import _capture_usage


class UsageCaptureTests(unittest.TestCase):
    def test_only_numeric_token_usage_is_captured(self):
        usage = type("Usage", (), {"input_tokens": 12, "output_tokens": 8, "total_tokens": 20, "secret": "not copied"})()
        response = type("Response", (), {"usage": usage})()
        telemetry = {}
        _capture_usage(response, telemetry)
        self.assertEqual(telemetry, {"input_tokens": 12, "output_tokens": 8, "total_tokens": 20})
