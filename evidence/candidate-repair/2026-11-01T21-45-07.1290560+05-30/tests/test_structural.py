import unittest

from movie_review_summarizer.evaluation.structural import evaluate_structure


class StructuralTests(unittest.TestCase):
    def test_invalid_extra_field_fails(self):
        result = {"summary": "x", "sentiment": "positive", "positive_aspects": [], "negative_aspects": [], "recommendation": "x", "extra": True}
        self.assertFalse(evaluate_structure(result)["passed"])

