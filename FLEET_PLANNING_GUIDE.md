# Fleet Planning Guide

How to plan, build and run a fleet of AI agents and the pipelines that connect them.

This guide doesn't depend on any runtime. Agents, skills, pipelines and fleets are written as Markdown and YAML, so you can wire them into Hermes, Claude Code, LangGraph, CrewAI, a custom loop or anything else.

> **The rule to remember:** an agent is worth adding only if it **measurably** improves quality, cost, speed or safety compared with a single good agent. Everything else in this guide follows from that.

---

## Contents

1. [Core concepts](#1-core-concepts)
2. [When to use a fleet (and when not to)](#2-when-to-use-a-fleet-and-when-not-to)
3. [Capabilities: the layer that makes fleets switchable](#3-capabilities-the-layer-that-makes-fleets-switchable)
4. [The two fleets: lean and full](#4-the-two-fleets-lean-and-full)
5. [Designing an agent](#5-designing-an-agent)
6. [Designing a skill](#6-designing-a-skill)
7. [Designing a pipeline](#7-designing-a-pipeline)
8. [Routing levels](#8-routing-levels)
9. [Briefs and the shared workspace](#9-briefs-and-the-shared-workspace)
10. [Verification](#10-verification)
11. [Critique (red team)](#11-critique-red-team)
12. [Memory](#12-memory)
13. [Security](#13-security)
14. [Budgets and termination](#14-budgets-and-termination)
15. [Failure handling](#15-failure-handling)
16. [Observability](#16-observability)
17. [Evaluation](#17-evaluation)
18. [Anti-patterns](#18-anti-patterns)
19. [Checklists](#19-checklists)
20. [Glossary](#20-glossary)

---

## 1. Core concepts

| Concept | What it is | Where it lives |
|---|---|---|
| **Agent** | One model instance with a persona, a mission, allowed tools, skills and an output contract. It starts fresh on every task. | `agents/<id>.md` |
| **Skill** | A reusable procedure (instructions + checklist + output format) that any agent can load. Skills hold the *how*; agents hold the *who*. | `skills/<name>/SKILL.md` |
| **Capability** | An abstract job such as `research`, `build` or `critique`. Pipelines ask for capabilities, not agents. | `fleets/*.yaml` |
| **Fleet** | A binding of capabilities to agents. Switching fleets changes who does the work without rewriting pipelines. | `fleets/lean.yaml`, `fleets/full.yaml` |
| **Pipeline** | A graph of stages (capability + brief + dependencies + gates) that turns one request into one answer. | `pipelines/*.yaml` |
| **Policy** | Rules every agent must obey: tool permissions, budgets, approvals, security. | `policies/` |
| **Workspace** | A per-task folder that all stages read from and write to, so no detail is lost in handoffs. | `templates/workspace/` |
| **Gate** | A checkpoint a pipeline can't pass without a condition: verification passed, critic approved, human approved. | defined in pipelines |

**Separation of concerns:**

```
agent    = WHO  (persona, judgment, permissions)
skill    = HOW  (procedure, checklist, format)
pipeline = WHEN / IN WHAT ORDER
fleet    = WHICH agent fills each capability
policy   = WHAT IS NEVER ALLOWED
```

Keep these apart. If an agent file starts spelling out step-by-step procedures, move them into a skill. If a pipeline names an agent directly, change it to name a capability.

---

## 2. When to use a fleet (and when not to)

A multi-agent fleet costs more tokens and more time, and adds more ways to fail. It pays off only when at least one of these is true:

| Use a fleet when... | Because... |
|---|---|
| The work splits into **independent** parts that can run **in parallel** | Wall-clock time drops |
| Parts need **different permissions** (e.g. web reading vs. shell) | Least privilege: no single agent holds every power |
| You need an **independent** check (verification, critique) | A model checking its own work shares its own blind spots |
| The context is too large for one agent | Each agent gets a focused slice |
| Some parts are routine and some need deep judgment | You can match model strength to the task |

**Don't** use a fleet when:

- The question can be answered in one step → answer directly (Level 0).
- The steps are tightly coupled and strictly sequential, with each needing the full context of the last → one agent with skills does better.
- You can't yet measure whether the fleet beats a single agent → build the evals first (section 17).

> **Default to fewer agents.** Start with the lean fleet. Add a role only when an eval shows it helps.

---

## 3. Capabilities: the layer that makes fleets switchable

Pipelines never name an agent. They name a **capability**, and the active fleet decides which agent provides it.

| Capability | Meaning | Typical output |
|---|---|---|
| `plan` | Decompose, route, set budgets, reconcile, deliver | Plan + final answer |
| `research` | Establish facts from sources | Cited findings + confidence |
| `monitor` | Detect change against a watchlist over time | Dated signal digest |
| `build` | Write and run code, automation, systems | Working artifact + execution log |
| `compute` | Quantitative modeling, done in code | Numbers + method + sensitivity |
| `strategize` | Frame decisions, compare options | Recommendation + tripwire |
| `critique` | Attack a plan or conclusion | Ranked weaknesses + verdict |
| `verify` | Independently re-check claims and artifacts | Pass/fail per claim |
| `remember` | Write durable knowledge | Notes created/updated/skipped |
| `write` | Turn outputs into human-readable documents | Ready-to-publish text |
| `approve` | Hold irreversible or outbound actions for a human | Approved / denied / pending |

Two fleets ship with this repo (see section 4). To create your own, copy a fleet file and change the bindings.

**Rules**

1. Every capability a pipeline uses must be bound in the active fleet, or the pipeline must refuse to start.
2. One agent may provide several capabilities (lean fleet), and it loads the skills for each one.
3. `verify` and `critique` must **never** be bound to the same agent that produced the work being checked.
4. `approve` must be bound to a non-LLM gate (rules + a human), never to a model alone.

---

## 4. The two fleets: lean and full

### Lean fleet: 6 agents + gate (recommended starting point)

| Agent | Capabilities | Replaces (from the original 10) |
|---|---|---|
| **Atlas** | plan, strategize, write | Atlas, Vega, Muse |
| **Scout** | research, monitor | Cipher, Pulse |
| **Forge** | build, compute | Forge, Quant |
| **Rook** | critique | Rook |
| **Verifier** | verify | *(new)* |
| **Librarian** | remember | Librarian |
| **Gatekeeper** | approve | *(new, non-LLM)* |

**Pros:** fewer handoffs, less context loss, cheaper, easier to debug.
**Cons:** Atlas carries more load, so it needs your strongest model, and its context can grow large.

### Full fleet: 10 specialists + verifier + gate

| Agent | Capability |
|---|---|
| Atlas | plan |
| Cipher | research |
| Pulse | monitor |
| Forge | build |
| Quant | compute |
| Vega | strategize |
| Rook | critique |
| Verifier | verify |
| Librarian | remember |
| Muse | write |
| Gatekeeper | approve |

**Pros:** deeper specialization, smaller prompts per agent, each role can use a cheaper model.
**Cons:** more handoffs, more latency, more cost, and more places to lose context.

### How to choose

| Situation | Fleet |
|---|---|
| Starting out, or no evals yet | Lean |
| Most requests are Level 0–2 | Lean |
| Heavy, frequent research **and** monitoring workloads that justify separate tuning | Full |
| Your evals show a specialist improves quality by more than its cost | Full, or lean + that one specialist |

Switch fleets by changing one line in `fleet.config.yaml` (`active_fleet: lean | full`).

---

## 5. Designing an agent

Use `templates/agent-template.md`. Every agent file has YAML frontmatter (machine-readable) and a Markdown body (instructions).

### 5.1 Required fields

| Field | Rule |
|---|---|
| `id` | lowercase, unique, stable (other files refer to it) |
| `capabilities` | the capabilities it can provide |
| `fleets` | which fleets include it |
| `model_profile` | **requirements**, not model names: reasoning depth, context size, tool use, speed. Pick the model at deploy time. |
| `tools.allow` / `tools.deny` | explicit, least privilege. Anything not in `allow` is denied. |
| `skills` | skills it loads by default |
| `budgets` | max steps, tokens, wall-clock, spend per task |
| `inputs` | what its brief must contain |
| `output_contract` | the exact sections its result must have |
| `escalation` | when it stops and returns to the planner instead of guessing |

### 5.2 Body sections (in this order)

1. **Mission:** one sentence.
2. **Use for / don't use for:** concrete examples on both sides.
3. **Procedure:** numbered steps, or references to skills.
4. **Output contract:** the template it fills.
5. **Rules:** MUST / MUST NOT, each testable.
6. **Signature rule:** the one rule that defines the role.
7. **Failure modes:** how this role usually goes wrong, and the guard against each.
8. **Handoff:** who consumes its output and what they need from it.

### 5.3 Rules for writing agents

- **One mission per agent.** If you need "and" to describe it, check whether it's two agents, or one agent with two skills.
- **Contracts beat personas.** A strict output format reduces hallucination more than a colorful character does. Keep personas to one or two lines.
- **Every rule must be testable.** "Be thorough" isn't a rule. "Each finding has a source URL or file path" is.
- **Say what to do when stuck.** "If you can't verify X, say 'could not verify X' and stop" prevents invented answers.
- **Never give an agent a tool it doesn't need for its mission.** A writer doesn't need a shell. A web reader doesn't need secrets.
- **Treat the model as replaceable.** Nothing in the agent file should depend on one vendor's quirks.

---

## 6. Designing a skill

Skills use the portable `SKILL.md` format: YAML frontmatter with `name` and `description`, then Markdown instructions. The same file works across runtimes that support skills, and in any other runtime it can be pasted into a prompt.

### 6.1 Rules

1. **The description is the trigger.** Write it as "Use when ... / Don't use when ...", because runtimes load skills by matching the description.
2. **Procedure, not philosophy.** Use numbered steps the agent can follow and a checker can audit.
3. **Include a checklist** the agent runs before returning.
4. **Include an output format** with exact headings.
5. **Keep `SKILL.md` under ~200 lines.** Put long reference material in `skills/<name>/reference/` and link it, so it's loaded only when needed (progressive disclosure).
6. **No secrets, no environment-specific paths.** Use placeholders like `{workspace}`.
7. **Make it composable.** A skill shouldn't assume which agent loaded it.

### 6.2 Techniques that make skills hold up under pressure

Agents, like people, take shortcuts when a task feels easy or urgent. The most reliable skills in public collections (e.g. obra/superpowers, Trail of Bits) use these devices:

| Technique | What it looks like | Why it works |
|---|---|---|
| **Iron law** | One bold, non-negotiable rule at the top ("No fix without a root cause") | Gives the agent a single thing it can't trade away |
| **Red flags** | Thoughts or actions that mean "stop, you're off track" ("Let me just try…") | Catches drift *while it happens* |
| **Rationalization table** | Excuse → reality ("Too simple to test" → "Simple code breaks too") | Pre-empts the exact arguments a model uses to skip steps |
| **Gates** | Numbered pass/fail checks before output (e.g. 7 triage gates for security findings) | Turns judgment into a checklist a verifier can audit |
| **Master workflow skill** | One skill routes to specialist skills (`code-build-verify`, `red-team-review`) | The agent loads the right depth without carrying everything at once |
| **Evidence format** | Output templates that require commands, file:line, quotes or vectors | "Done" without evidence becomes visibly incomplete |
| **Three-strike rule** | After 3 failed attempts, stop and escalate | Prevents infinite fix loops and runaway cost |

### 6.3 The skill set in this repo

See `skills/README.md` for the full catalog, which skills each agent loads, and external skill sources.

---

## 7. Designing a pipeline

Use `templates/pipeline-template.yaml`. A pipeline is a directed acyclic graph (DAG) of stages.

### 7.1 Stage fields

| Field | Meaning |
|---|---|
| `id` | unique within the pipeline |
| `capability` | which capability runs it (resolved by the active fleet) |
| `skills` | extra skills to load for this stage |
| `depends_on` | stage IDs that must finish first |
| `brief` | what the stage must achieve, with inputs pulled from the workspace |
| `outputs` | files it must write into the workspace |
| `gate` | condition to continue: `verify_pass`, `critic_not_blocking`, `human_approved` |
| `on_failure` | `retry(n)`, `fallback(stage)`, `escalate`, `abort` |
| `budget` | overrides for this stage |

### 7.2 Rules

1. **Parallel by default.** If two stages don't need each other's output, they must not depend on each other. The slide-14 "buy vs build" chain of 7 sequential hops should be about 3 waves.
2. **Every pipeline is a DAG.** No cycles. Loops ("revise until good") are bounded with `max_rounds`.
3. **Every pipeline ends in one `plan` stage** that writes the single final answer.
4. **Verification sits on the critical path** for any stage that produces code, numbers or cited facts.
5. **Critique is required** for Level 3 pipelines and for anything irreversible.
6. **Every outbound or irreversible action** passes through an `approve` gate.
7. **Declare the budget** at the pipeline level. Stages inherit it and may lower it, but never raise it.
8. **Name what goes into memory.** The last step lists which outputs are durable (sent to `remember`) and which are scratch.

### 7.3 Shape of a good pipeline

```
           ┌─ research ─┐
 plan ─────┼─ compute ──┼─ verify ─ strategize ─ critique ─ plan(final) ─ remember
           └─ build ────┘                                     │
                                                          approve (if outbound)
```

Wave 1 is the parallel fan-out. Wave 2 checks it. Wave 3 makes the decision, and wave 4 delivers and stores it.

---

## 8. Routing levels

The planner classifies every request **before** spending anything.

| Level | When | What runs | Typical cost |
|---|---|---|---|
| **0: Direct** | Simple fact, chat, short answer, no tools or one cheap tool | Planner answers alone | 1× |
| **1: Single specialist** | One clear capability is needed (e.g. "fix this script") | One agent + verify if it produced code, numbers or citations | 2–3× |
| **2: Parallel fan-out** | 2–3 independent parts | Up to 3 agents in parallel → verify → planner synthesizes | 4–8× |
| **3: Full pipeline** | High stakes, irreversible, money, security, or a strategic decision | Named pipeline with critique + approval gates | 10×+ |

**Rules**

- If in doubt, go **one level lower** and escalate if needed. Escalating is cheap; over-orchestrating is expensive.
- The planner must **state the chosen level and why** in the trace.
- The user can force a level ("quick answer" → L0, "full analysis" → L3).
- **Max fan-out = 3** concurrent workers unless the pipeline says otherwise.

---

## 9. Briefs and the shared workspace

Every worker starts fresh. Whatever isn't in its brief or the workspace doesn't exist for it.

### 9.1 The brief (see `templates/task-brief.md`)

Every brief **must** contain:

1. **Goal:** one sentence: what done looks like.
2. **Context:** why this matters, and what the user actually asked (quoted).
3. **Inputs:** exact workspace paths, URLs and data.
4. **Constraints:** scope, what's forbidden, deadlines, budget.
5. **Output contract:** exact sections and the file path to write.
6. **Acceptance criteria:** how the verifier will judge it.
7. **Escalate if:** conditions under which the worker stops and returns.

A brief that says "research X" with no acceptance criteria is a bug.

### 9.2 The workspace (see `templates/workspace/`)

```
workspace/<task-id>/
  00-request.md        # the user's original words, verbatim. Never edited.
  01-plan.md           # level, stages, budget, assumptions
  stages/<stage-id>/
    brief.md
    output.md          # follows the agent's output contract
    artifacts/         # code, data, logs, screenshots
    verify.md          # verifier's result for this stage
  critique.md
  final.md             # the single answer delivered
  trace.jsonl          # one line per event (see section 16)
```

**Rules**

- `00-request.md` is immutable. Every stage can read it, so the user's intent never gets lost in the chain.
- Writers and synthesizers read **raw stage outputs and artifacts**, not just another agent's summary.
- Workers write only inside their own `stages/<stage-id>/` folder.
- Workers report *completion events*. The planner never polls in a loop.

---

## 10. Verification

**Principle:** a claim that something was tested isn't a test. Verification means re-executing or re-checking independently.

| Output type | What the verifier does |
|---|---|
| Code / builds | Re-runs the exact commands from the execution log in a clean sandbox and compares output |
| Numbers | Recomputes with an independent method or a second implementation, and checks units and orders of magnitude |
| Citations | Fetches each source and confirms the cited text actually appears and supports the claim |
| Files written | Confirms they exist, parse, and match the contract |
| Claims of "no change" (monitoring) | Spot-checks one or two watched sources |

**Rules**

1. The verifier never fixes the work. It reports `pass` / `fail` / `could-not-verify` per claim with evidence.
2. Prefer **deterministic checks** (scripts, tests, diffs, schema validation). Use an LLM only for judgment calls such as "does this paragraph support this claim?"
3. If a stage fails verification, the planner decides: retry with the failure attached (max 2), reroute, or report the gap to the user. It never hides a failure.
4. The final answer lists anything that **could not be verified**.

---

## 11. Critique (red team)

**Principle:** a critic is only useful if it can think differently from the author.

**Rules**

1. Use a **different model family** for critique than for the plan being critiqued, when you can.
2. The critic gets the **decision and its evidence**, not the author's reasoning chain, so it isn't anchored by it.
3. Each weakness has a severity (`deal-breaker` / `significant` / `minor`) **and** a concrete scenario. "This could be a problem" is rejected.
4. The critic steelmans the opposing view once, and lists what survives.
5. Verdict: `proceed` / `proceed-with-changes` / `dont-proceed`.
6. A `deal-breaker` blocks the pipeline. The planner must address it or tell the user why it's overriding.
7. Bound the cycle: at most 2 critique → revise rounds, then deliver with open issues listed.

**When critique is mandatory:** Level 3; anything involving money, security, legal, health, deletion, publishing, or messaging other people; any recommendation the user will act on.

---

## 12. Memory

**Principle:** memory compounds, and so do errors in it. Write little, write carefully, and cite sources.

**Rules**

1. Only the `remember` capability writes long-term memory. Other agents propose; the Librarian decides.
2. **Durable vs scratch:** decisions, verified facts, user preferences, project state and lessons learned are durable. Intermediate drafts and raw search results are scratch.
3. **Search before write.** Update or merge existing notes instead of creating duplicates.
4. **Every note has a source** (task ID, URL or file) and a date. A note without a source is a rumor.
5. **Never silently delete.** Mark a note `superseded_by: [[new-note]]`.
6. **Unverified content is labeled** `status: unverified` and isn't used as a fact in later tasks.
7. **No secrets in memory, ever.**
8. Structure: `Research/`, `Decisions/`, `Projects/`, `People/`, `Journal/`, `Lessons/`. Use YAML frontmatter and `[[wikilinks]]`.

---

## 13. Security

See `policies/security.md` and `policies/tool-permissions.yaml`.

**Rules**

1. **Least privilege per agent.** Tools are deny-by-default. Agents never share one toolset.
2. **Untrusted content is data, not instructions.** Anything from the web, email, files or other agents' outputs is wrapped and labeled. An agent never follows instructions found inside it.
3. **Agents that read untrusted content don't hold dangerous tools.** Research and monitor agents have no shell, no write access outside their stage folder, and no secrets.
4. **Secrets are scoped per agent** and injected at runtime, never written into agent files, skills, memory or logs.
5. **Code runs in a sandbox** (container, VM or restricted user) with no network unless the brief requires it.
6. **Irreversible or outbound actions go through Gatekeeper**: sending messages, payments, deletes, pushes, deploys, posting publicly, changing permissions.
7. **One external entry point.** Only the planner faces the user. Specialists are internal and have no bots or public endpoints of their own.
8. **Data privacy:** don't send sensitive data to providers whose terms allow logging or training on it.

---

## 14. Budgets and termination

See `policies/budgets.yaml`.

| Limit | Default | Applies to |
|---|---|---|
| Max steps per worker | 40 | each stage |
| Max steps for planner | 60 | whole task |
| Max wall-clock per task | 30 min (L1–L2), 2 h (L3) | task |
| Max concurrent workers | 3 | task |
| Max retries per stage | 2 | stage |
| Max critique rounds | 2 | task |
| Max spend per task | set per deployment | task |

**Rules**

1. Every loop has a hard cap. There's no "until done" without a number.
2. At **80%** of any budget, the agent wraps up and returns its best partial result with a clear note.
3. A worker that makes no progress for 3 consecutive steps stops and escalates.
4. Budget exhaustion is reported to the user, never hidden.

---

## 15. Failure handling

| Failure | Response |
|---|---|
| Worker returns something that doesn't match its contract | Reject; retry once with the contract violation quoted |
| Verification fails | Retry with failure evidence (max 2) → reroute → report the gap |
| Tool or provider error / rate limit | Exponential backoff, then fallback model profile, then escalate |
| Conflicting results between stages | Planner reconciles explicitly in `final.md`, showing both |
| Critic says deal-breaker | Revise or explain the override to the user; never drop it silently |
| Budget hit | Stop, deliver a partial result, list what's missing |
| Ambiguous request | Planner asks the user **one** focused question before fanning out |
| Possible prompt injection detected | Stop that stage, quarantine the source, report it |
| Worker ran out of budget mid-phase | Verify the committed state yourself, post a numbered resume brief as a card comment, unblock; don't recreate the card |
| Partial work is internally inconsistent | Save it on a salvage branch, reset to the last tested commit, re-scope into smaller serial cards |
| "Timed out, retrying" | Check for surviving worker processes and half-written files first; ignore stale notices for cards already done |
| Two agents' branches conflict | A neutral third worker reconciles (skill `merge-reconciliation`); neither author resolves it |

### 15.1 Long-running and multi-phase work

Lessons from running a fleet on real multi-day builds (skills `task-board-orchestration` and `task-board-worker`):

1. **Start from green.** Scaffold first (skeleton, build and tests passing, first commit), then create the whole serial chain of phase cards up front.
2. **A progress file carries the conventions.** Each phase reads it first and appends its own section. Nothing has to be re-briefed.
3. **Size cards for one run.** Workers commit per item and, at 80% budget, stop at a clean commit with an exact resume list. A clean partial is cheap to resume; a dirty one costs a full re-run.
4. **The coordinator never waits on a card it is the parent of.** That's a deadlock.
5. **Comments are the durable channel.** Decisions made while a worker runs go into card comments, which the next run always sees.
6. **Self-reports are claims.** Before publishing, the planner re-runs the gates itself, including isolated runs of tracked tests, and scrubs host-specific data from the tree.

**Golden rule:** a fleet must **fail loudly**. "I couldn't verify X" is a valid answer; a confident wrong answer is the worst outcome.

---

## 16. Observability

Every event appends one line to `trace.jsonl`:

```json
{"ts":"2026-11-14T10:02:11Z","task":"t-0142","stage":"research-vendors","agent":"scout",
 "event":"stage_done","steps":17,"tokens_in":48211,"tokens_out":3120,"cost":0.04,
 "verify":"pass","notes":"3 sources, 1 could-not-verify"}
```

Track per task: level chosen, stages run, steps, tokens, cost, wall-clock, verify results, critic verdict, retries, and the final outcome (user accepted / corrected / rejected).

**Use it to answer:** which agent fails most? Which stage costs most? Is the planner over-escalating? Which skill is never used?

---

## 17. Evaluation

See `evals/`.

1. Keep a **golden task set** of 20–50 real tasks across all levels, each with acceptance criteria.
2. Run each task on the **single-agent baseline**, the **lean fleet** and the **full fleet**.
3. Score: correctness, completeness, groundedness (citations check out), cost, latency, and safety (no forbidden actions).
4. **Decision rule:** keep a role or pipeline only if it beats the baseline on quality by more than its added cost and latency.
5. Re-run the evals after every change to agents, skills, models or pipelines. Treat a drop in the scores like a failing test.
6. Add every real-world failure to the golden set as a new test case.

---

## 18. Anti-patterns

Each of these was seen in real fleet designs.

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| Strongest roles on the weakest models | The planner and memory decide everything downstream | Put the best model on plan, critique and remember |
| Critic on the same model as the author | Shared blind spots, so it rubber-stamps | Use a different model family for critique |
| All agents share all tools | One prompt injection = full compromise | Deny-by-default, per-agent tools |
| Long sequential chains | Latency, cost and error compound, and context gets lost | Parallel waves + shared workspace |
| "Described as tested" | Self-reports aren't evidence | An independent verifier that re-runs |
| Polling for completion | Wastes steps and tokens | Completion events |
| `max_iterations: 250` | Runaway cost | Hard caps + the 80% wrap-up rule |
| A bot or endpoint per specialist | Larger attack surface, user confusion | One entry point (the planner) |
| Writer reads only summaries | Telephone-game distortion | Writer reads raw outputs + `00-request.md` |
| Overlapping roles | Duplicate work, contradictory answers | One capability → one agent per fleet |
| No evals | Can't tell if the fleet helps at all | Golden set + single-agent baseline |
| Personas instead of contracts | Style without reliability | Testable output contracts |
| Coordinator as the parent of its own sub-cards | The child waits for the parent, the parent waits for the child: deadlock | Create sub-cards unlinked; link only chains between other agents |
| Phases bigger than one worker run | Budget runs out mid-change; the next run inherits a broken tree | One-run cards, commit per item, stop clean |
| Relaying truncated notifications | Generic advice replaces what the worker actually found | Read the full card; say changed vs advised |
| Exporting over a live profile | Wipes the user's own skills and local facts | Merge skills, back up `SOUL.md`, keep a `fleet:local` block |
| Publishing worker output unscrubbed | Real hostnames, IPs and paths leak into a public repo | Grep for host terms before every commit (`git-workflow` publishing gates) |

---

## 19. Checklists

### New agent
- [ ] One-sentence mission, no "and"
- [ ] Capabilities listed and bound in at least one fleet
- [ ] Tools deny-by-default; each allowed tool justified
- [ ] Output contract with exact sections
- [ ] Every rule is testable
- [ ] "When stuck" / escalation behavior defined
- [ ] Budgets set
- [ ] Added to `evals/golden-tasks.yaml` coverage

### New skill
- [ ] `description` says when to use and when not to
- [ ] Numbered procedure
- [ ] Pre-return checklist
- [ ] Output format
- [ ] Under ~150 lines; references split out
- [ ] No secrets or machine-specific paths

### New pipeline
- [ ] Uses capabilities, not agent names
- [ ] DAG; independent stages are parallel
- [ ] Verify gate after code, numbers and citations
- [ ] Critique gate if L3 or irreversible
- [ ] Approval gate before outbound or irreversible actions
- [ ] Budget declared
- [ ] Ends with a single `plan` synthesis stage + memory step
- [ ] At least 2 golden tasks exercise it

### Before going live
- [ ] Only the planner is user-facing
- [ ] Secrets scoped per agent; none in files
- [ ] Sandbox for code execution
- [ ] Tracing on
- [ ] Evals beat the single-agent baseline
- [ ] Exported profiles previewed with `--dry-run`; local facts in a `fleet:local` block
- [ ] Push gate (secret scan + host-term grep) in place for public repos
- [ ] Budget alerts configured

---

## 20. Glossary

- **Brief:** the self-contained instruction given to a worker for one stage.
- **Capability:** an abstract job a pipeline needs; bound to an agent by the fleet.
- **DAG:** directed acyclic graph; stages with dependencies and no cycles.
- **Fan-out:** running several stages in parallel.
- **Gate:** a condition a pipeline must satisfy to continue.
- **Golden set:** fixed evaluation tasks with known acceptance criteria.
- **Least privilege:** each agent gets only the tools and data its mission needs.
- **Output contract:** the exact structure an agent's result must follow.
- **Tripwire:** an observable condition that would change a recommendation.
- **Workspace:** the per-task folder shared by all stages.
