---
name: output-verification
description: Use to independently check a stage's output against its brief's acceptance criteria by re-running commands, recomputing numbers and validating files. For citations also load citation-verification. Don't use to fix the work.
---

# Output verification

## Procedure
1. Read `brief.md` (acceptance criteria) and `output.md` (claims). List every checkable claim.
2. For each, pick the most deterministic check available:
   - **Command claims:** re-run from `run.log` in a **clean** sandbox and diff the output.
   - **Test claims:** run the test suite; diff test files against the baseline to catch weakened tests.
   - **Numeric claims:** re-run the model script, then recompute one key number by an independent method.
   - **File claims:** confirm they exist, parse (JSON/YAML/code), and match the contract.
   - **Citation claims:** follow `citation-verification`.
   - **Contract:** all required output sections present.
3. Record each check: what, how (exact command/URL), result, evidence.
4. Overall: `pass` (all pass), `partial` (non-critical failures or could-not-verify), `fail` (any acceptance criterion fails).

## Output format (`verify.md`)
```
| # | claim/criterion | check | result | evidence |
## Overall
## Notes
```

## Re-review rounds
When the same work comes back after a fail, lead with a different lens each round; repeating round 1's lens mostly re-finds round 1's findings.

| Round | Lead lens | How |
|---|---|---|
| 1 | Artifact | Read the diff or deliverable **cold**, before the producer's summary; then compare and investigate every mismatch |
| 2 | Execution | Run it yourself: build, tests, the reported behavior |
| 3+ | Contract | Re-read the original brief and acceptance criteria; confirm every earlier requested change actually landed and nothing that passed before regressed |

Parallel reviewers: give each a different lens (diff-only, full-context, run-it) rather than identical briefs, which produce correlated verdicts.

Each result is exactly one of: **pass** · **fail with numbered, reproducible findings** (where, how it reproduces, why it violates the brief, the minimum fix) · **escalate** (needs a human decision or an external prerequisite). Don't block on style preferences when behavior and repo standards are met.

## Rules
- Report only. Never edit the output.
- `could-not-verify` beats a guessed `pass`.
- Nondeterministic outputs: run twice and compare the structure, not exact bytes.
- A full suite passing doesn't prove each test passes alone, or the reverse. Re-run tracked tests in isolation too.
- Check that tests assert behavior, not snapshots of source text or constants.
