# Optional Git Scope Check

Read this only when the task has explicit allowed paths and a Git-based scope check is useful. The checker is optional, uses Python 3's standard library, and **is not a sandbox**. Its `check` command only reads Git state; `snapshot` writes one JSON baseline (by default in the repository's Git metadata directory). Do not rely on it to prevent actions before they occur.

Run from the repository root, before **any** task edits:

```bash
python skill/scripts/check_scope.py snapshot
```

Run after each edit batch (before further edits) and at completion:

```bash
python skill/scripts/check_scope.py check --allow 'src/parser/**' --allow 'tests/parser/**'
```

Use `--repo /path/to/repo` **before** `snapshot` or `check` if necessary. Use `snapshot --output /path/to/file.json` and `check --snapshot /path/to/file.json` for an explicit shared location. In a linked worktree, the default snapshot path resolves through `git rev-parse --git-path` so it lives in the proper worktree metadata, not alongside tracked files.

Allow patterns are paths relative to the repository, expressed with forward slashes. An exact file (`src/parser.py`), a directory (`src/parser`), or a subtree (`src/parser/**`) is supported. Prefixes match **only component boundaries**: `src/api` does not match `src/api-extra`. Parent traversal, absolute paths, backslashes, and arbitrary globs are rejected. Supply repeated `--allow` options; no hidden all-files default.

The tool compares current tracked/unstaged/staged/untracked changes and commits after the recorded HEAD against SHA-256/index fingerprints for dirty paths that existed when `snapshot` was taken. Unchanged pre-existing modifications are excluded from the reported new changes, even if outside scope. Changes made later to those same files are conservatively flagged. Renames are handled as deletion plus addition; both paths must be permitted. This is state-based attribution, **not proof of who edited a path**: concurrent user edits and changes later reverted cannot be reliably attributed. If the baseline is stale or the working environment changes, inspect manually and take a fresh pre-edit snapshot for a new task; never silently refresh the baseline in the middle of an attempt.

Exit codes: `0` within scope, `2` out-of-scope changes, `3` invalid snapshot/Git/configuration error. In either error case, stop further unauthorized edits and report the findings. **Never automatically reset, clean, delete, or revert the user's files.** Treat this tool as defense in depth alongside explicit scope limits.
