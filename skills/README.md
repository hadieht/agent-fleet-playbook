# Skill set

Every skill is a folder with a `SKILL.md` in the open **Agent Skills** format (YAML frontmatter `name` + `description`, then Markdown instructions). Larger skills put depth in a `reference/` folder that agents load only when needed (progressive disclosure). The format is supported by Hermes, Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI and others. In any other runtime, paste the body into the agent's prompt.

**39 skills** in 7 groups. Skills marked ★ have an **iron law**: one non-negotiable rule, backed by red flags and a table of rationalizations to reject. That pattern is the most effective way we know to stop agents from taking shortcuts.

## Catalog

### Coordination
| Skill | Purpose |
|---|---|
| [routing-and-triage](routing-and-triage/SKILL.md) | Pick Level 0–3 for each request |
| [task-decomposition](task-decomposition/SKILL.md) | Split work into stages, waves and gates |
| [brief-writing](brief-writing/SKILL.md) | Self-contained briefs for zero-context workers |
| [synthesis](synthesis/SKILL.md) | Merge verified outputs into one answer |
| [budget-control](budget-control/SKILL.md) | Step, token and time limits; 80% wrap-up; no-progress rule |

### Engineering (language-agnostic)
| Skill | Purpose |
|---|---|
| [code-build-verify](code-build-verify/SKILL.md) ★ | Master coding workflow; routes to the skills below; evidence before completion claims |
| [clean-code](clean-code/SKILL.md) ★ | Naming, functions, SRP, errors, duplication, comments; [smells catalog](clean-code/reference/code-smells.md), [design principles](clean-code/reference/design-principles.md) |
| [test-driven-development](test-driven-development/SKILL.md) ★ | Red-green-refactor, test seen failing first; [testing anti-patterns](test-driven-development/reference/testing-anti-patterns.md) |
| [systematic-debugging](systematic-debugging/SKILL.md) ★ | 4-phase root-cause process, one variable at a time, three-strike rule |
| [refactoring-safely](refactoring-safely/SKILL.md) ★ | Characterization tests, small steps, strangler fig, expand/contract |
| [code-review](code-review/SKILL.md) ★ | 8-axis review with severity-ranked, scenario-backed findings |
| [api-design](api-design/SKILL.md) ★ | HTTP semantics, Problem Details (RFC 9457), pagination, idempotency, compatibility |
| [database-design](database-design/SKILL.md) ★ | Constraints, safe migrations, N+1, indexes, query plans |
| [performance-engineering](performance-engineering/SKILL.md) ★ | Measure → change one thing → measure; profiling; caching rules |
| [git-workflow](git-workflow/SKILL.md) ★ | Small commits, clear messages, secrets check, PR template |
| [containers-and-ci](containers-and-ci/SKILL.md) ★ | Dockerfiles, Kubernetes, hardened CI (SHA-pinned actions, OIDC, script injection) |

### Language stacks
| Skill | Purpose |
|---|---|
| [dotnet-csharp](dotnet-csharp/SKILL.md) ★ | Modern C# / .NET; references: [modern C#](dotnet-csharp/reference/modern-csharp.md), [ASP.NET Core](dotnet-csharp/reference/aspnetcore.md), [EF Core](dotnet-csharp/reference/efcore.md), [testing](dotnet-csharp/reference/testing.md), [performance & diagnostics](dotnet-csharp/reference/performance-diagnostics.md), [security](dotnet-csharp/reference/security.md), [project setup](dotnet-csharp/reference/project-setup.md) |
| [python-engineering](python-engineering/SKILL.md) ★ | uv, ruff, type checking, pytest, safe subprocess / deserialization / paths |
| [typescript-engineering](typescript-engineering/SKILL.md) ★ | Strict TS, runtime validation, no floating promises, DOM and Node sinks |

### Research and knowledge
| Skill | Purpose |
|---|---|
| [source-research](source-research/SKILL.md) | Cited, tiered, triangulated findings |
| [citation-verification](citation-verification/SKILL.md) | Does the source exist and support the claim? |
| [change-monitoring](change-monitoring/SKILL.md) | Recurring watches that report only deltas |
| [knowledge-capture](knowledge-capture/SKILL.md) | Durable vs scratch, dedupe, sourced notes |
| [report-writing](report-writing/SKILL.md) | Reader-first documents with a fidelity pass |

### Decision and red team
| Skill | Purpose |
|---|---|
| [quantitative-modeling](quantitative-modeling/SKILL.md) | Math in code + sanity check + sensitivity |
| [decision-framing](decision-framing/SKILL.md) | Options, scenarios, one recommendation, tripwire |
| [red-team-review](red-team-review/SKILL.md) ★ | Master critique workflow: decision, design/security, code/security and AI-agent modes |
| [pre-mortem](pre-mortem/SKILL.md) ★ | Assume failure, generate causes, early-warning signals, kill criteria |
| [cognitive-bias-check](cognitive-bias-check/SKILL.md) ★ | 17 biases (incl. AI automation bias and sycophancy) with debiasing techniques |

