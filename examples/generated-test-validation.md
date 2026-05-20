# Generated Test Validation

## Goal

Generate a focused test suite for a date-formatting utility and fix any implementation issues exposed by those tests.

## Success criteria

- Generated tests cover valid dates, invalid dates, leap years, and timezone edge cases.
- The utility passes the generated tests.
- No production files outside the date utility are changed.

## Validation

```bash
python -m pytest tests/generated/test_date_formatting.py
```

## Scope

- `src/date_formatting.py`
- `tests/generated/test_date_formatting.py`

## Budget

- Maximum 3 implementation iterations after the test file is generated.
- Stop earlier if validation passes.

## Stop conditions

- The same failing assertion appears twice.
- The correct timezone policy is unclear.
- Validation requires external services or credentials.
