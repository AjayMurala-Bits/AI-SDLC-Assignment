import unittest

from movie_review_summarizer.schema import sentence_count, validate_result, word_count


class SchemaTests(unittest.TestCase):
    def test_valid_success_shape(self):
        result = {
            "summary": "Clear performances support a warm story.",
            "sentiment": "positive",
            "positive_aspects": ["Clear performances"],
            "negative_aspects": [],
            "recommendation": "Consider it for a warm story.",
        }
        self.assertEqual(validate_result(result), [])

    def test_word_and_sentence_rules_are_deterministic(self):
        self.assertEqual(word_count("one two three"), 3)
        self.assertEqual(sentence_count("One. Two!"), 2)

    def test_failure_shape(self):
        self.assertEqual(validate_result({"error": {"type": "empty_input", "message": "empty"}}), [])

