import unittest

from movie_review_summarizer.provider import InvalidProviderOutput, sanitized_provider_diagnostic


class ProviderDiagnosticTests(unittest.TestCase):
    def test_authentication_classification(self):
        error = type("AuthenticationError", (Exception,), {"status_code": 401, "code": "invalid_api_key"})()
        self.assertEqual(sanitized_provider_diagnostic(error), {"category": "authentication", "status_code": 401, "error_code": "invalid_api_key"})

    def test_quota_precedes_rate_limit(self):
        error = type("RateLimitError", (Exception,), {"status_code": 429, "code": "insufficient_quota"})()
        self.assertEqual(sanitized_provider_diagnostic(error)["category"], "quota_billing")

    def test_rate_limit_classification(self):
        error = type("RateLimitError", (Exception,), {"status_code": 429, "code": "rate_limit_exceeded"})()
        self.assertEqual(sanitized_provider_diagnostic(error)["category"], "rate_limit")

    def test_timeout_and_connection_classification(self):
        timeout = type("APITimeoutError", (Exception,), {})()
        connection = type("APIConnectionError", (Exception,), {})()
        self.assertEqual(sanitized_provider_diagnostic(timeout)["category"], "timeout")
        self.assertEqual(sanitized_provider_diagnostic(connection)["category"], "connection")

    def test_malformed_response_classification(self):
        self.assertEqual(sanitized_provider_diagnostic(InvalidProviderOutput("bad json"))["category"], "malformed_response")

    def test_sensitive_message_is_not_recorded(self):
        error = type("AuthenticationError", (Exception,), {"status_code": 401, "code": "invalid_api_key"})()
        diagnostic = sanitized_provider_diagnostic(error)
        self.assertNotIn("message", diagnostic)
        self.assertNotIn("authorization", str(diagnostic).lower())
