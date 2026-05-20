---
name: controlled-goal-driven
description: Use this skill only when the user explicitly requests a controlled, goal-driven Codex workflow for a complex coding or verification task with measurable success criteria.
---

# Controlled Goal-Driven Workflow

Use this skill only for complex tasks that have objective validation.

This workflow converts a broad coding task into a bounded iterative process with:

- a concrete goal
- measurable success criteria
- allowed scope
- validation commands
- iteration limits
- stop conditions
- a final report

## Required task fields

Before starting, identify or infer:

1. Goal
2. Success criteria
3. Allowed files and directories
4. Validation commands
5. Maximum iteration count
6. Stop conditions

If the user does not provide limits, use conservative defaults:

- maximum 3 iterations
- no unrelated file rewrites
- no subagents unless explicitly useful
- stop after 3 repeated failures
- stop if validation cannot be run

## Workflow

1. Restate the goal and success criteria briefly.
2. Inspect the repository.
3. Produce a short execution plan.
4. Work in bounded iterations.
5. After each iteration, run validation if available.
6. Continue only if the result is measurably closer to the success criteria.
7. Stop when the success criteria are met, the iteration limit is reached, the same failure repeats, or further progress requires external information.

## Rules

Do not run indefinitely.
Do not claim success without validation.
Do not broaden the task.
Do not rewrite unrelated files.
Do not consume tokens merely to keep working.
Use subagents only for bounded exploration, testing, or log analysis.
Summarize noisy intermediate results instead of dumping raw logs.

## Final report

At the end, report:

- Goal
- Changes made
- Validation results
- Remaining issues
- Recommended next action
