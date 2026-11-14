---
name: systematic-debugging
description: Use for any bug, failing test, crash, wrong output, performance regression, flaky behavior or build/CI failure, before proposing any fix. Finds the root cause through evidence instead of trial-and-error. Don't use for feature work with no defect.
---

# Systematic debugging

## Iron law
> **No fix without a root cause.** A change that makes the symptom disappear without explaining it is a guess, and guesses come back.

## Phase 1: Investigate (no code changes yet)
1. **Read the whole error:** message, full stack trace, error codes, line numbers, *and* the first error in the log (later errors are often fallout).
2. **Reproduce it reliably.** Write the exact steps or command. If you can't reproduce it, gather more data (logs, inputs, environment) rather than guessing.
3. **Check what changed:** recent commits (`git log -p`, `git bisect` for regressions), dependency versions, config, environment, data.
4. **Instrument boundaries** in multi-component systems (client → API → queue → worker → DB). Log what enters and leaves each boundary, run once, and find the first boundary where the data is wrong.
5. **Trace backward** from the symptom to the origin: where did this bad value come from? Who called with it? Keep going until you reach the source, not just the place it blew up.

## Phase 2: Compare against what works
1. Find working code that does something similar, in the same codebase or the library's docs and examples.
2. Read the working reference **completely**, not just the part you think matters.
3. List **every** difference between working and broken: inputs, config, versions, order of calls, environment, permissions, data shape.

## Phase 3: Hypothesize and test
1. Write one hypothesis: **"The root cause is X, because evidence Y."**
2. Design the smallest experiment that could prove it **wrong**, and change **one variable at a time**.
3. Disproved → form a new hypothesis from the new evidence. Don't stack a second fix on top of the first.
4. Don't understand something? Say so, read the source or docs, or escalate. Don't pretend.

## Phase 4: Fix
1. **Write a failing test that reproduces the bug** (skill `test-driven-development`).
2. Make **one** fix at the root cause. No unrelated refactoring in the same change.
3. Verify: the new test passes, the full suite passes, and the original reproduction steps no longer fail.
4. Ask whether the same bug exists elsewhere. Search for the pattern (variant analysis) and add defense in depth where cheap.

## The three-strike rule
If **three** fixes have failed, stop. Repeated failure means your model of the system is wrong, or the design is. Write up what you've learned, question the architecture, and escalate to the planner or human before attempting a fourth fix.

## When no root cause is found
Some failures really are environmental or timing-related. Then:
- Document everything you checked and ruled out.
- Add targeted handling (retry with backoff, timeout, clearer error) **and** logging or metrics that will capture the cause next time.
- Say so explicitly in your output. Most "no root cause" conclusions come from incomplete investigation, so list what you'd check next.

## Techniques
| Situation | Technique |
|---|---|
| "It worked last week" | `git bisect` between the good and bad commits |
| Flaky test | Run it 50× in a loop; vary order and parallelism; look for shared state, time, randomness or races |
| Works locally, fails in CI | Diff environments: OS, runtime version, env vars, locale, timezone, file paths, case sensitivity |
| Huge input fails | Delta-debug: halve the input until it's minimal |
| Performance regression | Profile before and after (skill `performance-engineering`); don't guess hotspots |
| Intermittent production error | Correlate logs by request or trace ID; find the common factor |
| Async or timing | Replace sleeps with condition waits; add sequence logging with timestamps |

## Red flags: back to Phase 1
- "Let me just try…" / "Maybe if I change…"
- Several changes made at once.
- A fix proposed before reproducing the bug.
- Copying a pattern you don't understand.
- Adding a `try/catch`, null check or retry that hides the symptom.
- Increasing a timeout without knowing why the operation is slow.

## Output format
```
## Symptom          # exact error + repro steps
## Root cause       # X because evidence Y (with file:line)
## Evidence         # logs, bisect result, experiment results
## Fix              # what changed and why it addresses the root cause
## Verification     # failing-then-passing test + full suite output
## Variants         # other places with the same pattern (fixed or ticketed)
```
