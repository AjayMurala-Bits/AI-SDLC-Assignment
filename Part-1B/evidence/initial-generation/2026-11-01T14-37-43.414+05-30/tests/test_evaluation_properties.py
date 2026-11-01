import unittest

from movie_review_summarizer.evaluation.semantic import required_semantic_passes


class EvaluationPropertyTests(unittest.TestCase):
    def test_ceiling_rule(self):
        self.assertEqual(required_semantic_passes(15), 14)
        self.assertEqual(required_semantic_passes(1), 1)

