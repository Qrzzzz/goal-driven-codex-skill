# Refactor With Scope

## Goal

Refactor duplicated request validation logic into a shared helper without changing runtime behavior.

## Success criteria

- Existing tests pass.
- Public API names and response formats remain unchanged.
- The duplicated validation branches are replaced by one shared helper.

## Validation

```bash
pytest tests/api
```

## Scope

- `src/api/validation.py`
- `src/api/routes/**`
- `tests/api/**`

## Budget

- Maximum 4 iterations.
- Each iteration must keep the diff reviewable.

## Stop conditions

- Tests fail with the same error twice.
- The refactor requires changing unrelated modules.
- The desired public behavior is unclear.
