import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from movie_review_summarizer.evaluation.runner import run
from movie_review_summarizer.provider import ProviderConfig


class RunnerFixtureTests(unittest.TestCase):
    def test_live_fixture_conditions_are_deterministic_and_labeled(self):
        dataset = {
            "dataset_version": "fixture-test",
            "freeze_status": "approved",
            "cases": [
                {
                    "id": "MISS-TEST",
                    "category": "missing-file",
                    "class": "deterministic",
                    "input_review": None,
                    "input_fixture": {"type": "missing_file"},
                    "expected": {"outcome": "failure", "failure_type": "invalid_input", "deterministic": {}},
                },
                {
                    "id": "SVC-TEST",
                    "category": "model-service-failure",
                    "class": "service-failure",
                    "input_review": "controlled service fixture",
                    "input_fixture": None,
                    "expected": {"outcome": "failure", "failure_type": "model_failure", "deterministic": {"service_gate": "mandatory"}},
                },
                {
                    "id": "OUT-TEST",
                    "category": "malformed-model-output",
                    "class": "deterministic",
                    "input_review": "controlled output fixture",
                    "input_fixture": None,
                    "expected": {"outcome": "failure", "failure_type": "invalid_model_output", "deterministic": {}},
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "prompts").mkdir()
            (root / "prompts" / "summarize.txt").write_text("summary", encoding="utf-8")
            (root / "prompts" / "judge.txt").write_text("judge", encoding="utf-8")
            dataset_path = root / "dataset.json"
            dataset_path.write_text(json.dumps(dataset), encoding="utf-8")
            digest = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
            (root / "dataset.lock.json").write_text(json.dumps({"dataset_version": "fixture-test", "dataset_sha256": digest}), encoding="utf-8")
            with patch("movie_review_summarizer.evaluation.runner.ProviderConfig.from_environment", return_value=ProviderConfig(api_key="test", model="test")):
                report = run(dataset_path, root, "live")
        by_id = {case["case_id"]: case for case in report["cases"]}
        self.assertEqual(by_id["MISS-TEST"]["result"]["error"]["type"], "invalid_input")
        self.assertFalse(by_id["MISS-TEST"]["simulated"])
        self.assertEqual(by_id["SVC-TEST"]["result"]["error"]["type"], "model_failure")
        self.assertEqual(by_id["SVC-TEST"]["fixture_mode"], "simulated-service-failure")
        self.assertTrue(by_id["SVC-TEST"]["simulated"])
        self.assertEqual(by_id["OUT-TEST"]["result"]["error"]["type"], "invalid_model_output")
        self.assertEqual(by_id["OUT-TEST"]["fixture_mode"], "simulated-malformed-output")
        self.assertTrue(by_id["OUT-TEST"]["simulated"])
        self.assertEqual(report["overall"], "PASS")
