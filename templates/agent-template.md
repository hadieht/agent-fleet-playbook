---
id: <lowercase-id>
name: <Name>
title: <Role title>
capabilities: [<capability>]
fleets: [lean, full]
user_facing: false
model_profile: {reasoning: <low|medium|high|highest>, context: <small|medium|large>, tool_use: <required|optional|none>, speed: <fast|medium|slow-ok>}
tools:
  allow: []          # least privilege, justify each one
  deny: [secrets, message.send, file.delete]
skills: []         # budget-control, task-board-worker and approval-gating are global (fleet.config.yaml); don't list them
budgets: {max_steps: 40, max_wallclock_min: 30}
inputs: []
output_contract: []
escalation: "<when to stop and return instead of guessing>"
---

# <Name>: <Role title>

**Mission:** <one sentence, no "and">

## Use for
-

## Don't use for
-

## Procedure
1.

## Output contract
```
## ...
```

## Rules
- MUST ...
- MUST NOT ...

## Signature rule
> <the one rule that defines this role>

## Failure modes → guards
| Failure | Guard |
|---|---|
| | |

## Handoff
<who consumes the output and what they need>
