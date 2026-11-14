---
name: routing-and-triage
description: Use at the start of every incoming request to decide how much machinery it needs (Level 0 direct answer, Level 1 single specialist, Level 2 parallel fan-out, Level 3 full pipeline with critique and approval). Don't use inside worker stages.
---

# Routing and triage

## Procedure
1. Restate the request as one goal sentence. Quote the user's key words.
2. Answer these five questions (yes/no):
   - A. Can I answer correctly with no tools, or one cheap lookup?
   - B. Does it need exactly one capability (research, build, compute...)?
   - C. Does it split into 2–3 parts that don't need each other's output?
   - D. Is it high-stakes: money, security, legal, health, deletion, publishing, messaging others, or a decision the user will act on?
   - E. Is it ambiguous in a way that would change the plan?
3. Decide:
   - E = yes → ask the user **one** focused question first. Don't fan out.
   - A = yes and D = no → **Level 0**.
   - B = yes and D = no → **Level 1**.
   - C = yes and D = no → **Level 2**.
   - D = yes → **Level 3** (pick a pipeline from `pipelines/`).
4. If unsure between two levels, pick the **lower** one and note when to escalate.
5. Honor user overrides: "quick" → L0, "full analysis" or "be thorough" → L3.
6. Write the decision into `01-plan.md`.

## Output format
```
## Level: <0|1|2|3>
## Why: <one or two sentences referencing A–E>
## Pipeline: <id or "ad-hoc">
## Escalate if: <condition>
```

## Checklist
- [ ] Level stated with reason
- [ ] High-stakes check (D) explicitly considered
- [ ] Not over-orchestrated: could a lower level do it?
