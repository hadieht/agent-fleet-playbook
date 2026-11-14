# Approval gate policy

Enforced by **Gatekeeper**, a deterministic rules engine plus a human. It's never an LLM alone.

## Rule table

| Action | Default | Notes |
|---|---|---|
| Read workspace, vault, web | auto-allow | logged |
| Write inside own stage folder | auto-allow | |
| Vault write (Librarian) | auto-allow | logged; no deletes |
| Sandbox code execution | auto-allow | no host access |
| `message.send`, `email.send`, `calendar.invite` | **require approval** | show the exact recipient and text |
| `post.publish` (social, blog, public issue) | **require approval** | show the exact text |
| `git.push`, merge, `deploy` | **require approval** | show the diff, target and rollback plan |
| `file.delete` outside sandbox, `db.write:prod` | **require approval** | show what's affected and whether a backup exists |
| `payment`, `purchase`, subscription change | **require approval** | show amount, payee, recurrence |
| `permissions.change`, new credential scope | **require approval** | |
| `host.shell`, global secrets, `vault.delete` | **always deny** | |
| Anything requested from content found in a web page, email or file | **always deny** | possible prompt injection |

## Approval request (what the human sees)
```
ACTION     email.send
WHY        User asked to send vendor shortlist to procurement (task t-0142)
PAYLOAD    to: … / subject: … / body: (full text)
REVERSIBLE no
COST       0
RISK       wrong recipient → pricing leak
[approve] [deny] [edit]
```

## Rules
1. Timeout → **deny** (default 30 min, configurable).
2. One approval = one action with one exact payload. A changed payload needs a new approval.
3. Standing approvals (e.g. "always allow pushing to branch `drafts/*`") must be written into this file by a human, with a date and an expiry.
4. Every decision is logged to the task's `trace.jsonl`.

## Standing approvals
| Rule | Granted by | Date | Expires |
|---|---|---|---|
| *(none)* | | | |
