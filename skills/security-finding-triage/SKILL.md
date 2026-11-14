---
name: security-finding-triage
description: Use to validate a candidate security finding (from a scanner, a code review, a bug report or another agent) before it's reported or fixed. Checks reachability, attacker control, preconditions and real impact; rejects false positives; scores severity with CVSS v4.0; runs variant analysis. Don't use to discover new issues from scratch (use secure-code-review).
---

# Security finding triage

## Iron law
> **A finding is real only when you can state who the attacker is, what they control, the path to the sink, and the concrete impact.** Anything less is labeled `unconfirmed`, not reported as a vulnerability.

## Gates (a candidate must pass all to be reported as confirmed)

| # | Gate | Question | Fail → |
|---|---|---|---|
| 1 | **Exists** | Is the code path real and present in the reviewed version (not dead code, tests, examples, vendored code that isn't shipped)? | Reject |
| 2 | **Reachable** | Can an entry point reach the sink? Trace every hop with file:line | Reject or `unconfirmed` |
| 3 | **Attacker-controlled** | Does attacker input reach the sink *unsanitized for this context*? Check validation, type constraints, encoding and framework protections along the path | Reject |
| 4 | **Preconditions** | What does the attacker need (auth level, role, user interaction, specific config, race window)? Are those realistic? | Downgrade |
| 5 | **Impact** | What concretely happens: data read or written, code execution, privilege gain, DoS? To whom, and how much? | Downgrade or reject |
| 6 | **Not mitigated elsewhere** | WAF, gateway authz, DB permissions, sandboxing, CSP? (Note them; defense in depth doesn't make a bug go away, but it lowers severity) | Downgrade |
| 7 | **Reproducible** (when feasible) | A test or PoC in an **authorized sandbox** demonstrates it | Keep as `likely` if not reproducible |

## Common false-positive patterns
- Scanner flags SQL concatenation, but the value is a constant, an enum or an allow-listed identifier.
- "XSS" in a context the framework auto-encodes, with no raw-HTML opt-out on the path.
- Hard-coded "secret" that's a test fixture, a public key or a placeholder (still check the git history).
- "Weak hash" used for a non-security purpose (cache keys, ETags), not passwords or signatures.
- Path traversal where the path is generated server-side.
- Vulnerable dependency version where the vulnerable function is never called and isn't reachable. Report it as **low / update hygiene**, not as an exploitable bug, unless reachability is unknown.

## Severity: CVSS v4.0 base metrics
- **Exploitability:** `AV` Attack Vector (N network / A adjacent / L local / P physical) · `AC` Attack Complexity (L/H) · `AT` Attack Requirements (N/P) · `PR` Privileges Required (N/L/H) · `UI` User Interaction (N/P passive / A active)
- **Impact on the vulnerable system:** `VC` / `VI` / `VA`: confidentiality, integrity, availability (H/L/N)
- **Impact on subsequent systems:** `SC` / `SI` / `SA` (H/L/N)
- Vector example: `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N`
- Compute the score with the official FIRST calculator (first.org/cvss/calculator/4.0) or a vetted library. Never estimate the number by intuition.
- Rating bands: None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 · Critical 9.0–10.0
- Add **context** beyond CVSS: data sensitivity, number of affected users, exploit availability, internet exposure.

## Variant analysis (for every confirmed finding)
1. Abstract the bug into a pattern: "query by ID without tenant filter", "`Path.Combine` with request data", "`FromSqlRaw` with interpolation".
2. Search the codebase for the pattern: grep or ripgrep first, then a Semgrep or CodeQL rule if it recurs.
3. Triage each hit through the same gates.
4. Recommend a **systemic fix** (shared helper, analyzer rule, base-class check, lint rule) when there are 3 or more variants.

## Output format
```
## Candidate         # source (tool/rule/reviewer), location
## Gates             # 1–7 with pass/fail + evidence (file:line, test name)
## Verdict           # confirmed | likely | unconfirmed | false-positive (+ reason)
## Severity          # CVSS v4.0 vector + score + contextual notes
## Variants          # pattern, search used, hits with verdicts
## Fix guidance      # specific fix + regression test + systemic prevention
```

## Rules
- PoCs run only in an authorized sandbox against code the requester owns, and must be non-destructive.
- Never "fix" a finding during triage. Report it.
- When unsure, mark it `unconfirmed` and state what evidence would settle it.
