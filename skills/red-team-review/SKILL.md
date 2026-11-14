---
name: red-team-review
description: Use to stress-test a plan, recommendation, design or conclusion before it becomes final. Produces severity-ranked weaknesses with concrete scenarios and a proceed/don't verdict. Don't use to rewrite or improve the work.
---

# Red-team review

## Procedure
1. **Assumptions:** list what must be true for the plan to work. For each, is it verified (cite the stage) or unverified? What happens if it's false?
2. **Logic attacks:** circular evidence, unstated consequences, deferred deal-breakers, survivorship and selection bias, confusing correlation with causation.
3. **Plan attacks:** failure modes, scale (10× load or cost), adversarial input, dependency failure, reversibility, timing, people and process.
4. **Severity** for each weakness:
   - `deal-breaker`: plan fails or causes serious harm if true; blocks the pipeline.
   - `significant`: materially worse outcome; needs a change or explicit acceptance.
   - `minor`: worth noting; 3 max.
5. **Steelman** the strongest opposing view once.
6. **What survives:** name the parts that hold up.
7. **Verdict:** `proceed` | `proceed-with-changes` (list) | `dont-proceed`.

## Rules
- Every weakness has a **concrete scenario**: "If X happens, then Y, because Z."
- Critique the decision and evidence, not writing style.
- Don't rewrite the plan.
- Max 2 rounds per task.
