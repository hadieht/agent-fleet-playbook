---
name: test-driven-development
description: Use when implementing any feature, bug fix or behavior change in production code, before writing the implementation. Enforces red-green-refactor with a test that is seen failing first. Don't use for throwaway prototypes, generated code or pure configuration unless the brief asks for tests.
---

# Test-driven development

## Iron law
> **No production code without a failing test first.** If you didn't watch the test fail for the right reason, you don't know that it tests anything.

If implementation code was written before its test, set it aside, write the test, watch it fail, then re-implement. Don't "adapt" the untested code into place.

## The cycle

### 1. RED: one failing test
- Test **one behavior**, with a name that states it: `rejects_empty_email`, `Total_IncludesTax_WhenRegionIsEU`.
- Write the assertion first, then work backwards to setup. Use the API you *wish* existed.
- Use real collaborators where cheap. Use fakes or mocks only at true boundaries (network, clock, file system, paid services).
- **Run it and confirm the failure:**
  - It must **fail**, not **error**. A compile error or missing import doesn't count; fix it and rerun.
  - It must fail **for the expected reason** (the assertion about the missing behavior).
  - If it passes immediately, it's testing existing behavior. Fix the test.

### 2. GREEN: the simplest code that passes
- Write the minimum production code to make that test pass. No extra options, no handling of cases no test demands yet.
- Run the **whole relevant suite**, not just the new test. Everything green, no new warnings.
- If the new test still fails, fix the **code**, not the test.

### 3. REFACTOR: clean while green
- Remove duplication, improve names and extract functions (skill `clean-code`). Change no behavior.
- Rerun the suite after each refactoring step.

### 4. Repeat
Pick the next behavior: happy path → edge cases → error cases.

## Bug fixes
1. Write a test that reproduces the bug. It must fail on the current code.
2. Fix the root cause (skill `systematic-debugging`).
3. The test passes and stays in the suite as a regression guard.

## Good tests
| Property | Rule |
|---|---|
| Focused | One behavior; if the name needs "and", split it |
| Behavioral | Assert on outputs and observable state, not on which private methods ran |
| Deterministic | No real time, randomness or network; inject clock, seed and fakes |
| Independent | Any order, in parallel; no shared mutable fixtures |
| Fast | Unit tests in milliseconds; slow integration tests marked and separated |
| Readable | Arrange / Act / Assert visible; builders over giant setup blocks |
| Meaningful | You can name the production bug that would make it fail |

## Test levels
- **Unit:** pure logic, most tests.
- **Integration:** real database, queue or HTTP pipeline (Testcontainers, in-process test servers). Use these for anything where the framework or the database *is* the behavior.
- **End-to-end:** a few critical user journeys only.
- Don't test framework code or trivial getters. Test *your* decisions.

## Red flags: stop and restart the cycle
- Production code exists with no test that failed first.
- A test passed on its first run and you didn't investigate.
- You changed a test's expected value to make it pass without understanding why.
- You're asserting that a mock was called instead of asserting an outcome.
- You disabled, skipped or deleted a failing test.
- "I tested it manually."

## Rationalizations to reject
| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code is quick to test, and simple code breaks too. |
| "I'll write tests after" | Tests written after pass immediately and prove nothing about their own validity. |
| "Manual testing is enough" | It isn't repeatable, and the next change will break it silently. |
| "This code is hard to test" | That's design feedback. Reduce coupling and inject the dependency. |
| "TDD is slower" | It's slower than skipping tests, not slower than debugging in production. |
| "I need to explore first" | Fine. Spike, throw the spike away, then TDD the real thing. |

## When stuck
| Problem | Do this |
|---|---|
| Don't know how to test it | Write the assertion you want first; design the API from the test |
| Setup is enormous | The unit is too big or too coupled; extract and inject |
| Must mock everything | Move logic into a pure function; mock only the boundary |
| Flaky test | Find the hidden time, order or shared-state dependency; never just retry |

See [reference/testing-anti-patterns.md](reference/testing-anti-patterns.md).

## Checklist before returning
- [ ] Every new behavior has a test that was **seen failing** for the right reason
- [ ] Minimal code to pass; refactoring done while green
- [ ] Full relevant suite passes; output has no new warnings
- [ ] Edge and error cases covered
- [ ] No skipped or disabled tests; no assertions weakened
- [ ] Test run output pasted in the verification log
