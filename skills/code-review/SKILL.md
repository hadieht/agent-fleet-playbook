---
name: code-review
description: Use to review a diff, pull request or set of changed files before merge. Checks correctness, design, readability, tests, security, performance and operability, and reports severity-ranked findings with concrete fixes. Don't use to rewrite the code yourself; for a dedicated security audit use secure-code-review.
---

# Code review

## Iron law
> **Review the change against its intent, and back every finding with a concrete scenario.** "This looks off" isn't a finding.

## Procedure
1. **Understand intent:** read the brief, ticket or PR description. What should this change do? What should it *not* change?
2. **Get the full picture:** the diff, *plus* the surrounding code it touches, callers of changed functions, and tests. Diffs hide context.
3. **Build and run** if you can: tests, linters, type checker. Failures are findings.
4. **Review by axis**, in this order (most important first):

| # | Axis | Questions |
|---|---|---|
| 1 | **Correctness** | Does it do what the intent says? Edge cases: empty, null, zero, max, duplicates, unicode, time zones, concurrency? Error paths? Off-by-one? |
| 2 | **Security** | Untrusted input reaching queries, commands, paths, HTML, deserializers? Authz on every new endpoint? Secrets? (Deep dive: `secure-code-review`) |
| 3 | **Data and compatibility** | Migrations safe and reversible? API or contract changes backward compatible? Serialized formats? |
| 4 | **Tests** | Do the tests fail without the change? Do they cover the edge and error cases? Are they deterministic? |
| 5 | **Design** | Right place for this logic? New coupling? Abstractions earning their cost? Consistent with existing patterns? |
| 6 | **Readability** | Names, function size, comments explaining *why* (skill `clean-code`) |
| 7 | **Performance** | N+1 queries, unbounded loops or allocations, missing pagination, sync I/O on hot paths, missing indexes |
| 8 | **Operability** | Logs with context (no secrets/PII), metrics, error messages, feature flags, config, rollback path |

5. **Rank** each finding:
   - `blocker`: incorrect, insecure, data loss, breaks compatibility. Must fix.
   - `major`: likely bug, missing tests for risky logic, significant design problem. Should fix.
   - `minor`: readability, small improvements. Optional.
   - `nit`: style. At most 3, and only if no linter covers it.
6. **Write each finding** with location, problem, scenario and a suggested fix.
7. **Note what's good.** Name the solid parts so they're kept.

## Finding format
```
[blocker] src/Orders/RefundService.cs:88
Problem: refund amount isn't checked against the original charge.
Scenario: a client sends amount=1e6 for a $10 order → refund over-pays.
Fix: reject when amount > order.CapturedAmount - order.RefundedAmount; add a test.
```

## Output format
```
## Summary          # 2–3 sentences: what the change does, overall assessment
## Verdict          # approve | approve-with-changes | request-changes
## Findings         # ranked blocker → nit, format above
## Tests run        # commands + results
## Good             # what to keep
```

## Rules
- Review the code, not the author. Use neutral, specific language.
- Distinguish facts ("this throws on empty input; see test X") from opinions ("I'd prefer…").
- Don't block on style the linter doesn't enforce.
- Large diffs (over ~400 lines of logic): say so, and suggest splitting; review the riskiest parts first.
- Don't approve anything you didn't understand. Ask.

## Red flags in a diff
- Tests changed in the same commit as the logic they test, with expected values edited.
- New `catch` blocks that swallow errors; new retries without limits.
- `TODO`, `HACK`, `FIXME`, commented-out code, debug prints.
- New dependencies (check them with skill `supply-chain-security`).
- Changes to auth, crypto, payments, permissions or migrations. These need extra scrutiny.
