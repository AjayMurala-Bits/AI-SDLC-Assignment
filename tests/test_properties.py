import unittest

from movie_review_summarizer.evaluation.properties import evaluate_properties


class PropertyTests(unittest.TestCase):
    def test_expected_sentiment(self):
        case = {"class": "semantic", "expected": {"outcome": "success", "deterministic": {"sentiment": "mixed"}}}
        result = {"sentiment": "mixed"}
        self.assertTrue(evaluate_properties(case, result)["passed"])

    def test_expected_failure_type(self):
        case = {"class": "deterministic", "expected": {"outcome": "failure", "failure_type": "empty_input"}}
        result = {"error": {"type": "empty_input", "message": "empty"}}
        self.assertTrue(evaluate_properties(case, result)["passed"])

