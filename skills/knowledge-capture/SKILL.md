---
name: knowledge-capture
description: Use to decide what from a finished task becomes long-term memory and to write it into the vault without duplicates. Only the remember capability uses this skill.
---

# Knowledge capture

## Durable vs scratch
| Durable (keep) | Scratch (skip) |
|---|---|
| Decisions + rationale + tripwire | Drafts, intermediate attempts |
| Verified facts likely to be reused | Raw search results |
| User preferences and constraints | One-off chatter |
| Project state and milestones | Unverified claims (unless flagged) |
| Lessons from failures | Anything containing secrets |

## Procedure
1. For each proposal, decide durable or scratch, and note the reason.
2. `vault.search` by title, aliases and key terms.
3. Match found → **update** (append, refresh `updated`, add the source). Two near-duplicates → **merge**, and mark one `superseded_by`.
4. No match → **create** in the right folder: `Research/ Decisions/ Projects/ People/ Journal/ Lessons/`.
5. Add `[[wikilinks]]` to 1–5 related notes.

## Note template
```markdown
---
type: decision|research|project|person|journal|lesson
status: verified|unverified|superseded
sources: [<url or workspace path>]
task_id: <id>
created: YYYY-MM-DD
updated: YYYY-MM-DD
superseded_by: null
---
# Title
Summary in 1–3 sentences.
## Details
## Related
- [[...]]
```

## Rules
- No source → don't write it.
- Never delete; supersede.
- Never store secrets or credentials.
