# Test-Driven Bug Fix

## Goal

Fix a parser bug that causes valid nested expressions to fail.

## Success criteria

- Existing parser tests pass.
- A regression test covers the nested-expression case.
- No unrelated behavior changes are introduced.

## Validation

```bash
npm test -- parser
```

## Scope

- `src/parser/**`
- `tests/parser/**`

## Budget

- Maximum 3 iterations.
- Stop earlier if the validation command passes.

## Stop conditions

- The same validation error appears twice.
- The bug requires changing files outside the allowed scope.
- Required reproduction details are missing.
