---
name: controlled-goal-driven
description: Use this skill only when the user explicitly requests a controlled, goal-driven Codex workflow for a complex coding or verification task with measurable success criteria.
---

# Controlled Goal-Driven Workflow

Use this skill only for complex tasks with objective validation. The workflow turns a broad coding or verification task into a bounded iterative process with a concrete goal, measurable success criteria, allowed scope, validation commands, iteration limits, stop conditions, and a final report.

## Required task fields

Before starting, identify or infer:

1. Goal
2. Success criteria
3. Allowed files and directories
4. Validation commands
5. Maximum iteration count
6. Stop conditions

If any required field is missing, use conservative defaults only when they are obvious from the request. Otherwise, produce a plan and stop.

Default limits:

- maximum 3 iterations
- no unrelated file rewrites
- no subagents unless they have a bounded purpose and a clear output
- stop if validation cannot be run
- stop if the same validation error appears twice

## Start criteria

Start the iteration loop only when validation is concrete enough to run.

If no validation command exists, produce a plan and stop instead of entering an iteration loop.

If the task requires external credentials, paid APIs, missing files, or unclear product decisions, stop and report what is blocked.

## Workflow

1. Restate the goal and success criteria briefly.
2. Confirm the allowed editing scope and validation command.
3. Inspect the repository.
4. Produce a short execution plan.
5. Work in bounded iterations.
6. After each iteration, run validation.
7. Continue only if the result is measurably closer to the success criteria.
8. Stop when success criteria are met, the iteration limit is reached, the same error repeats twice, or further progress requires blocked information or resources.

## Iteration report

Each iteration must include:

1. What changed
2. What validation was run
3. What result was observed
4. Whether the next iteration is justified

Summarize noisy logs. Include only the lines needed to explain the result.

## Rules

- Do not run indefinitely.
- Do not claim success without validation.
- Do not broaden the task.
- Do not rewrite unrelated files.
- Do not consume tokens merely to keep working.
- Do not create subagents unless they have a bounded purpose and a clear output.
- Stop and report if validation fails with the same error twice.
- Stop and report if required credentials, paid APIs, files, or product decisions are unavailable.

## Final report

At the end, report:

- Goal
- Changes made
- Validation results
- Remaining issues
- Recommended next action
