---
name: controlled-goal-driven
description: Use this skill only when the user explicitly requests a controlled, goal-driven Codex workflow for a complex coding or verification task with measurable success criteria.
---

# Controlled Goal-Driven Workflow

Invoke **explicitly** for complex coding or verification tasks with objective success criteria. Do not run open-ended loops, broaden scope, or claim completion based solely on model confidence or a subset of green tests.

## Required contract and baseline

Before edits, establish: (1) goal and individually verifiable success criteria, including non-test criteria; (2) allowed paths and user-owned existing changes; (3) executable checks or independently inspectable evidence; (4) finite edit-and-validate budget (default **3 iterations**); (5) stop conditions and decisions reserved for the user. Infer only safe, obvious defaults. If an essential decision is unclear, stop as **NEEDS_DECISION**; if necessary access or verification is unavailable, stop as **BLOCKED**.

Inspect the working tree **before** edits. Record the current HEAD, staged/unstaged/untracked user changes, relevant checks and their baseline outcomes, and which requirements are already met. Never reset, overwrite, or discard user changes. For more detailed baseline and regression methods, read [baseline-and-validation.md](references/baseline-and-validation.md) when results or environment are nontrivial.

## Bounded execution

1. Summarize the goal, success criteria, scope, budget, and verification plan.
2. Capture pre-edit evidence. If no trustworthy way to validate exists, plan and stop instead of editing.
3. Make one smallest justified edit batch inside scope. Every edit-plus-verification round counts toward the finite budget, including test-only edits.
4. Validate focused behavior (L1) and relevant regressions (L2); use build/integration/performance checks (L3) when necessary for the goal. Record each check as **PASS**, **FAIL**, **BLOCKED**, or **NOT_RUN**, with command or evidence source and observed result. BLOCKED/NOT_RUN never imply PASS.
5. Compare only trustworthy, comparable evidence against baseline and the previous round. Classify each iteration **PROGRESS**, **NO_PROGRESS**, **REGRESSION**, or **UNKNOWN**; record any new failure and a concrete next hypothesis. Do not count weakened/deleted tests or narrower criteria as improvement.
6. Stop immediately on verified completion, essential user decisions, unsafe regression, unavoidable blockers, two consecutive comparable NO_PROGRESS rounds, or budget exhaustion. A repeated individual error alone is **not** a stop condition. UNKNOWN permits at most one justified diagnostic before stopping if evidence stays unreliable.
7. Report the terminal state and evidence, without inventing results or exceeding the budget.

Terminal states: **SUCCESS**, **NO_PROGRESS**, **REGRESSION**, **BLOCKED**, **BUDGET_EXHAUSTED**, **NEEDS_DECISION**. SUCCESS requires positive evidence for **every** required criterion and no unresolved unacceptable regression. A fixable regression may receive a bounded repair; do not continue after an unsafe one. See [stop-and-progress.md](references/stop-and-progress.md) when choosing between terminal states or evaluating ambiguous progress.

## Optional Git scope guard

For Git repositories with explicit path allowlists, optionally use the stdlib-only [check_scope.py](scripts/check_scope.py) script: run `snapshot` before any edits, then `check --allow 'src/module/**'` after edits. It compares the current state against fingerprints of pre-existing user changes, including staged, unstaged, untracked, renamed and deleted paths; both sides of renames count. See [scope-check.md](references/scope-check.md) **only when adopting the checker**. A scope violation blocks further out-of-scope writes; report it without automatically reverting anything. This checker is advisory, not a security sandbox; inability to run it does not authorize ignoring the user's scope restriction.

## Final report

State: terminal state and reason; goal, scope and edits; baseline versus final evidence and iterations used; each acceptance criterion **verified / not met / unverified**; each validation command or observation **PASS / FAIL / BLOCKED / NOT_RUN**; regressions, blockers, remaining issues, and recommended next action. Clearly distinguish observations from inferences.

Do not create unbounded subagents, run indefinite retries, modify unrelated files, or broaden requirements without authorization. Preserve `agents/openai.yaml`'s explicit-invocation policy.
