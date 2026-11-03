# Refactor With Scope

## Goal

Replace duplicated request validation logic with a shared helper **without changing observable runtime behavior**.

## Success criteria

- Related tests pass.
- Public API names, error cases, and response formats remain unchanged.
- Previously duplicated branches are consolidated into a single shared helper.
- Only allowed files are edited.

## Validation and baseline

```bash
pytest tests/api
```

Before edits, record the initial test status, existing worktree modifications, and representative API response/error behavior. During iterations use focused API tests (L1); before declaring success compare public API contracts and related regression tests (L2). Inspect the diff to verify removal of duplication and allowed scope.

**Important:** `pytest tests/api` returning PASS does **not** establish SUCCESS if the public API contract or code-structure requirement remains unverified. Report the missing criterion as **unverified** and obtain independent evidence; if it cannot be obtained, report **BLOCKED**, never PASS by assumption.

## Scope

- `src/api/validation.py`
- `src/api/routes/**`
- `tests/api/**`

## Budget

- Maximum 4 edit-and-validate iterations (explicit override of the default 3).
- Keep each iteration's diff reviewable.

## Stop conditions

- Two comparable iterations with no improvement → **NO_PROGRESS**.
- A necessary edit exceeds the permitted scope → **BLOCKED**.
- Public behavior depends on an undocumented product decision → **NEEDS_DECISION**.
- New API incompatibility that cannot be safely repaired within the budget → **REGRESSION**.
- All criteria verified with evidence → **SUCCESS** immediately.
