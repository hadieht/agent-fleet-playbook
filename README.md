# Agent Fleet Playbook

A framework-agnostic kit for planning, building and running fleets of AI agents: agent specs, a reusable skill set, pipelines, two switchable fleet configs (lean and full), policies, templates and evals.

Everything is plain Markdown and YAML, so you can wire it into any runtime: Hermes, Claude Code, LangGraph, CrewAI, OpenAI Agents SDK, or a custom loop.

## Start here

1. Read **[FLEET_PLANNING_GUIDE.md](FLEET_PLANNING_GUIDE.md)**. It covers the concepts, rules, checklists and anti-patterns.
2. Pick a fleet in **[fleet.config.yaml](fleet.config.yaml)** (`lean` is recommended to start).
3. Browse the **[agents](agents/)**, **[skills](skills/)** and **[pipelines](pipelines/)**.
4. Before trusting the fleet, run the **[evals](evals/)** against a single-agent baseline.

## Layout

```
FLEET_PLANNING_GUIDE.md   the full guide: rules, design method, checklists
fleet.config.yaml         active fleet + global settings
agents/                   one spec per agent (YAML frontmatter + instructions)
skills/                   reusable SKILL.md procedures + catalog
pipelines/                DAGs of stages, written against capabilities
fleets/                   lean.yaml and full.yaml: capability → agent bindings
policies/                 tool permissions, budgets, approvals, security
templates/                blank agent, skill, pipeline, brief, workspace
evals/                    golden tasks, scoring rubric, baseline protocol
```

## The two fleets

| Lean (6 + gate) | Full (10 + verifier + gate) |
|---|---|
| Atlas: plan, strategize, write | Atlas: plan |
| Scout: research, monitor | Cipher: research · Pulse: monitor |
| Forge: build, compute | Forge: build · Quant: compute |
| Rook: critique | Vega: strategize · Rook: critique |
| Verifier: verify | Verifier: verify |
| Librarian: remember | Librarian: remember · Muse: write |
| Gatekeeper: approve (non-LLM) | Gatekeeper: approve (non-LLM) |

Pipelines ask for **capabilities**, never agents, so switching fleets needs no pipeline changes.

## Wiring into a runtime

| Runtime | How |
|---|---|
| Any LLM loop | System prompt = agent body + loaded `SKILL.md` bodies. Enforce `tools.allow` in your tool router. |
| Claude Code | Copy agents to `.claude/agents/` (frontmatter: `name`, `description`, `tools`) and skills to `.claude/skills/`. |
| Hermes | One profile per agent. `SOUL.md` = agent body; copy skills into the profile's skills folder. |
| LangGraph / CrewAI | One node or agent per stage. Resolve `capability` through `fleets/<active>.yaml`. |

### Hermes: generated profiles

```bash
pip install pyyaml
python scripts/export_hermes.py --fleet lean                          # → dist/hermes/lean/<agent>/
python scripts/export_hermes.py --fleet lean --out ~/.hermes/profiles --dry-run   # preview what would change
python scripts/export_hermes.py --fleet lean --out ~/.hermes/profiles --force     # update existing profiles
```

Each profile gets a `SOUL.md` (agent spec + fleet routing context + global rules) and the fleet's skills in its `skills/` folder.

**Existing profiles are safe:**
- Profiles that already have a `SOUL.md` are skipped unless you pass `--force`. Run `--dry-run` first.
- With `--force`, the old `SOUL.md` is copied to `SOUL.md.bak-<timestamp>`. Anything between `<!-- fleet:local -->` and `<!-- /fleet:local -->` (your vault path, hosts, team conventions) is carried into the new file, so put local facts there rather than editing the generated text.
- Skills are **merged, never wiped**. Your own and the bundled Hermes skills stay. The exporter tracks what it installed in `skills/.fleet-skills`, and only updates or removes those. A fleet skill with the same name as one of yours is skipped unless you pass `--replace-colliding`.
- `config.yaml`, memories, sessions and auth are never touched.

To add an external skill to specific profiles, prefer the Hermes hub over vendor installers (which often target other runtimes): `HERMES_HOME=~/.hermes/profiles/<agent> hermes skills install <owner>/<repo>/skills/<name> --yes`. Install by role (code skills to forge, not to every profile), and read any skill flagged by the security scan before you install it by hand. `fleet-profile.yaml` is a **reference only**: copy the model choice and toolsets into each profile's own `config.yaml` by hand, because its keys depend on your Hermes version. Gatekeeper isn't exported, since it's a rules engine plus your approval, not a model.

After installing: point your single messaging bot at the **atlas** profile only. The specialists stay internal.

### CI

`.github/workflows/validate.yml` runs `scripts/validate.py` on every push and pull request, exports both fleets, and attaches them as the `hermes-profiles` build artifact.

The models are deliberately **not** pinned. Each agent declares a `model_profile` (requirements), and you choose the models at deploy time.
