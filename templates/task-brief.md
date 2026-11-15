# Brief: <stage-id> (task <task-id>)

**Capability:** <research|build|compute|...>   **Pipeline:** <id>   **Wave:** <n>

## 1. Goal
<one sentence: what done looks like>

## 2. Context
User's request (verbatim, from `00-request.md`):
> ...

Why this stage matters:

## 3. Inputs
- Known facts (hosts, paths, earlier findings, task ids):
- Progress file to read first (multi-phase work):
- `workspace/<task-id>/...`
- <URLs / data>

## 4. Constraints
- Mode: apply | advise
- Approved actions (live systems; backup first, prove the effect):
- Scope:
- Forbidden:
- Budget: max_steps <n>, max_wallclock_min <n>

## 5. Output contract
Write to `stages/<stage-id>/output.md` with sections:
```
## ...
```

## 6. Acceptance criteria
1.
2.

## 7. Escalate if
-
