import unittest

from movie_review_summarizer.schema import validate_result


class OfflineCliContractTests(unittest.TestCase):
    def test_mocked_cli_contract_is_json_schema_checked(self):
        mocked_output = {"error": {"type": "insufficient_evidence", "message": "not enough review evidence"}}
        self.assertEqual(validate_result(mocked_output), [])

