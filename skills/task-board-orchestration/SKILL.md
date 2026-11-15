---
name: task-board-orchestration
description: Use when the planner routes work through a task board (kanban cards, queues, tickets) to other agents, relays their results, handles blocked or timed-out cards, or reports status. Covers dependency links without deadlock, multi-phase chains, budget-exhausted cards and honest status reports. Don't use inside a worker stage (use task-board-worker).
---

# Task-board orchestration

## Iron law
> **A worker's completion summary is a claim, not a fact.** Before you relay it, re-read the full card (summary, metadata, comments) and check the live state (files, git log, gates) for anything the user will act on.

## 1. Create cards that can't deadlock
- **Never make yourself the dependency parent of a card you are waiting on.** The child only becomes ready when all its parents are done, and you can't finish while waiting. Create it unlinked and wait for its completion event, or end your turn and resume when the result arrives.
- Use parent → child links only for chains that flow through *other* agents (research → strategize → critique).
- If a child must start *after* your own analysis, write that analysis into the child's brief first, then create the child.
- **Out-of-order start:** some dispatchers start cards the moment they're created, before your links land. For a serial chain created in one batch: create → immediately block the later cards with reason "dependency: wait for predecessor" → link A→B→C → unblock. They then wait, parent-gated, and promote in order.

## 2. Brief every card for a stranger
Follow `brief-writing`, plus:
- Say **apply** or **advise**. "Provide instructions" returns instructions, and the user has to ask again.
- For changes to live systems the user owns, list the exact approved actions, require a backup before any edit, and a check that shows the change took effect.
- Include known facts: hosts, paths, earlier findings and card ids. A one-line brief makes the worker rediscover everything and return generic advice.

## 3. Multi-phase builds of one repository
1. **Green baseline first.** Do the scaffold yourself (or as card 1): skeleton, a build and tests that pass, first commit. Every later phase starts from green.
2. Create the **whole serial chain up front**; each card's parent is the previous card, so phases promote themselves.
3. **A progress file is the convention log.** Every brief opens with "read `PROGRESS.md` (all sections) first", and every phase appends its own section (decisions, versions, hooks for the next phase). Conventions travel without re-briefing.
4. **Size each card for about one worker run.** If a phase is bigger, the brief mandates: commit after each item; when the budget runs low, stop at a clean committed state, write what remains in the progress file, and block with an exact list.
5. Verify at every phase boundary yourself (build with incremental caching off, full tests, plus the specific acceptance checks), and only then let the next phase start or publish.

## 4. Relay results
- Notifications truncate. Read the full card (`runs[-1].summary` and metadata) before answering.
- Report only what the worker actually found or did. Never fill gaps with generic how-to text; the worker's specific facts (secondary errors, wrong hosts tried) are usually the useful part.
- Say whether the worker **changed** anything or only **advised**.
- A worker may finish part of the brief and spawn its own follow-up card. Name the missing part and report the feature as not usable yet.

## 5. Blocked, timed out, or budget-exhausted cards
| Situation | Do |
|---|---|
| Blocked on missing input | Resolve it, write the decision as a **comment** (comments outlive worker sessions), then unblock |
| Budget-exhausted (often labeled as a capability block though nothing is missing) | Verify the on-disk state yourself, answer the worker's open questions **against the source code** (not docs or your own brief), post a numbered resume brief as a comment, unblock |
| In-flight work is internally inconsistent (interfaces and implementations disagree) | Save it on a salvage branch, reset to the last coherent tested commit, re-verify, re-scope into smaller serial cards |
| "Timed out, will retry" | Don't recreate the card. Check for surviving processes and half-written files before touching the tree |
| Timeout notice for a card that is already `done`, or that predates your unblock | Stale or late duplicate. Say so and do nothing |
| Deliverable committed and independently verified, but the worker keeps hanging on its own final check | Force-complete with a summary saying so. Only for work you confirmed green |

Resume brief format: **what is real and committed (don't redo)** · **what remains, in order** · **decisions made** · **budget discipline** (commit per item, stop clean, block precisely). Details: [reference/recovery-playbook.md](reference/recovery-playbook.md).

## 6. Decisions made while a worker runs
- Post owner decisions as a comment immediately. A running worker may miss it, but the next run's context includes the whole thread.
- If a decision widens permissions, write the exact limits in the comment.
- Review committed code read-only while the worker runs and post a numbered fix list. That's cheaper than a review cycle after completion.
- If a worker's sandbox refused an action on a live system, don't silently do it yourself. Ask the user; record a "no" on the card and state the risk.

## 7. Report status
- Ground it in live data: the board, the active card, the progress file and `git log`.
- Group it: **done (committed and verified)** · **in progress** · **remaining (in order)** · **deferred** · **decisions the user still owes**. Keep that last list at the end of every status reply until each item is answered.
- For a short or garbled user message, act on the most likely reading and say in one line how you read it. Don't block on a form the user may cancel.

## Red flags
- Your own card is a parent of a card you are waiting on.
- You are about to relay a summary you haven't read in full.
- You are recreating a card the dispatcher already retries.
- A "N tests green" claim you haven't re-run before publishing.

## Checklist
- [ ] No self-deadlocking links; serial chains block-link-unblocked
- [ ] Every brief says apply/advise, names approved actions, points at the progress file
- [ ] Each card sized for one run, with the stop-clean rule
- [ ] Results relayed from the full card, with changed-vs-advised stated
- [ ] Status grouped, with owed decisions listed last
