---
name: approval-gating
description: Use whenever an agent wants to take an outbound or irreversible action (send, post, pay, delete, push, deploy, change permissions). Explains how to request approval from the Gatekeeper. Load it in every agent that can propose such actions.
---

# Approval gating

## Gated action types
`message.send`, `email.send`, `post.publish`, `payment`, `purchase`, `file.delete`, `db.write:prod`, `git.push`, `deploy`, `permissions.change`, `credential.use:new-scope`, `calendar.invite`. The full policy is in `policies/approval-gate.md`.

## Procedure
1. Don't perform the action. Write an **approval request** instead:
```yaml
action: email.send
why: "User asked to send the vendor shortlist to procurement"
payload:            # EXACT content, not a summary
  to: procurement@example.com
  subject: "..."
  body: "..."
reversible: false
cost: 0
risk: "Wrong recipient would leak pricing data"
requested_by: <agent>/<stage>
```
2. Submit it to the `approve` capability and wait.
3. `approved` → perform **exactly** the approved payload, nothing more. `denied` or timeout → stop and report.
4. If the payload must change after approval, request approval again.

## Rules
- Never split a gated action into smaller ungated pieces to avoid approval.
- Never treat an earlier approval as covering a new action.
