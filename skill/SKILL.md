---
name: controlled-goal-driven
description: Use this skill only when the user explicitly requests a controlled, goal-driven Codex workflow for a complex coding or verification task with measurable success criteria.
---

# Controlled Goal-Driven Workflow

Use only when explicitly invoked for a complex coding or verification task. Work toward agreed, objectively verifiable criteria within a bounded editing scope and iteration budget. Do not treat effort, a passing subset of tests, or a model's confidence as proof of success.

## Preflight: establish a contract

Before editing, identify or conservatively infer:

1. **Goal** and individually checkable **success criteria**, including non-test requirements.
2. **Allowed paths** and prohibited changes; preserve existing user modifications.
3. **Validation commands / evidence** appropriate to each criterion.
4. **Iteration budget** (default: at most **3 edit-and-validate iterations**).
5. **Stop conditions**, dependencies, and decisions requiring user authority.

Make only obvious, safe inferences. If a product decision or essential verification definition is missing, produce a plan and stop as **NEEDS_DECISION**. If necessary tools, credentials, files, external services, or scope are unavailable, stop as **BLOCKED**. Never invent a validation result. If no meaningful executable or independently inspectable validation can be established, do not enter the edit loop.

Inspect the repository and record a **pre-edit baseline**: working-tree status, relevant existing tests/checks, acceptance criteria already satisfied, known failures, and any unavailable checks. Run nondestructive baseline checks when feasible; if comparability is unavailable, state that limitation. Do not reset, overwrite, or discard user changes.

## Validation evidence

Track each required check separately using one of these statuses:

- **PASS** — ran successfully and the observed outcome meets that check's requirement.
- **FAIL** — ran and the requirement was not met (including an assertion or a measurable target failure).
- **BLOCKED** — could not obtain a valid result (missing tool/dependency, unavailable credential, timeout, or inaccessible service).
- **NOT_RUN** — not attempted; include the reason.

For every check, record the command or evidence source, observed result (exit code, test summary, measurement, or inspected artifact), and limitations. A nonzero command exit is not automatically a product-code failure; classify tool/environment problems as BLOCKED. A flaky check remains inconclusive until a bounded, justified rerun yields trustworthy evidence. Do not silently turn BLOCKED or NOT_RUN into PASS.

Choose verification depth according to risk:

- **L1:** focused tests, syntax/type checks, or the smallest relevant measurement.
- **L2:** related regression tests and contractual/API behavior.
- **L3:** full suite, build, integration, or performance verification when the goal or risk requires it.

Use L1 for iteration feedback and L2/L3 as appropriate before claiming completion. Do not run an expensive full suite in every round without justification. Passing selected tests does **not** establish SUCCESS if another required criterion (e.g. public API stability, security, performance) is unverified. Record each acceptance criterion as **verified**, **not met**, or **unverified**, with supporting check IDs/evidence.

## Progress relative to the baseline

Compare evidence against the pre-edit baseline and the last **comparable** iteration. Record fixed requirements, remaining failures, newly introduced regressions, and any change to the test environment. Weight user-defined requirements and severity above raw pass counts.

Classify the outcome of each edit-and-validate iteration:

- **PROGRESS:** a relevant unmet criterion is demonstrably closer to passing (e.g. comparable required failures drop from 10 to 4 to 1), with no unacceptable new regression.
- **NO_PROGRESS:** comparable evidence shows no meaningful improvement toward any outstanding required criterion.
- **REGRESSION:** a new material failure, behavior break, or unacceptable degradation is attributable to the edits.
- **UNKNOWN:** the environment, tests, or measurements changed enough to make comparison unreliable, or evidence is inconclusive.

Repetition of one failing assertion is **not** by itself a stopping condition. Two consecutive comparable NO_PROGRESS iterations terminate as **NO_PROGRESS**. UNKNOWN is **not** progress and does not clear a previous no-progress streak; at most one bounded diagnostic/rerun may restore comparability. If trustworthy verification cannot be restored, stop as BLOCKED. Treat regressions as higher priority than superficial pass-count improvements.

Do **not** gain apparent progress by deleting/weakening required tests, relaxing success criteria, suppressing failures, or narrowing validation. Legitimate test changes are allowed only when justified by the goal and checked against independent or existing evidence; explain changed baselines explicitly.

## Bounded loop

1. Restate the goal, criteria, permitted paths, budget, and validation plan concisely.
2. Inspect the repository and capture the baseline before modifying files.
3. Make the smallest justified change within scope. One batch of edits followed by validation counts as **one iteration**, including test-only edits. Diagnostics without edits do not reset the counter.
4. Run focused validation; record per-check statuses and a progress classification. Run broader relevant verification before declaring success.
5. Apply the decision rules below. Continue only when a specific next hypothesis is justified, verification is available, and budget remains; do not keep trying solely to consume the budget.
6. Finish with the evidence-based final report.

**Hard limit:** maximum 3 iterations by default, or the user's explicitly specified smaller/larger finite limit. Never exceed it, and never run indefinite diagnostic retries. A prior failure can be fixed within the remaining budget; the same error reappearing is not an automatic stop.

## Terminal decision rules

Use exactly one final terminal state, with a short reason and evidence. Evaluate after validation and whenever blocked. If multiple conditions hold, prefer the more informative root cause in this order:

1. **REGRESSION** — stop immediately for a dangerous/unacceptable new regression; for a fixable regression, one bounded repair is permissible if safe and budget remains. If it is still unresolved at the end, report REGRESSION.
2. **NEEDS_DECISION** — an essential user-owned product, scope, or acceptance decision is unresolved. Do not guess or expand scope.
3. **BLOCKED** — required verification, dependency, permission, or allowed editing scope prevents responsible continuation. Do not mislabel a blocked check as a code failure.
4. **SUCCESS** — **every** required criterion has positive evidence and there are no unresolved unacceptable regressions. Stop immediately; do not use remaining iterations.
5. **NO_PROGRESS** — two consecutive comparable iterations showed NO_PROGRESS and no supported next step justifies continuing.
6. **BUDGET_EXHAUSTED** — the finite iteration cap was reached without verified success or a more specific terminal cause.

If evidence is UNKNOWN, attempt only bounded diagnosis; then classify the resulting blocker or unmet goal without claiming success. At each stop, say what is proven, what remains unverified, and what would unblock the next step.

## Iteration record

Keep records compact and factual. Example format (illustrative, not executed):

```text
Iteration 2/3 | changed: src/parser/parse.ts
Checks: parser tests FAIL (1 vs 4 previous, 10 pre-edit failures); related regressions PASS
Progress: PROGRESS | new regressions: 0 | next: fix remaining nested-expression case
```

Summarize noisy logs rather than pasting them. Always identify the next hypothesis before another edit.

## Final report

Include:

- **Terminal state and reason** (one of the six states above).
- **Goal, allowed scope, and changes made**, including unexpected or pre-existing changes.
- **Baseline vs final evidence** and iteration count.
- **Success criteria:** verified / not met / unverified, with evidence.
- **Validation:** commands or sources, PASS / FAIL / BLOCKED / NOT_RUN, and limitations.
- **Remaining failures, regressions, blockers, and next action.**

Do not claim full success when only a subset of required checks passed. Never overwrite unrelated files, change user constraints, invent observations, create unbounded subagents, or broaden the task without explicit authorization.
