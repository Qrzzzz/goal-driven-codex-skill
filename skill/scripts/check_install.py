#!/usr/bin/env python3
"""Read-only smoke check for this Skill's installed files (stdlib only)."""

import argparse
from pathlib import Path
import re
import sys

NAME = "controlled-goal-driven"


def inspect(root, expected_version=None):
    root = Path(root).expanduser().resolve()
    errors = []

    def read(relative):
        try:
            return (root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"Missing or unreadable UTF-8 file: {relative}")
            return ""

    skill = read("SKILL.md")
    metadata = read("agents/openai.yaml")
    version = read("VERSION").strip()
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", skill, re.S)
    names = re.findall(r"^name:\s*([^\r\n]+)", front[1], re.M) if front else []
    if names != [NAME]:
        errors.append(f"SKILL.md must declare name: {NAME} exactly once in frontmatter")
    if not front or not re.search(r"^description:\s*\S", front[1], re.M):
        errors.append("SKILL.md frontmatter must include a description")

    # Check the shipped plain block-mapping policy without a mandatory YAML package.
    # This intentionally is not a general-purpose YAML validator.
    lines = [line.split("#", 1)[0].rstrip() for line in metadata.splitlines()]
    policy_starts = [i for i, line in enumerate(lines) if line == "policy:"]
    policy_values = []
    if len(policy_starts) == 1:
        for line in lines[policy_starts[0] + 1:]:
            if line and not line.startswith(" "):
                break
            match = re.fullmatch(r"  allow_implicit_invocation:\s*(\S+)", line)
            if match:
                policy_values.append(match[1])
    if policy_values != ["false"]:
        errors.append("agents/openai.yaml must set policy.allow_implicit_invocation: false once")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        errors.append("VERSION must contain a semantic version such as 1.4.0")
    if expected_version is not None and version != expected_version:
        errors.append(f"Version mismatch: expected {expected_version}, found {version or 'missing'}")

    # Check transitive local documentation links, including optional scripts/examples.
    pending = [(root / "SKILL.md", skill)]
    visited = set()
    while pending:
        source, content = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            path = (source.parent / target.split("#", 1)[0]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append(f"Missing or external installed reference from {source.name}: {target}")
            elif path.suffix == ".md" and path not in visited:
                try:
                    pending.append((path, path.read_text(encoding="utf-8")))
                except (OSError, UnicodeError):
                    errors.append(f"Unreadable installed reference: {target}")
    for relative in ("scripts/check_scope.py", "scripts/check_install.py"):
        if not (root / relative).is_file():
            errors.append(f"Missing helper: {relative}")
    return version, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Skill root; defaults to the directory containing this installed script")
    parser.add_argument("--expected-version", help="fail if a stale/different version is installed")
    args = parser.parse_args(argv)
    try:
        version, errors = inspect(args.root, args.expected_version)
    except OSError:
        print("FAIL: installation path cannot be inspected", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {NAME} {version}; files and explicit-only policy verified")
    print(f"Invoke explicitly in Codex: ${NAME}")
    print("This smoke check does not prove Codex discovery or live model behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
