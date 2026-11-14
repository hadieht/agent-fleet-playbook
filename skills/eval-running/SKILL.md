---
name: eval-running
description: Use to measure whether a fleet, agent, skill or pipeline change helps, by running the golden task set against a single-agent baseline and scoring the results. Use after any change to agents, skills, models or pipelines.
---

# Eval running

## Procedure
1. Load `evals/golden-tasks.yaml`.
2. For each task, run three configurations: `baseline` (one strong agent, all skills, no fleet), `lean`, `full`.
3. Save each run's `final.md` and `trace.jsonl` under `evals/runs/<date>/<config>/<task-id>/`.
4. Score with `evals/rubric.md`: correctness, completeness, groundedness, safety (0–3 each), plus cost, latency and steps from the trace.
5. Use blind grading where possible: the grader doesn't know which config produced which answer, and is a different model from those under test.
6. Aggregate per config and per level.
7. Apply the decision rule: a config or role stays only if its quality gain beats its cost and latency increase. Write the result to `evals/runs/<date>/summary.md`.

## Summary format
```
| config | quality (avg/12) | safety fails | avg cost | avg latency | L0 | L1 | L2 | L3 |
## Decision
## Regressions
## New failure cases to add
```
