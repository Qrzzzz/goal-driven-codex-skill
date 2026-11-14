"""Exercise the install smoke checker against copied, damaged and stale installs."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skill"
spec = importlib.util.spec_from_file_location("check_install", SKILL / "scripts/check_install.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "controlled-goal-driven"
        shutil.copytree(SKILL, self.root, ignore=shutil.ignore_patterns("__pycache__"))
        self.version = (SKILL / "VERSION").read_text(encoding="utf-8").strip()

    def test_installed_script_defaults_to_own_root_from_another_cwd(self):
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/check_install.py"),
             "--expected-version", self.version], cwd=self.root.parent,
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("$controlled-goal-driven", result.stdout)

    def test_stale_version_fails_without_modifying_installation(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        _, errors = checker.inspect(self.root, "0.0.0")
        self.assertTrue(any("Version mismatch" in e for e in errors))
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_missing_metadata_and_linked_reference_fail(self):
        (self.root / "agents/openai.yaml").unlink()
        (self.root / "references/resource-budgets.md").unlink()
        _, errors = checker.inspect(self.root)
        self.assertTrue(any("agents/openai.yaml" in e for e in errors))
        self.assertTrue(any("resource-budgets.md" in e for e in errors))

    def test_implicit_policy_and_misplaced_or_duplicate_values_fail(self):
        for content in (
            "policy:\n  allow_implicit_invocation: true\n",
            "interface:\n  allow_implicit_invocation: false\n",
            "policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: true\n",
            "policy:\n  allow_implicit_invocation: false\npolicy:\n  allow_implicit_invocation: true\n",
        ):
            with self.subTest(content=content):
                (self.root / "agents/openai.yaml").write_text(content, encoding="utf-8")
                self.assertTrue(checker.inspect(self.root)[1])

    def test_wrong_skill_name_and_missing_version_fail(self):
        path = self.root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "name: controlled-goal-driven", "name: another-skill"), encoding="utf-8")
        (self.root / "VERSION").unlink()
        _, errors = checker.inspect(self.root)
        self.assertTrue(any("must declare name" in e for e in errors))
        self.assertTrue(any("VERSION" in e for e in errors))

    def test_transitive_broken_reference_fails(self):
        reference = self.root / "references/session-state.md"
        with reference.open("a", encoding="utf-8") as stream:
            stream.write("\n[missing](missing-state.json)\n")
        self.assertTrue(any("missing-state.json" in e for e in checker.inspect(self.root)[1]))


if __name__ == "__main__":
    unittest.main()
