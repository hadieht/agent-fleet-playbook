# Evals

Before trusting a fleet, prove it beats one good agent.

1. Write 20–50 real tasks into `golden-tasks.yaml`, covering all levels and including adversarial cases.
2. Run each task on three configs: `baseline` (single strong agent with all skills), `lean` and `full`.
3. Score with `rubric.md`, ideally blind and graded by a different model or a human.
4. Keep a role or pipeline only if its quality gain beats its added cost and latency.
5. Re-run after any change to agents, skills, models or pipelines. Treat a drop in the scores like a failing test.
6. Add every real-world failure as a new golden task.

The procedure is in `skills/eval-running/SKILL.md`. Store results under `evals/runs/<date>/`, which is gitignored except for `summary.md`.
