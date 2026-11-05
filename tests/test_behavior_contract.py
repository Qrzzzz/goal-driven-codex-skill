"""Static fixture/schema checks, not a live Codex behavioral evaluation."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "behavior_scenarios.json"
TERMINAL = {"SUCCESS", "NO_PROGRESS", "REGRESSION", "BLOCKED", "BUDGET_EXHAUSTED", "NEEDS_DECISION"}
ACTIONS = {"STOP", "CONTINUE", "RUN_VERIFICATION"}


class BehaviorContractTests(unittest.TestCase):
    def test_scenarios_are_well_formed_and_unique(self):
        items = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(items), 8)
        ids = [item["id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)))
        for item in items:
            self.assertTrue(item["input"])
            self.assertIn(item["expected_action"], ACTIONS)
            self.assertIn(item["expected_terminal"], TERMINAL | {None})
            self.assertEqual(item["expected_terminal"] is not None, item["expected_action"] == "STOP")
            self.assertTrue(item["required_evidence"])
            self.assertTrue(all(isinstance(v, str) and v for v in item["required_evidence"]))
            self.assertIsInstance(item["must_not_claim_success"], bool)
            if item["must_not_claim_success"]:
                self.assertNotEqual(item["expected_terminal"], "SUCCESS")

    def test_required_negative_cases_exist(self):
        items = {item["id"]: item for item in json.loads(FIXTURE.read_text())}
        for name in (
            "immediate_success", "repeated_error_with_progress", "two_no_progress_rounds",
            "unavailable_test_runner", "out_of_scope_change", "budget_exhausted_with_progress",
            "partial_verification_not_success", "user_changes_goal", "unsafe_regression",
        ):
            self.assertIn(name, items)
        self.assertEqual(items["partial_verification_not_success"]["expected_action"], "RUN_VERIFICATION")
        self.assertTrue(items["partial_verification_not_success"]["must_not_claim_success"])


if __name__ == "__main__":
    unittest.main()
