---
name: task-decomposition
description: Use when a request at Level 1–3 must be split into stages with capabilities, dependencies and parallel waves. Don't use for Level 0 requests or inside worker stages.
---

# Task decomposition

## Procedure
1. List the **deliverables** the final answer needs (facts, numbers, artifacts, a decision, a document).
2. For each deliverable, choose one capability: `research | monitor | build | compute | strategize | critique | verify | remember | write | approve`.
3. Draw dependencies: a stage depends on another **only** if it needs that stage's output.
4. Group the stages into **waves**. Everything in a wave runs in parallel, with at most 3 workers at once.
5. Insert gates:
   - `verify` after any stage that produces code, numbers or citations.
   - `critique` before final if Level 3 or irreversible.
   - `approve` before any outbound or irreversible action.
6. Add the final `plan` synthesis stage and a `remember` stage.
7. Set the budget per stage (inherit pipeline defaults, lower where possible).
8. Sanity-check: is any stage doing two jobs? Is any wave serial for no reason?

## Output format (in `01-plan.md`)
```
## Stages
| id | capability | depends_on | wave | outputs | gate |
## Budget
## Assumptions
```

## Checklist
- [ ] Every stage has exactly one capability
- [ ] No dependency that isn't a real data dependency
- [ ] Verify gate on code, numbers and citations
- [ ] Critique and approve gates where required
- [ ] Ends in one synthesis stage
