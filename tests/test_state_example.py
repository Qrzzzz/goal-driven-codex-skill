"""Consistency checks for documentation data, not live agent behavior."""

import json
from pathlib import Path
import unittest

EXAMPLE = Path(__file__).resolve().parents[1] / "skill/references/session-state.example.json"


class StateExampleTests(unittest.TestCase):
    def test_example_can_be_resumed_without_resetting_ledger(self):
        state = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(state["schema_version"], 1)
        budget = state["budget"]
        for dimension, limit in budget["limits"].items():
            consumed, remaining = budget["consumed"][dimension], budget["remaining"][dimension]
            if limit is None:
                self.assertIsNone(remaining)
                continue
            self.assertGreaterEqual(consumed, 0)
            self.assertGreaterEqual(remaining, 0)
            self.assertEqual(consumed + remaining, limit, dimension)
        implementations = [a for a in state["attempts"] if a["kind"] == "implementation"]
        self.assertEqual(len(implementations), budget["consumed"]["iterations"])
        diagnostics = [a for a in state["attempts"] if a["kind"] == "diagnostic"]
        self.assertEqual(len(diagnostics), budget["consumed"]["validation_retries"])
        self.assertGreater(budget["consumed"]["iterations"], 0)
        self.assertGreater(budget["remaining"]["validation_retries"], 0)

    def test_example_has_original_and_current_evidence(self):
        state = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.assertTrue(state["goal"])
        self.assertTrue(state["allowed_paths"])
        self.assertTrue(state["baseline"]["reference"])
        for key in ("worktree_root", "head", "branch", "dirty_fingerprints"):
            self.assertTrue(state["repository"][key], key)
        criterion_ids = {c["id"] for c in state["success_criteria"]}
        self.assertEqual({c["id"] for c in state["baseline"]["criteria"]}, criterion_ids)
        for attempt in state["attempts"]:
            self.assertIn(attempt["progress"], {"PROGRESS", "NO_PROGRESS", "REGRESSION", "UNKNOWN"})
            for check in attempt["checks"]:
                self.assertIn(check["criterion_id"], criterion_ids)
                self.assertIn(check["status"], {"PASS", "FAIL", "BLOCKED", "NOT_RUN"})
                self.assertTrue(check["evidence"])
        self.assertTrue(state["stop_reason"]["cause"])
        self.assertTrue(state["next_hypothesis"])


if __name__ == "__main__":
    unittest.main()
