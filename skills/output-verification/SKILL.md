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

## Rules
- Report only. Never edit the output.
- `could-not-verify` beats a guessed `pass`.
- Nondeterministic outputs: run twice and compare the structure, not exact bytes.
