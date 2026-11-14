# Changelog

## 1.3.0 — 2026-11-14

- Add optional resource budgets and task-wide bounded diagnostic retries while retaining the three-iteration default (#12).
- Define opt-in versioned JSON checkpoints, fresh validation and compatibility gates for explicit cross-session resumption; preserve original evidence and cumulative budgets (#13).
- Add evaluation scenarios for budget exhaustion, transient failures, missing telemetry and checkpoint recovery. These are specifications, not claims of live model evaluation.
- Fix offline test portability for Windows UTF-8 decoding and unusual filenames; retain newline parser coverage on all platforms.
