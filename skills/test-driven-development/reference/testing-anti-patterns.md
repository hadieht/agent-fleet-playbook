# Testing anti-patterns

| Anti-pattern | Why it's harmful | Instead |
|---|---|---|
| **Testing the mock** | Asserting `mock.verify(save)` proves wiring, not behavior | Assert the saved state or returned result; use a fake repository |
| **Mocking what you don't own** | Mocks of third-party APIs encode your guess of their behavior | Wrap the third party in your own adapter; mock the adapter; integration-test the adapter |
| **Over-mocking** | Tests pass while the real system is broken | Real objects for in-process collaborators; mocks only at I/O boundaries |
| **Test-only production code** | `if (isTest)` branches or public members just for tests | Inject dependencies; test via public API |
| **Assertion-free tests** | "Doesn't throw" is rarely the requirement | Assert specific outcomes |
| **Giant arrange** | 50 lines of setup hides intent | Test data builders, object mothers, factory helpers |
| **Shared mutable fixtures** | Order-dependent, flaky tests | Fresh state per test; transactions rolled back per test |
| **Sleep for async** | Slow and still flaky | Await the operation; poll a condition with a timeout |
| **Real clock / random** | Non-deterministic failures | Inject a clock (`TimeProvider`, `freezegun`, fake timers) and seeded randomness |
| **In-memory DB pretending to be relational** | Misses constraints, transactions and SQL dialect behavior | Real database in a container for data-access tests |
| **Snapshot everything** | Every change "updates snapshots" without review | Small, targeted snapshots; explicit assertions for key fields |
| **Testing private methods** | Couples tests to implementation | Test via public behavior; extract a class if it's complex enough to need its own tests |
| **Coverage as the goal** | 100% coverage with weak assertions catches nothing | Coverage finds *untested* code; mutation testing measures test *strength* |
| **Ignoring flaky tests** | Teaches everyone to ignore red | Quarantine with a ticket and fix the root cause quickly |
| **Catch-all exception assertions** | `assertThrows(Exception)` passes for the wrong error | Assert the specific exception type and message |

## Strengthening a suite
- **Mutation testing** (Stryker for .NET/JS/TS, mutmut for Python, PIT for Java) shows which lines can change without any test failing.
- **Property-based testing** (FsCheck, Hypothesis, fast-check) finds edge cases: state an invariant and let the tool generate inputs.
- **Contract tests** keep service boundaries honest without full end-to-end environments.
