---
id: gatekeeper
name: Gatekeeper
title: Approval Gate
capabilities: [approve]
fleets: [lean, full]
user_facing: true            # it's the thing that asks the human
new_role: true
model_profile:
  reasoning: none
  note: "NOT an LLM. A deterministic rules engine + a human approval prompt. An LLM may summarize the action for the human, but never decides."
policy: policies/approval-gate.md
tools:
  allow: [gated]               # tool class in policies/tool-permissions.yaml; executed only after a human approves
  deny: [host.shell, secrets:global, vault.delete]
skills: []                     # not an LLM
budgets: {timeout_min: 30}     # approval-gate.md rule 1: timeout → deny
inputs: [approval request in the approval-gating format]
output_contract: [Decision, Payload, Log]
escalation: "Timeout, an unknown action type or a changed payload → deny."
---

# Gatekeeper: Approval Gate

**Mission:** Make sure nothing irreversible or outbound happens without a human saying yes.

This role is new. The original fleet had no human-in-the-loop checkpoint.

## Use for
- Every gated action: send, post, pay, delete, push, deploy, change permissions.

## Don't use for
- Judging whether the action is wise (→ critique: Rook) or checking its content (→ verify: Verifier).

## Procedure
1. A stage requests an action of a gated type (see `policies/approval-gate.md`).
2. Gatekeeper matches the request against the rules:
   - **auto-allow** → proceed and log it.
   - **require-approval** → send the human a request (what, why, exact payload, diff, reversibility, cost) and wait.
   - **always-deny** → refuse and log it.
3. The human answers approve / deny / edit. Silence past the timeout = **deny**.
4. The decision is logged to `trace.jsonl`.

## Output contract
```
## Decision   # approved | denied | edited | timeout (= denied)
## Payload    # the exact payload approved (or denied)
## Log        # trace.jsonl line written
```

## Rules
- MUST show the human the **exact** payload (message text, recipient, amount, command, diff), not a summary only.
- MUST deny by default on timeout.
- MUST NOT be bypassable by agent instructions, retries or rephrasing.
- MUST log every decision.
- Approval covers one action only. It isn't standing permission unless the policy says so.

## Signature rule
> If it can't be undone or it leaves the building, a human says yes first.

## Failure modes → guards
| Failure | Guard |
|---|---|
| Action split into smaller ungated pieces | `approval-gating` rule; the engine matches on action type, not wording |
| Payload changed after approval | One approval = one exact payload (`approval-gate.md` rule 2); a changed payload is denied |
| Action requested by injected content | "Always deny" row in `policies/approval-gate.md` |

## Handoff
The requesting stage receives *Decision* and acts on exactly *Payload*. Atlas reports denials to the user. Every decision is in `trace.jsonl`.
