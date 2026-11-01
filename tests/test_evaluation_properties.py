import unittest

from movie_review_summarizer.evaluation.semantic import required_semantic_passes
from movie_review_summarizer.evaluation.semantic_integrity import score_semantic_with_integrity


class EvaluationPropertyTests(unittest.TestCase):
    def test_ceiling_rule(self):
        self.assertEqual(required_semantic_passes(15), 14)
        self.assertEqual(required_semantic_passes(1), 1)

    def test_fabricated_allegation_is_integrity_error_and_not_pass(self):
        result = score_semantic_with_integrity(
            {"faithfulness": 4, "coverage": 4, "uncertainty_usefulness": 4,
             "unsupported_claims": [{"claim": "box-office success", "missing_evidence": "not present"}]},
            {"version": "rubric-v1"},
            {"summary": "A grounded summary.", "sentiment": "positive", "positive_aspects": [], "negative_aspects": [], "recommendation": "Consider it."},
        )
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["verified_unsupported_claims"]), 0)
        self.assertEqual(len(result["unverified_judge_allegations"]), 1)
        self.assertTrue(result["evidence_integrity_errors"])

    def test_grounded_allegation_is_verified_mandatory_failure(self):
        result = score_semantic_with_integrity(
            {"faithfulness": 4, "coverage": 4, "uncertainty_usefulness": 4,
             "unsupported_claims": [{"claim": "outside detail", "evidence_span": "outside detail", "evidence_path": "$.summary"}]},
            {"version": "rubric-v1"},
            {"summary": "The outside detail is unsupported.", "sentiment": "positive", "positive_aspects": [], "negative_aspects": [], "recommendation": "Consider it."},
        )
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["verified_unsupported_claims"]), 1)
        self.assertFalse(result["evidence_integrity_errors"])

    def test_complete_assertion_quote_can_be_verified_in_array_item(self):
        result = score_semantic_with_integrity(
            {"faithfulness": 4, "coverage": 4, "uncertainty_usefulness": 4,
             "unsupported_claims": [{"claim": "unsupported aspect", "evidence_span": "unsupported aspect", "evidence_path": "$.negative_aspects[0]"}]},
            {"version": "rubric-v1"},
            {"summary": "Grounded.", "sentiment": "negative", "positive_aspects": [], "negative_aspects": ["unsupported aspect"], "recommendation": "Skip it."},
        )
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["verified_unsupported_claims"]), 1)

