# Controlled Goal-Driven Codex Skill

A controlled Codex skill inspired by Li Dang's goal-driven agent workflow.

This project is based on the idea introduced in the original repository:

- Original GitHub repository: [lidangzzz/goal-driven](https://github.com/lidangzzz/goal-driven)
- Author on X: [@lidangzzz](https://x.com/lidangzzz)

This repository is not intended to be a magic prompt or an infinite agent loop. It is a practical rewrite of the goal-driven workflow idea for Codex, with explicit budgets, validation commands, stop conditions, and safer defaults.

## What this is

This is a Codex skill for complex coding tasks where progress can be objectively measured.

It is designed for tasks such as:

- test-driven bug fixing
- compiler or interpreter experiments
- large refactors
- migration tasks
- benchmark-driven optimization
- generated test suite validation
- repeated validation against a known expected output

The core idea is simple:

> A coding agent should not just “try harder”. It should work toward a clearly defined goal, check measurable success criteria, and stop when further progress is no longer justified.

## Origin and motivation

The original goal-driven prompt pattern by [@lidangzzz](https://x.com/lidangzzz) emphasizes persistent agent work until success criteria are met.

This project keeps the useful part of that idea:

- define a concrete goal
- define success criteria
- let the agent iterate toward the goal
- validate progress repeatedly

But this version adds stricter practical constraints for Codex usage:

- explicit iteration limits
- validation commands
- stop conditions
- no infinite loops
- no automatic activation
- clear final reporting
- conservative defaults when the user does not specify a budget

The purpose is to make goal-driven agent work more usable, auditable, and less wasteful.

## Why not run indefinitely?

Long-running agent workflows can be useful, but only when the task has objective validation.

For example, a long-running workflow makes sense when the agent can repeatedly run:

```text
npm test
cargo test
pytest
make test
go test ./...
```

or compare generated outputs against a known reference.

It is not useful when the goal is vague, such as:

```text
Make this project better.
Improve the codebase.
Keep optimizing until it is good.
```

In those cases, the skill should produce a plan and stop instead of burning tokens.

## Usage

Install the `skill` folder as a Codex skill.

Invoke it explicitly only when needed.

Example prompt:

```text
$controlled-goal-driven

Goal:
Fix the parser so all syntax tests pass.

Success criteria:
- npm test passes
- no unrelated files modified
- maximum 3 iterations
- stop if the same error repeats twice
```

## Design principles

This skill follows several rules:

1. Do not run indefinitely.
2. Do not claim success without validation.
3. Do not broaden the task without permission.
4. Do not rewrite unrelated files.
5. Do not create subagents unless they are useful for bounded investigation.
6. Stop when the same failure repeats.
7. Prefer a clear failure report over fake progress.

## Recommended task format

When using this skill, provide:

```text
Goal:
The concrete thing Codex should accomplish.

Success criteria:
How to know the task is complete.

Validation:
Commands Codex should run to verify progress.

Scope:
Files or directories Codex may edit.

Budget:
Maximum number of iterations or attempts.

Stop conditions:
When Codex should stop and report instead of continuing.
```

## Example

```text
$controlled-goal-driven

Goal:
Fix the TypeScript parser so it correctly handles optional chaining.

Success criteria:
- npm test passes
- new tests cover optional chaining
- no unrelated formatter changes
- maximum 4 iterations

Validation:
npm test

Scope:
src/parser/
tests/parser/

Stop conditions:
- stop if the same parser error repeats twice
- stop if the required behavior is unclear
- stop if tests cannot be run locally
```

## Final report format

At the end of a run, Codex should report:

- Goal
- Changes made
- Validation results
- Remaining issues
- Recommended next action

## Acknowledgement

This project is inspired by Li Dang's original goal-driven workflow:

- GitHub: [lidangzzz/goal-driven](https://github.com/lidangzzz/goal-driven)
- X: [@lidangzzz](https://x.com/lidangzzz)

This version is an independent, controlled adaptation focused on safer and more bounded Codex usage.
