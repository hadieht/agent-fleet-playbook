# Pipelines

Each pipeline is a DAG of stages written against **capabilities**, never agent names. The active fleet (`fleet.config.yaml`) resolves each capability to an agent.

| Pipeline | Level | Use when |
|---|---|---|
| [direct-answer](direct-answer.yaml) | 0 | Simple question; the planner answers alone |
| [single-specialist](single-specialist.yaml) | 1 | One capability + verification |
| [research-brief](research-brief.yaml) | 2 | Answer a question with sourced research and a written brief |
| [build-and-verify](build-and-verify.yaml) | 1–2 | Build or change code, verified, with release behind approval |
| [decision](decision.yaml) | 3 | Buy vs build, vendor choice, go/no-go (the slide-14 example, parallelized) |
| [watch-digest](watch-digest.yaml) | scheduled | Recurring monitoring → dated digest in the vault |

## Stage schema
```yaml
- id: string                 # unique in pipeline
  capability: string         # plan|research|monitor|build|compute|strategize|critique|verify|remember|write|approve
  skills: [string]           # extra skills for this stage (optional)
  depends_on: [stage-id]     # only real data dependencies
  brief: string              # goal + inputs; the planner expands it with brief-writing
  outputs: [path]            # relative to stages/<id>/
  gate: verify_pass | critic_not_blocking | human_approved   # optional
  when: string               # optional condition, e.g. "plan.level >= 3"
  on_failure: retry(2) | fallback(<stage>) | escalate | abort
  budget: {max_steps: int, max_wallclock_min: int}          # may lower, never raise
```
