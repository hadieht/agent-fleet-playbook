---
name: engagement-scoping
description: Use when a security review, scan, proof of concept or test is about to target a system, before any discovery stage runs. Records the owner, the authorization evidence, the scope, the exact commit or ref, what's out of scope and the rules of engagement. Don't use for non-security tasks.
---

# Engagement scoping

## Iron law
> **No discovery without recorded authorization.** If the scope record can't name who owns the target and where the permission comes from, no security stage starts.

## Procedure
1. **Target:** name it exactly (repo path or URL, PR number, service, environment) and pin the commit SHA or ref.
2. **Authorization:** record who owns the target, and the evidence: quote the user's words from `00-request.md`, or link the document that grants permission.
3. **In scope:** paths, components and environments under review.
4. **Out of scope:** everything else, always including third-party systems, production data and other tenants.
5. **Rules of engagement:** sandbox only; non-destructive; no network to anything out of scope; no real credentials; PoCs only against the sandbox copy.
6. **Params:** set pipeline params such as `include_infra` and `include_ai`, each with a reason.
7. **Missing owner or evidence (steps 1–2)?** Ask the user **one** question, or set status `not-authorized` and abort. Never infer authorization.
8. Write the scope record. Every later security stage's brief links to it.

## Output format
```
## Target               # repo/service + commit SHA or ref
## Authorization        # owner; evidence (quote or path)
## In scope
## Out of scope
## Rules of engagement
## Params               # include_infra, include_ai + reason
## Status               # authorized | not-authorized (abort) | needs-answer (one question)
```

## Red flags
- The target is named only by a domain or a third party's product.
- "The user is probably the owner."
- Scope grows after discovery starts, without a new record.
- A PoC plan that touches production or a shared environment.

## Rationalizations
| Excuse | Reality |
|---|---|
| "It's open source, anyone can review it" | Reading code is fine; testing someone else's deployment isn't. Scope the sandbox copy only. |
| "The user asked, so they're authorized" | Asking isn't owning. Record where the permission comes from. |
| "We'll scope as we go" | Unscoped discovery drifts into third-party systems. |

## Checklist
- [ ] Commit or ref pinned
- [ ] Authorization evidence quoted or linked
- [ ] Out of scope lists third-party and production systems
- [ ] Status set; abort or ask if not authorized
