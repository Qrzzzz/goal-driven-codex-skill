# Baseline and Regression Verification

Read this reference for dirty worktrees, multiple checks, non-test acceptance criteria, inconclusive test results, or potential regressions. For simple tasks, the checklist in `SKILL.md` is sufficient.

## Before the first edit

1. Record branch and HEAD (`git status --short --branch`, `git rev-parse HEAD`), with existing staged, unstaged, deleted, renamed, and untracked paths. Do not run `git reset`, `git clean`, or overwrite pre-existing work.
2. List every independently verifiable success criterion. Mark each **verified**, **not met**, or **unverified** and state its supporting evidence.
3. Choose L1 focused checks, L2 related regression/API-contract checks, and L3 full/build/integration/performance checks only when applicable. Where practical, run relevant checks before changes to establish a comparable baseline, including known failing case identifiers, not just pass counts.
4. When the pre-edit command cannot run, record **BLOCKED** and the error. If a generated test file does not exist yet, record **NOT_RUN**, and use independent existing tests or inspected behavior if feasible. Never fabricate an initial result.
5. If a meaningful success criterion has no verification path, stop and seek a decision rather than beginning an unverified repair loop.

## After each iteration

Use the **same test identifiers, environment, configuration, and inputs** when comparing results. If test inventory or external conditions changed, mark progress **UNKNOWN** and explain why; do not compare raw counts as though they were equivalent.

For each check report command/evidence, result, status, baseline result, current result, and limits. A missing runner, permission, credential, or timeout is **BLOCKED**, not proof the implementation is faulty. With flaky tests, make at most one justified diagnostic/rerun, retaining both outcomes. A failed assertion in a valid run is **FAIL**. A check not attempted is **NOT_RUN**.

Treat tests that already failed before edits as **pre-existing failures**. Only previously passing checks or verified criteria that now fail under comparable conditions are **new regressions**. An independent inspection/measurement can establish a regression if an automated suite is unavailable. Prioritize user acceptance criteria, severity and regression risk over total pass count. Do not weaken tests to manufacture improvement.

Before declaring SUCCESS, execute appropriate L2/L3 checks and verify all non-test criteria (public contracts, performance targets, scope constraints) with observed evidence. No suite is mandatory if irrelevant; conversely, a passing selected suite is insufficient for unrelated required criteria.

## Small report template

```text
Baseline: HEAD abc123; user-owned changes: notes.txt (unchanged)
Criterion: parser rejects nested expressions — not met (3 named assertions fail)
Iteration 1/3: parser tests FAIL (1 existing failure, from 3); PROGRESS
New regressions: 0; focused check: FAIL; related API checks: PASS
Final criterion: verified / not met / unverified with specific evidence
```

When a check is BLOCKED, explain the unavailable input and the next responsible action; do not misreport it as FAIL or PASS. If scope needs widening, request authorization instead of silently changing it.