### Security
| Skill | Purpose |
|---|---|
| [threat-modeling](threat-modeling/SKILL.md) ★ | DFD + trust boundaries, STRIDE per element, abuse cases, LINDDUN; [STRIDE prompts](threat-modeling/reference/stride-checklist.md) |
| [secure-code-review](secure-code-review/SKILL.md) ★ | Differential / full / targeted modes; source→sink; [OWASP Top 10:2025 checklist](secure-code-review/reference/vulnerability-checklist.md) |
| [security-finding-triage](security-finding-triage/SKILL.md) ★ | 7 false-positive gates, CVSS v4.0, variant analysis |
| [supply-chain-security](supply-chain-security/SKILL.md) ★ | Dependency vetting, typosquats, lockfiles, pinning, SBOM, provenance, agent plugins/skills |
| [cloud-infra-security](cloud-infra-security/SKILL.md) ★ | IAM, network exposure, storage, secrets, logging, Kubernetes, IaC |
| [llm-agent-security](llm-agent-security/SKILL.md) ★ | Lethal trifecta, OWASP LLM Top 10 (2025), OWASP Agentic Top 10 (2026) |
| [prompt-injection-defense](prompt-injection-defense/SKILL.md) | Treat untrusted content as data |
| [approval-gating](approval-gating/SKILL.md) | Request human approval for gated actions |

### Verification and quality
| Skill | Purpose |
|---|---|
| [output-verification](output-verification/SKILL.md) | Independent re-run, recompute, validate |
| [eval-running](eval-running/SKILL.md) | Golden set vs single-agent baseline |

## Skill → agent matrix

`●` = default skill · `○` = added when the agent holds an extra capability in the lean fleet

**Global skills:** `budget-control` is loaded by every agent, and `approval-gating` by every agent that can propose a gated action. Your runtime should inject them automatically (see `global_skills` in `fleet.config.yaml`), so they aren't repeated in each agent's frontmatter.

| Skill | atlas | scout | cipher | pulse | forge | quant | vega | rook | verifier | librarian | muse |
|---|---|---|---|---|---|---|---|---|---|---|---|
| routing-and-triage, task-decomposition, brief-writing, synthesis | ● | | | | | | | | | | |
| source-research | | ● | ● | | | | | | | | |
| citation-verification | | ● | ● | | | | | | ● | | |
| change-monitoring | | ○ | | ● | | | | | | | |
| code-build-verify, clean-code, test-driven-development, systematic-debugging, refactoring-safely | | | | | ● | | | | | | |
| api-design, database-design, performance-engineering, git-workflow, containers-and-ci | | | | | ● | | | | | | |
| dotnet-csharp, python-engineering, typescript-engineering | | | | | ● | | | | | | |
| code-review | | | | | ● | | | | ● | | |
| quantitative-modeling | | | | | ○ | ● | | | | | |
| decision-framing | ○ | | | | | | ● | | | | |
| cognitive-bias-check | ○ | | | | | | ● | ● | | | |
| pre-mortem | | | | | | | ● | ● | | | |
| red-team-review, threat-modeling, secure-code-review, cloud-infra-security, llm-agent-security | | | | | | | | ● | | | |
| security-finding-triage | | | | | | | | ● | ● | | |
| supply-chain-security | | | | | ● | | | ● | | | |
| output-verification | | | | | | | | | ● | | |
| knowledge-capture | | | | | | | | | | ● | |
| report-writing | ○ | | | | | | | | | | ● |
| prompt-injection-defense | | ● | ● | ● | ● | | | | ● | | |
| eval-running | *(run by you or CI, not by fleet agents)* |

## External skill sources (reviewed, used for inspiration)

These collections informed the patterns used here. The skills in this repo are original text written for this fleet, not copies. **Read every external skill before installing it.** Skills are instructions and can include scripts, so treat them like code from the internet.

| Source | What it's good for | License |
|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) · [agentskills.io](https://agentskills.io/) | The open specification for the format | see repo |
| [anthropics/skills](https://github.com/anthropics/skills) | Official example skills; document skills | Apache 2.0 (examples) |
| [obra/superpowers](https://github.com/obra/superpowers) | Disciplined engineering workflows: TDD, systematic debugging, verification before completion; the iron-law and rationalization-table pattern | MIT |
| [dotnet/skills](https://github.com/dotnet/skills) | Microsoft's official .NET skills: core, ASP.NET Core, EF/data, diagnostics, MSBuild, NuGet, testing, upgrades, MAUI, Blazor | MIT |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Security auditing: differential review, insecure defaults, sharp edges, false-positive checks, variant analysis, supply-chain risk, CVSS scoring, static analysis | CC-BY-SA-4.0 |
| [openai/skills](https://github.com/openai/skills), [google/skills](https://github.com/google/skills), [vercel-labs/skills](https://github.com/vercel-labs/skills) | Other vendor collections in the same format | see repos |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Hermes bundled skills; `hermes skills tap add <repo>` adds a GitHub repo as a source | MIT |
| [SamurAIGPT/awesome-hermes-agent](https://github.com/SamurAIGPT/awesome-hermes-agent) | Community list (not official) | see repo |

Standards referenced: [OWASP Top 10:2025](https://top10.owasp.org/2025), OWASP Top 10 for LLM Applications (2025), OWASP Top 10 for Agentic Applications (2026), CVSS v4.0 (FIRST), RFC 9457 (Problem Details).

**Installing an external skill alongside these:** copy its folder into `skills/`, check that its `name` doesn't collide with an existing one, add it to the matrix above and to the right agents, then run `python scripts/validate.py`.

## Adding a skill
1. Copy `templates/skill-template/` to `skills/<name>/`. The folder name must equal `name` (lowercase, hyphens).
2. Write a `description` that says when to use it and when not to (it's the trigger).
3. Keep `SKILL.md` under ~200 lines. Move depth into `reference/*.md` and link it with relative links.
4. For discipline skills, add an iron law, red flags and a rationalizations table.
5. Add it to the catalog and matrix above, and to the agents that should load it.
6. Run `python scripts/validate.py`. It checks names, links and line counts.
