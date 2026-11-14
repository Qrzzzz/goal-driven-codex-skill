# Resource Budgets and Bounded Retries (v1.3)

Read only when the task needs extra limits, retries, or resource accounting. A short `Budget: maximum 3 edit-and-validate iterations` remains sufficient. This is an execution protocol, not a scheduler, billing client, or automatic timeout mechanism.

## Optional dimensions

| Dimension | Default | Accounting |
| --- | --- | --- |
| Implementation iterations | 3 | Each edit batch plus verification, including test-only edits; a resumed session keeps the count. |
| Validation/diagnostic retries | 0 | Extra executions of an inconclusive check without edits; a task-wide cap, not a new allowance per command/session. |
| Active elapsed seconds | No extra cap | If specified, include planning, edits, checks and diagnostics while executing the task; carry cumulative usage across sessions, excluding idle gaps. |
| Command timeout seconds | No extra cap | If specified, apply to each subprocess using a supported timeout mechanism; record actual timeouts. |
| Tool calls / model tokens / cost | No extra cap | Enforce only from trustworthy counters with a defined scope and units. All calls, including failed ones and retries, consume the applicable limit. |

Example: `Budget: 3 iterations; 1 diagnostic retry total; 600 active seconds; 60 seconds per command.` These extra controls are optional. Account for validation needed to establish completion before starting another edit. Do not launch work known to exceed the remaining budget; an iteration allowance alone does not permit indefinite checks.

Record limits, consumed and remaining values separately. For an edit round record, for example: `iteration 2/3; diagnostic retries 1/1; active seconds 145/600; focused check BLOCKED (timeout); next hypothesis: inspect offline evidence`. Diagnostics never reset the iteration count or NO_PROGRESS streak. The one diagnostic allowed for UNKNOWN in the stop-state reference is an upper bound, not a free retry: it must also fit the agreed retry and resource budgets.

## Retry decisions

- **Deterministic implementation failure** (same assertion/compiler error with unchanged inputs): record FAIL. Re-running unchanged code is not a repair. Make a supported in-scope edit within the implementation budget, or stop under the progress/stop rules.
- **Transient environment failure** (one connection reset or temporary unavailable service): record BLOCKED for that attempt. Retry only with a specific reason it may clear, an explicitly available retry allowance, and remaining time/usage budget. Each extra execution consumes one retry, whether it succeeds or fails.
- **Suspected flaky test**: preserve both observations and investigate the cause with a bounded diagnostic. A later green run alone does not establish stable behavior or erase the failure. Restore trustworthy evidence before SUCCESS.
- **Persistent missing dependency, denied access, or unavailable credentials**: BLOCKED; repeated execution cannot provide the missing prerequisite.

Do not retry side-effecting commands unless their prior outcome is known and repeating them is safe and authorized. If the outcome is uncertain, inspect first or request the necessary decision; a retry budget is not authorization for duplicate writes.

## Exhaustion and missing telemetry

Stop when **any agreed dimension** prevents the next necessary action. Use BUDGET_EXHAUSTED and name the dimension (`validation_retries: used 1, limit 1`, for example), remaining unmet criteria, and next action. The per-check status remains FAIL, BLOCKED or NOT_RUN as actually observed. A command timeout is BLOCKED for that check; it becomes a terminal budget exit only if the agreed timeout/remaining allowance prevents required verification. Otherwise a permitted, safe diagnostic can proceed. Independently unsafe regressions or essential decisions retain the higher priority in [stop-and-progress.md](stop-and-progress.md).

If completion was already fully verified within budget, stop with SUCCESS; do not perform extra work to spend the allowance. If the cause is an unavailable prerequisite rather than a consumed allowance, report BLOCKED.

Without reliable token/cost counters, record `null`/unknown, never estimated token or dollar figures. Use finite observable iterations and retries, and elapsed time/command timeouts when measurable. If the user requires a hard unobservable cost/usage cap, disclose that enforcement is unavailable and stop BLOCKED pending an enforceable alternative; do not silently substitute a different cap. Do not reset accounting to continue, or treat a fresh session as a fresh budget.
