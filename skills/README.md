# Skill set

Every skill is a folder with a `SKILL.md` in the open **Agent Skills** format (YAML frontmatter `name` + `description`, then Markdown instructions). The format is supported by Hermes, Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI and others. In any other runtime, paste the body into the agent's prompt.

## Catalog

| Skill | Group | Purpose |
|---|---|---|
| [routing-and-triage](routing-and-triage/SKILL.md) | Coordination | Pick Level 0–3 for each request |
| [task-decomposition](task-decomposition/SKILL.md) | Coordination | Split work into stages, waves and gates |
| [brief-writing](brief-writing/SKILL.md) | Coordination | Self-contained briefs for zero-context workers |
| [synthesis](synthesis/SKILL.md) | Coordination | Merge verified outputs into one answer |
| [budget-control](budget-control/SKILL.md) | Coordination | Step/token/time limits, 80% wrap-up, no-progress rule |
| [source-research](source-research/SKILL.md) | Research | Cited, tiered, triangulated findings |
| [citation-verification](citation-verification/SKILL.md) | Research / Verify | Does the source exist and support the claim? |
| [change-monitoring](change-monitoring/SKILL.md) | Research | Recurring watches that report only deltas |
| [code-build-verify](code-build-verify/SKILL.md) | Build | Small increments, sandbox, real execution logs |
| [quantitative-modeling](quantitative-modeling/SKILL.md) | Build | Math in code + sanity check + sensitivity |
| [decision-framing](decision-framing/SKILL.md) | Decide | Options, scenarios, one recommendation, tripwire |
| [red-team-review](red-team-review/SKILL.md) | Decide | Severity-ranked weaknesses with scenarios |
| [output-verification](output-verification/SKILL.md) | Verify | Independent re-run / recompute / validate |
| [knowledge-capture](knowledge-capture/SKILL.md) | Memory | Durable vs scratch, dedupe, sourced notes |
| [report-writing](report-writing/SKILL.md) | Communicate | Reader-first documents with a fidelity pass |
| [approval-gating](approval-gating/SKILL.md) | Safety | Request human approval for gated actions |
| [prompt-injection-defense](prompt-injection-defense/SKILL.md) | Safety | Treat untrusted content as data |
| [eval-running](eval-running/SKILL.md) | Quality | Golden set vs single-agent baseline |

## Skill → agent matrix

`●` = default skill · `○` = added when the agent holds an extra capability in the lean fleet

**Global skills:** `budget-control` is loaded by every agent, and `approval-gating` by every agent that can propose a gated action. Your runtime should inject them automatically (see `global_skills` in `fleet.config.yaml`), so they aren't repeated in each agent's frontmatter.

| Skill | atlas | scout | cipher | pulse | forge | quant | vega | rook | verifier | librarian | muse |
|---|---|---|---|---|---|---|---|---|---|---|---|
| routing-and-triage | ● | | | | | | | | | | |
| task-decomposition | ● | | | | | | | | | | |
| brief-writing | ● | | | | | | | | | | |
| synthesis | ● | | | | | | | | | | |
| budget-control | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| source-research | | ● | ● | | | | | | | | |
| citation-verification | | ● | ● | | | | | | ● | | |
| change-monitoring | | ○ | | ● | | | | | | | |
| code-build-verify | | | | | ● | | | | | | |
| quantitative-modeling | | | | | ○ | ● | | | | | |
| decision-framing | ○ | | | | | | ● | | | | |
| red-team-review | | | | | | | | ● | | | |
| output-verification | | | | | | | | | ● | | |
| knowledge-capture | | | | | | | | | | ● | |
| report-writing | ○ | | | | | | | | | | ● |
| approval-gating | ● | | | | ● | | | | | | ● |
| prompt-injection-defense | | ● | ● | ● | ● | | | | ● | | |
| eval-running | *(run by you or CI, not by fleet agents)* |

## External skill sources

These are public collections of skills in the same format, useful for adding domain skills such as GitHub, DevOps, documents or data work. **Read every external skill before installing it.** Skills are instructions and can contain scripts, so treat them like code from the internet.

| Source | Notes |
|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) · [agentskills.io](https://agentskills.io/) | The open specification for the format |
| [anthropics/skills](https://github.com/anthropics/skills) | Official example skills (Apache 2.0 for the examples) |
| [openai/skills](https://github.com/openai/skills), [google/skills](https://github.com/google/skills), [vercel-labs/skills](https://github.com/vercel-labs/skills) | Other vendor collections in the same format |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Hermes bundled skills; `hermes skills tap add <repo>` adds a GitHub repo as a skill source |
| [SamurAIGPT/awesome-hermes-agent](https://github.com/SamurAIGPT/awesome-hermes-agent) | Community list (not official) |

## Adding a skill
1. Copy `templates/skill-template/` to `skills/<name>/`. The folder name must equal `name` (lowercase, hyphens).
2. Write a `description` that says when to use it and when not to.
3. Add it to the catalog and matrix above, and to the agents that should load it.
4. Run `python scripts/validate.py`.
