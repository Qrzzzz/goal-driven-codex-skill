"""Offline Git-fixture tests for the optional scope checker."""

import importlib.util
import io
import json
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skill" / "scripts" / "check_scope.py"
spec = importlib.util.spec_from_file_location("check_scope", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScopeCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")
        self.write("src/api/core.py", "v1\n")
        self.write("src/api-extra/other.py", "v1\n")
        self.write("notes/user.txt", "initial\n")
        self.git("add", ".")
        self.git("commit", "-qm", "init")
        self.snapshot = Path(self.temp.name) / "baseline.json"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True).stdout

    def write(self, path, content):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

    def run_tool(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = module.main(["--repo", str(self.repo), *args])
        return code, stdout.getvalue(), stderr.getvalue()

    def take(self):
        code, _, err = self.run_tool("snapshot", "--output", str(self.snapshot))
        self.assertEqual(code, 0, err)

    def check(self, *allows):
        args = ["check", "--snapshot", str(self.snapshot)]
        for item in allows:
            args.extend(["--allow", item])
        return self.run_tool(*args)

    def test_allowed_unstaged_edit(self):
        self.take()
        self.write("src/api/core.py", "v2\n")
        self.assertEqual(self.check("src/api/**")[0], 0)

    def test_prefix_collision_rejected(self):
        self.take()
        self.write("src/api-extra/other.py", "v2\n")
        code, output, _ = self.check("src/api")
        self.assertEqual(code, 2)
        self.assertIn("src/api-extra/other.py", output)

    def test_untracked_staged_and_deleted(self):
        self.take()
        self.write("other/new.txt", "added\n")
        self.write("src/api/core.py", "v2\n")
        self.git("add", "src/api/core.py")
        (self.repo / "notes/user.txt").unlink()
        code, output, _ = self.check("src/api/**")
        self.assertEqual(code, 2)
        self.assertIn("other/new.txt", output)
        self.assertIn("notes/user.txt", output)

    def test_rename_checks_source_and_destination(self):
        self.take()
        self.git("mv", "src/api/core.py", "src/api-extra/renamed.py")
        code, output, _ = self.check("src/api/**")
        self.assertEqual(code, 2)
        self.assertIn("src/api-extra/renamed.py", output)

    def test_preexisting_dirty_files_ignored_if_unchanged(self):
        self.write("notes/user.txt", "user-owned change\n")
        self.write("notes/untracked.txt", "user-owned new file\n")
        self.take()
        self.write("src/api/core.py", "v2\n")
        self.assertEqual(self.check("src/api/**")[0], 0)
        self.assertEqual((self.repo / "notes/user.txt").read_text(), "user-owned change\n")
        self.assertEqual((self.repo / "notes/untracked.txt").read_text(), "user-owned new file\n")

    def test_preexisting_dirty_file_changed_later_is_detected(self):
        self.write("notes/user.txt", "user-owned change\n")
        self.take()
        self.write("notes/user.txt", "subsequent edit\n")
        self.assertEqual(self.check("src/api/**")[0], 2)

    def test_index_only_change_detected(self):
        self.take()
        self.write("notes/user.txt", "staged\n")
        self.git("add", "notes/user.txt")
        self.write("notes/user.txt", "initial\n")
        self.assertEqual(self.check("src/api/**")[0], 2)

    def test_changes_in_new_commit_detected(self):
        self.take()
        self.write("notes/user.txt", "committed\n")
        self.git("add", "notes/user.txt")
        self.git("commit", "-qm", "later")
        self.assertEqual(self.check("src/api/**")[0], 2)

    def test_path_traversal_and_absolute_allow_rejected(self):
        self.take()
        for invalid in ("../src", "src/../api", "/src", "C:/src", "src\\api", "src/*/bad"):
            self.assertEqual(self.check(invalid)[0], 3, invalid)

    def test_unusual_filename(self):
        self.take()
        self.write("odd/new\nname.txt", "new\n")
        code, output, _ = self.check("src/api/**")
        self.assertEqual(code, 2)
        self.assertIn("new\\nname.txt", output)

    def test_snapshot_repo_mismatch(self):
        self.take()
        data = json.loads(self.snapshot.read_text())
        data["root"] = "/some/other/repo"
        self.snapshot.write_text(json.dumps(data))
        self.assertEqual(self.check("src/api/**")[0], 3)

    def test_missing_snapshot(self):
        self.assertEqual(self.check("src/api/**")[0], 3)

    def test_preexisting_unchanged_staged_change(self):
        self.write("notes/user.txt", "staged by user\n")
        self.git("add", "notes/user.txt")
        self.take()
        self.write("src/api/core.py", "v2\n")
        self.assertEqual(self.check("src/api/**")[0], 0)


if __name__ == "__main__":
    unittest.main()
