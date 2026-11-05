"""Deterministic structure checks, not execution of agent instructions."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "SKILL.md"


class DocumentationChecks(unittest.TestCase):
    def test_skill_frontmatter_and_explicit_invocation(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: controlled-goal-driven\n"))
        self.assertIn("Invoke **explicitly**", skill)
        config = (ROOT / "skill" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", config)

    def test_skill_reference_links_exist(self):
        content = SKILL.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((references/[^)]+|scripts/[^)]+)\)", content):
            self.assertTrue((SKILL.parent / target).is_file(), target)
        self.assertIn("references/stop-and-progress.md", content)
        self.assertIn("references/baseline-and-validation.md", content)
        self.assertIn("references/scope-check.md", content)

    def test_core_safety_contract(self):
        content = SKILL.read_text(encoding="utf-8")
        for value in ("SUCCESS", "NO_PROGRESS", "REGRESSION", "BLOCKED", "BUDGET_EXHAUSTED", "NEEDS_DECISION", "PROGRESS", "UNKNOWN", "NOT_RUN", "PASS", "FAIL"):
            self.assertIn(value, content)
        self.assertIn("Never reset, overwrite, or discard user changes", content)
        self.assertIn("two consecutive comparable NO_PROGRESS", content)
        self.assertIn("baseline", content.lower())
        self.assertLess(len(content.splitlines()), 100)

    def test_references_explain_conditional_loading(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("when results or environment are nontrivial", skill)
        self.assertIn("only when adopting the checker", skill)
        self.assertIn("when choosing between terminal states", skill)


if __name__ == "__main__":
    unittest.main()
