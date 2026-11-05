#!/usr/bin/env python3
"""Advisory Git change-scope checker. Never modifies repository files."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

SCHEMA = 1
SNAPSHOT_NAME = "controlled-goal-driven.scope.json"


class ScopeError(Exception):
    pass


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False
    )
    if result.returncode:
        raise ScopeError(result.stderr.decode("utf-8", "replace").strip() or "Git command failed")
    return result.stdout


def root_for(path):
    root = git(Path(path), "rev-parse", "--show-toplevel").decode("utf-8", "surrogateescape").strip()
    return Path(root).resolve()


def nul_paths(data):
    return {os.fsdecode(item) for item in data.split(b"\0") if item}


def local_changes(root):
    # --no-renames reports both old and new paths, including rename/deletion cases.
    paths = set()
    for args in (
        ("diff", "--no-renames", "--name-only", "-z", "HEAD"),
        ("diff", "--no-renames", "--cached", "--name-only", "-z", "HEAD"),
        ("diff", "--no-renames", "--name-only", "-z"),
        ("ls-files", "--others", "--exclude-standard", "-z"),
    ):
        paths.update(nul_paths(git(root, *args)))
    return paths


def file_fingerprint(root, name):
    path = root / name
    try:
        info = path.lstat()
    except FileNotFoundError:
        worktree = "missing"
    else:
        if stat.S_ISLNK(info.st_mode):
            worktree = "symlink:" + os.readlink(path)
        elif stat.S_ISREG(info.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            worktree = "file:" + digest.hexdigest() + ":" + str(stat.S_IMODE(info.st_mode))
        else:
            worktree = "special:" + str(info.st_mode)
    # Include index entries so a staged change is visible even if the working copy is unchanged.
    index = git(root, "ls-files", "--stage", "-z", "--", name)
    return hashlib.sha256(worktree.encode("utf-8", "surrogateescape") + b"\0" + index).hexdigest()


def snapshot_path(root, override):
    if override:
        return Path(override).expanduser().resolve()
    raw = git(root, "rev-parse", "--git-path", SNAPSHOT_NAME).decode("utf-8", "surrogateescape").strip()
    path = Path(raw)
    return path if path.is_absolute() else root / path


def allowed_pattern(pattern):
    if not pattern or "\\" in pattern or pattern.startswith("/") or re.match(r"^[A-Za-z]:", pattern):
        raise ScopeError(f"Invalid allow path: {pattern!r}")
    is_tree = pattern.endswith("/**")
    base = pattern[:-3] if is_tree else pattern.rstrip("/")
    if not base or any(part in ("", ".", "..") for part in base.split("/")) or any(ch in base for ch in "*?[]\0"):
        raise ScopeError(f"Invalid allow path: {pattern!r}; use exact paths or directory/**")
    return base, is_tree


def is_allowed(path, patterns):
    return any(path.startswith(base + "/") if tree else (path == base or path.startswith(base + "/")) for base, tree in patterns)


def capture(root, output):
    head = git(root, "rev-parse", "HEAD").decode("ascii").strip()
    initial = {name: file_fingerprint(root, name) for name in sorted(local_changes(root))}
    data = {"schema": SCHEMA, "root": str(root), "head": head, "initial_changes": initial}
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.name + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(output)
    print(f"Snapshot saved: {output} ({len(initial)} pre-existing changed paths)")


def check(root, baseline, allows):
    if not baseline.is_file():
        raise ScopeError(f"Baseline missing: {baseline}; run snapshot before editing")
    try:
        data = json.loads(baseline.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ScopeError(f"Invalid baseline: {exc}") from exc
    if data.get("schema") != SCHEMA or data.get("root") != str(root) or not isinstance(data.get("initial_changes"), dict):
        raise ScopeError("Baseline schema/repository mismatch; create a fresh pre-edit snapshot")
    head = data.get("head")
    if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40,64}", head):
        raise ScopeError("Baseline commit is invalid")
    patterns = [allowed_pattern(value) for value in allows]
    if not patterns:
        raise ScopeError("Supply one or more --allow paths")
    committed = nul_paths(git(root, "diff", "--no-renames", "--name-only", "-z", head, "HEAD"))
    candidates = local_changes(root) | committed
    original = data["initial_changes"]
    actual = {name for name in candidates if original.get(name) != file_fingerprint(root, name)}
    violations = sorted(name for name in actual if not is_allowed(name, patterns))
    if violations:
        print("FAIL: paths changed outside the allowed scope:")
        for name in violations:
            print(f"  {name!r}")
        print("Do not automatically revert or delete files. Investigate and report the violation.")
        return 2
    print(f"PASS: {len(actual)} changed paths within scope; {len(candidates - actual)} unchanged baseline paths ignored")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="path inside the target Git repository")
    sub = parser.add_subparsers(dest="action", required=True)
    take = sub.add_parser("snapshot", help="record pre-edit dirty paths and fingerprints")
    take.add_argument("--output", help="snapshot file (default: inside the Git metadata directory)")
    verify = sub.add_parser("check", help="compare current changes against the pre-edit snapshot")
    verify.add_argument("--snapshot", help="pre-edit snapshot file")
    verify.add_argument("--allow", action="append", default=[], help="exact path or subtree/** (repeatable)")
    args = parser.parse_args(argv)
    try:
        root = root_for(args.repo)
        if args.action == "snapshot":
            capture(root, snapshot_path(root, args.output))
            return 0
        return check(root, snapshot_path(root, args.snapshot), args.allow)
    except (ScopeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
