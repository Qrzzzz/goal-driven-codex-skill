# Test-Driven Bug Fix

## Goal

Fix a parser bug that rejects valid nested expressions.

## Success criteria

- Existing parser tests pass.
- A regression test reproduces the nested-expression bug and passes with the fix.
- No unrelated parser behavior is changed and no files outside the permitted paths are edited.

## Validation and baseline

```bash
npm test -- parser
```

Before edits, inspect the diff/worktree and record the existing parser-test result. After the focused tests, check any relevant parser regression or compatibility suite, if available. Inspect the added regression test and changed files; a green command alone does not verify the full scope and behavior requirements.

## Scope

- `src/parser/**`
- `tests/parser/**`

## Budget

- Maximum 3 **edit-and-validate** iterations, including test-only changes.
- Stop immediately if all success criteria are verified, not merely when the first command turns green.

## Example iteration decisions

The numbers below are hypothetical, not results from this repository:

| Stage | Comparable parser failures | Decision | Reason |
| --- | ---: | --- | --- |
| Baseline | 10 | — | Known initial failures |
| Iteration 1 | 4 | PROGRESS | Six relevant failures fixed, no new regression |
| Iteration 2 | 1 | PROGRESS | Three more fixed; one assertion still fails |
| Iteration 3 | 0 | SUCCESS **only if** all criteria verified | Regression test and unrelated behavior must also be checked |

The same failing assertion appearing in iterations 1 and 2 does **not** cause an automatic stop. If the cap is reached with one unresolved failure, report **BUDGET_EXHAUSTED** (or **REGRESSION** if the edits introduced an unresolved new failure).

## Stop conditions

- Two consecutive comparable NO_PROGRESS iterations → **NO_PROGRESS**.
- A required fix would exceed permitted paths → **BLOCKED** until scope is authorized.
- Missing reproduction facts requiring a user decision → **NEEDS_DECISION**.
- A new unacceptable regression that cannot be safely repaired → **REGRESSION**.
