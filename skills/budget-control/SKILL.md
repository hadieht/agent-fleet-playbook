---
name: budget-control
description: Use in any agent loop to enforce step, token, time and spend limits and to wrap up gracefully. Load it in every long-running agent.
---

# Budget control

## Rules
1. Read your budgets from the brief (fall back to `policies/budgets.yaml`).
2. Keep a running count of steps, tokens, wall-clock and spend.
3. At **50%**: check progress against the acceptance criteria. If under half are met, narrow the scope.
4. At **80%**: stop starting new work. Finish what's in progress and write the output with a `## Budget note`.
5. At **100%**: stop immediately and return a partial result.
6. **No-progress rule:** 3 consecutive steps with no new information or artifact → stop and escalate.
7. Never retry the same failing action more than twice without changing something.

## Budget note format
```
## Budget note
Used: steps 34/40, ~41k tokens, 22 min.
Completed: criteria 1, 2, 4. Not completed: 3 (reason).
```
