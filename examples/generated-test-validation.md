# Generated Test Validation

## Goal

Generate targeted tests for a date-formatting utility and fix any implementation defects they expose.

## Success criteria

- Tests cover valid dates, invalid dates, leap years, and timezone boundaries.
- The utility passes meaningful generated tests, with relevant existing independent checks still passing.
- The generated tests genuinely exercise the intended behavior; they are not weakened or deleted to create a green result.
- Production changes stay within the allowed utility file.

## Validation and baseline

```bash
python -m pytest tests/generated/test_date_formatting.py
```

The generated file may not exist at baseline. Record that check as **NOT_RUN** (with reason) until the file is created; instead inspect existing related tests and the initial utility behavior as available. A newly written test passing by itself is insufficient evidence that the timezone policy is correct. Use existing tests or independently verified cases as a cross-check.

If Python or pytest is missing and the command cannot run, classify the required check as **BLOCKED**, not FAIL. Report the missing dependency; do not enter an unverified repair loop.

## Scope

- `src/date_formatting.py`
- `tests/generated/test_date_formatting.py`

## Budget

- Maximum 3 edit-and-validate iterations **including test generation**.
- Stop early only when all four coverage categories, implementation behavior, regression evidence, and scope have been verified.

## Stop conditions

- Two consecutive comparable iterations without measurable improvement → **NO_PROGRESS**.
- Missing dependency/credentials needed for verification → **BLOCKED**.
- The correct timezone behavior requires a user policy decision → **NEEDS_DECISION**.
- A newly introduced incorrect date behavior cannot be safely repaired → **REGRESSION**.
- The iteration cap is reached while required behavior remains unmet → **BUDGET_EXHAUSTED**.
