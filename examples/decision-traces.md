# v1.1 Decision Traces (Illustrative)

These are **expected decisions for hypothetical scenarios**, not command output or an automated evaluation result. Validation statuses describe **checks**; progress classifications describe **changes between comparable rounds**; terminal states explain **why execution stopped**.

| Scenario | Evidence | Check status | Progress | Expected action / terminal state |
| --- | --- | --- | --- | --- |
| Relevant failures: 10 → 4 → 1; same assertion remains | Same test set and environment; no new regression | FAIL in each round | PROGRESS, PROGRESS | Continue while budget remains; **do not** stop for repeated assertion. If cap reached with remaining failure: BUDGET_EXHAUSTED |
| Failures: 4 → 4 → 4 | Same required test and environment; no criterion closer | FAIL | NO_PROGRESS, NO_PROGRESS | Stop: **NO_PROGRESS** |
| All selected unit tests green; required performance target unchecked | Unit tests pass, benchmark not run | Tests PASS, benchmark NOT_RUN | UNKNOWN for performance | **Not SUCCESS**. Run benchmark within budget; if it cannot run: BLOCKED |
| Validation command unavailable (missing test runner) | Command cannot start | BLOCKED | UNKNOWN | Stop: **BLOCKED**; do not infer an implementation failure |
| Comparable test outcome becomes worse | New critical security or API regression | FAIL | REGRESSION | Stop: **REGRESSION** if unsafe; otherwise attempt a bounded repair |
| Tests weakened/deleted to turn red into green | Required coverage removed; comparison invalid | New green result cannot establish criterion | UNKNOWN | Restore trustworthy checks; never call it PROGRESS or SUCCESS |
| Dependencies/environment change between runs | Counts cannot be compared | PASS/FAIL only for valid individual checks | UNKNOWN | At most one justified diagnostic; if reliable comparison cannot be restored: **BLOCKED** |
| All required checks and non-test criteria verified at iteration 1 | Passing tests, inspected scope, behavior contract verified | PASS for every required check | PROGRESS | Stop immediately: **SUCCESS**, leaving unused iterations |
| Product timezone policy is unspecified | Multiple plausible required outputs | NOT_RUN for policy-specific acceptance | UNKNOWN | Stop: **NEEDS_DECISION** before choosing behavior |
| Progress continues but iteration 3/3 still has unmet criteria | One relevant test still fails | FAIL | PROGRESS | Stop: **BUDGET_EXHAUSTED** (unless a more specific blocker/regression applies) |

## Evidence-based reporting examples

### Passing tests but incomplete goal

```text
Terminal state: BLOCKED — required performance check unavailable
Goal verification: NOT COMPLETE
Validation:
- npm test: PASS (all selected tests)
- npm run benchmark: BLOCKED (benchmark environment unavailable)
Criteria:
- Functional tests: verified
- Performance <= 100 ms p95: unverified
```

### Improving work despite a repeated error

```text
Baseline: 10 relevant failures
Iteration 1/3: 4 failures | PROGRESS | no new regression
Iteration 2/3: 1 failure  | PROGRESS | one old assertion still failing
Decision: CONTINUE (1 iteration remaining; focused hypothesis exists)
```

A check classified as PASS never automatically proves other, unverified acceptance criteria. An iteration classified as PROGRESS never overrides the hard budget.
