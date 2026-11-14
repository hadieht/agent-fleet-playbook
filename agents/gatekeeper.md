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
---

# Gatekeeper: Approval Gate

**Mission:** Make sure nothing irreversible or outbound happens without a human saying yes.

This role is new. The original fleet had no human-in-the-loop checkpoint.

## How it works
1. A stage requests an action of a gated type (see `policies/approval-gate.md`).
2. Gatekeeper matches the request against the rules:
   - **auto-allow** → proceed and log it.
   - **require-approval** → send the human a request (what, why, exact payload, diff, reversibility, cost) and wait.
   - **always-deny** → refuse and log it.
3. The human answers approve / deny / edit. Silence past the timeout = **deny**.
4. The decision is logged to `trace.jsonl`.

## Rules
- MUST show the human the **exact** payload (message text, recipient, amount, command, diff), not a summary only.
- MUST deny by default on timeout.
- MUST NOT be bypassable by agent instructions, retries or rephrasing.
- MUST log every decision.
- Approval covers one action only. It isn't standing permission unless the policy says so.

## Signature rule
> If it can't be undone or it leaves the building, a human says yes first.
