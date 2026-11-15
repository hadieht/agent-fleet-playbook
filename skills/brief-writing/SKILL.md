---
name: brief-writing
description: Use whenever you hand work to another agent. Produces a self-contained brief so a worker that starts with zero context can succeed. Don't use for messages to the human user.
---

# Brief writing

The worker knows **nothing** except the brief and the files it points to.

## Procedure
1. Fill every section of `templates/task-brief.md`:
   1. **Goal:** one sentence describing what done looks like.
   2. **Context:** why it matters; quote the user's original words from `00-request.md`.
   3. **Inputs:** exact workspace paths, URLs and data. No "the file we discussed".
   4. **Constraints:** scope, forbidden actions, deadline, budget.
   5. **Output contract:** exact sections + output path `stages/<id>/output.md`.
   6. **Acceptance criteria:** numbered, each checkable by the Verifier.
   7. **Escalate if:** when to stop and return instead of guessing.
   - Under **Constraints**, state the **mode**: `apply` or `advise`. For changes to live systems, list the exact approved actions, require a backup first and a check that shows the change took effect.
   - Under **Inputs**, list **known facts**: hosts, paths, earlier findings and task ids, so the worker doesn't rediscover them. For multi-phase work: "read the progress file first, append your section".
2. Read it as a stranger would: could someone with no history do this correctly?
3. Remove anything the worker doesn't need. Noise lowers quality too.

## Bad vs good
- Bad: "Research data pipeline vendors."
- Good: "Find 3–5 managed data-pipeline vendors that support Postgres CDC → S3, with list price for ~50 GB/day. Output: table vendor | CDC support (quote+URL) | price (quote+URL) | date checked. Acceptance: every cell sourced; ≥3 vendors. Escalate if pricing is not public for ≥2 vendors."

## Checklist
- [ ] All 7 sections present
- [ ] Mode (apply / advise) stated; approved live-system actions listed
- [ ] Every input is a concrete path or URL
- [ ] Acceptance criteria are testable
- [ ] Escalation condition stated
