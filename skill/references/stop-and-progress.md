# Stop States and Comparable Progress

Read this reference when deciding whether to retry, classify an inconclusive result, resolve conflicting stop reasons, or explain a non-success exit. The core `SKILL.md` is sufficient for straightforward success.

## Per-check evidence and per-iteration movement

- Check **PASS**: valid execution/evidence meets that specific check. **FAIL**: valid execution does not meet it. **BLOCKED**: no valid result (environment, tool, credentials, timeout, etc.). **NOT_RUN**: not attempted, with reason.
- Iteration **PROGRESS**: a required unmet criterion measurably improves on comparable evidence, with no unacceptable new regression. **NO_PROGRESS**: comparable results show no meaningful advance. **REGRESSION**: new attributable material failure or degradation. **UNKNOWN**: comparisons are invalid/inconclusive.
- Identical error text in two rounds never *by itself* causes a stop. Failures 10 → 4 → 1 may be PROGRESS even if one assertion remains. Two consecutive comparable NO_PROGRESS edit rounds lead to **NO_PROGRESS**. UNKNOWN neither counts as progress nor resets a no-progress streak; allow at most one bounded diagnostic, then BLOCKED if trust cannot be restored.
- A test changed to become easier cannot establish PROGRESS by itself. Validate test edits against original acceptance conditions and independent checks. Record environment or test-inventory changes.

## Terminal-state priority

Use exactly one state; explain other unresolved conditions in the report. After unsafe regressions, stop; a fixable regression may receive a safe repair within the budget.

1. **REGRESSION**: unsafe or unresolved new material regression after any permitted repair.
2. **NEEDS_DECISION**: essential product, scope, or acceptance judgment belongs to the user.
3. **BLOCKED**: tools, permissions, trusted validation, resources, or allowed editing scope prevent responsible continuation.
4. **SUCCESS**: every required criterion independently verified; no unacceptable unresolved regression. Stop immediately even if budget remains.
5. **NO_PROGRESS**: two comparable consecutive NO_PROGRESS rounds with no evidence-backed next step.
6. **BUDGET_EXHAUSTED**: finite edit-iteration limit reached with unmet requirements and no more specific cause.

Do not keep trying just to exhaust the allowed rounds. Count a batch of edits followed by validation as one iteration (including test-only edits); diagnostics without edits do not reset the budget. Do not exceed the user's finite cap. When several states fit, report the most specific underlying stop reason rather than an invented success.

## Reporting

For any terminal result, include the trigger, supporting observations, unresolved criteria, whether the current changes are safe, iteration count, and next action. Clearly label unknown and skipped evidence; a model's self-assessment is never a substitute for execution results.
