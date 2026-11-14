---
name: synthesis
description: Use at the end of a multi-stage task to merge verified stage outputs into one coherent final answer. Don't use to summarize a single document (use report-writing).
---

# Synthesis

## Procedure
1. Re-read `00-request.md`. The answer must address **that**, not the plan.
2. Re-read every `stages/*/output.md` and `verify.md`. Work from the files, not from memory of them.
3. Build a claim ledger: claim → stage → verify status.
4. Reconcile conflicts explicitly: say which source wins and why, or present both.
5. Drop claims that failed verification. Carry `could-not-verify` claims into the open-items section.
6. If a critique exists, address every `deal-breaker` and `significant` item: fixed, accepted risk, or overridden with a reason.
7. Write `final.md`: answer first, then evidence, confidence and open items.

## Output format
```
## Answer
## How we got there
## Confidence
## Unverified / open
## Next steps (optional)
```

## Checklist
- [ ] The first paragraph directly answers the user's question
- [ ] No claim that failed verification
- [ ] Every critic deal-breaker addressed
- [ ] Open items listed honestly
