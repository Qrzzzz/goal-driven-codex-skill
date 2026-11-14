# Changelog

## 1.4.0 — 2026-11-14

- Add matching Windows PowerShell and Unix Bash installation instructions, version checks, deliberate preservation of customizations, rollback and reversible uninstall guidance (#15).
- Add a read-only, stdlib-only installed-package smoke checker for the Skill identity, explicit-only policy, version and transitive local references.
- Add regression tests for copied, stale, incomplete and misconfigured installations, plus a maintainer release checklist.

## 1.3.0 — 2026-11-14

- Add optional resource budgets and task-wide bounded diagnostic retries while retaining the three-iteration default (#12).
- Define opt-in versioned JSON checkpoints, fresh validation and compatibility gates for explicit cross-session resumption; preserve original evidence and cumulative budgets (#13).
- Add evaluation scenarios for budget exhaustion, transient failures, missing telemetry and checkpoint recovery. These are specifications, not claims of live model evaluation.
- Fix offline test portability for Windows UTF-8 decoding and unusual filenames; retain newline parser coverage on all platforms.
