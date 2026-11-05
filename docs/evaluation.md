# v1.2 Verification and Behavioral Evaluation

This project has two distinct evidence levels. **Do not describe the fixture tests as proving Codex behavior.**

## 1. Offline deterministic tests (no API key required)

From the repository root, with Python 3.11+ and Git installed:

```bash
python -m unittest discover -s tests -v
```

This verifies the Python Git-scope checker in temporary repositories (including staged/unstaged/untracked changes, renames, deletions, user-owned dirty files, prefix collisions, and traversal inputs), parses the behavior-fixture expectations, and checks required Skill references. GitHub Actions runs exactly this command on push and pull requests. Tests never run Codex and need no paid service or credentials.

## 2. Model-dependent behavioral evaluations (manual / opt-in)

The scenarios in [`tests/fixtures/behavior_scenarios.json`](../tests/fixtures/behavior_scenarios.json) specify a human-readable prompt, expected action, expected terminal state (or `null` when the agent should continue), required supporting evidence, and an explicit prohibition on claiming success in certain cases.

To evaluate actual Skill behavior:

1. Create a **disposable** repository fixture for each scenario and record its initial HEAD, dirty files, tests, and ground-truth expected outcome. Never run destructive scenarios in a contributor's real worktree.
2. Explicitly invoke `$controlled-goal-driven` for that fixture. Supply the scenario's input, scope, relevant validation commands, and finite budget. Do not let the agent see the expected answer field as an instruction.
3. Capture the Codex transcript, changed-file list, validation exit codes/test summaries, and edit iteration count. Avoid collecting secrets or user-owned private files.
4. Score `expected_action` and `expected_terminal` against the **observed** decision. Independently check every `required_evidence` item and that `must_not_claim_success` was respected. An answer that chooses the correct state without evidence **fails** the scenario.
5. Record introduced regressions and out-of-scope writes using an independent Git diff. Record attempts that made no justified improvement, elapsed time, and model/tool usage **only when observable**. Missing metrics must remain unknown, not estimated.
6. Repeat model runs when meaningful. Record model/version, date, fixture revision, and validation environment; do not treat one successful run as a universal guarantee.

Suggested scoring worksheet:

| Scenario ID | Action correct | Terminal correct | Evidence complete | False-success claim | Scope violation | Iterations | Time | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (fill from fixture) | yes/no | yes/no/N/A | yes/no | yes/no | yes/no | observed | observed/unknown | transcript link |

Aggregate separately: task completion rate, false-success rate, out-of-scope change rate, wasted iterations, and observed resource usage. Report denominators and unknowns. The evaluation cases are specifications for future manual/integrated Codex runs, **not** a claim that those runs have occurred.
