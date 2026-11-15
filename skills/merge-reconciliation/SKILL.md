---
name: merge-reconciliation
description: Use when two agents' branches or worktrees conflict and neither author should resolve it. A neutral third party classifies every conflicted hunk by the stated intents, resolves it, verifies both intents survive and reports each decision. Don't use for conflicts inside one agent's own work or for lockfiles and generated files (regenerate those).
---

# Merge reconciliation

Agents resolving a conflict against a peer's work tend to overwrite the peer or abandon their own change. They lack the other side's context and favor their own. Use a reconciler that wrote neither side.

## Iron law
> **Never favor a side, and never bury a design call.** Every "pick one" decision appears in the hand-back so a human can veto it.

## Setup
- Run as a fresh worker instance that produced **neither** branch. On a task board, create one reconciliation card with **both** conflicting cards as parents, so both completion summaries reach your context.
- Inputs: the repo path, both branch names, both sides' stated intents (completion summaries or PR bodies; commit messages only as a last resort), and the build/test command.

## Procedure
1. **Gather:** `git status`, `git merge-base A B`, then `git log --oneline base..A` / `base..B` and `git diff base..<side> -- <file>` for every conflicted file. Write one sentence of intent per side before editing anything.
2. **Classify every hunk** (per hunk, not per file; split a hunk if it holds several decisions):

   | Class | Meaning | Resolution |
   |---|---|---|
   | disjoint-intent | Different goals that can coexist | Combine both |
   | same-question-different-answer | Both answered one design question differently | Pick **one** by the stated intents; surface it |
   | superseded | One side's premise no longer holds after the other's change | Keep the survivor; note why |

3. **Resolve** only inside conflict regions: no formatting, renames or drive-by fixes. Never split the difference into a hybrid neither side designed. If the intents genuinely tie, escalate instead of guessing.
4. **Verify:** no conflict markers remain; the build and tests pass; **both** intents are observable in the merged behavior. Then commit the merge.
5. **Hand back** one line per hunk: `file:lines — class — side(s) kept — rationale`, and for every design pick, the question and the chosen answer.

## Red flags
- You were spawned by one of the two authors. Say so, and weigh the other side deliberately.
- A whole file classified as one class.
- Edits outside conflict markers.
- The **same file** conflicts again in a later round. That's a hotspot: flag it to the planner (`hotspot: <path> — <reason>`) so the work gets decomposed, instead of reconciling it again and again.

## Checklist
- [ ] Both intents written down before editing
- [ ] Every hunk classified with a rationale
- [ ] No markers left; build and tests green; both intents present
- [ ] Hand-back lists every hunk and every design pick
