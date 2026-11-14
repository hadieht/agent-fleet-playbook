---
name: pre-mortem
description: Use before committing to a plan, launch, migration, investment or decision, to imagine it has already failed and work out why. Surfaces risks that optimism hides and turns them into early-warning signals and mitigations. Complements red-team-review. Don't use after the fact (that's a post-mortem).
---

# Pre-mortem

## Iron law
> **Start from certainty of failure.** Don't ask "what could go wrong?". Say "it's 12 months from now, this failed badly; write the story of why."

## Procedure
1. **State the plan** and its success criteria in 2–3 sentences, plus the time horizon.
2. **Assume failure:** "It's <date + horizon>. The plan failed clearly and expensively."
3. **Generate failure stories independently.** Write at least **8** distinct causes before evaluating any. Cover each lens:
   | Lens | Prompts |
   |---|---|
   | Technical | It didn't scale; integration broke; data was worse than assumed; a dependency failed |
   | People / org | Key person left; no owner; teams misaligned; skills missing |
   | Market / users | Users didn't want it; competitor moved; adoption was slower than modeled |
   | Money / time | Cost overran; timeline slipped; budget cut halfway |
   | Security / legal | Breach; compliance issue; contract or licensing problem |
   | Assumptions | The one belief everyone shared was wrong |
   | Execution | Scope crept; we started three things and finished none |
   | External | Regulation, vendor price change, outage, macro shock |
4. **Score each cause:** likelihood (1–5) × impact (1–5). Mark which are **controllable**.
5. **For the top 5:**
   - **Early-warning signal:** what you'd observe *before* the failure (a metric, a date, an event).
   - **Mitigation:** what to do now to reduce likelihood or impact.
   - **Contingency:** what to do if the signal fires.
6. **Kill criteria:** the conditions under which you'd stop or pivot. Decide them now, while unbiased.

## Output format
```
## Plan & success criteria
## Failure stories        # numbered, 1–3 sentences each, concrete
## Risk ranking
| # | cause | likelihood | impact | score | controllable |
## Top risks → signals, mitigations, contingencies
| cause | early-warning signal | mitigation now | contingency |
## Kill / pivot criteria
```

## Rules
- Failure stories must be **specific** ("the Postgres CDC connector couldn't handle schema changes, so ingestion stopped for 3 days") not generic ("technical issues").
- Include at least one story where the core assumption was wrong.
- Pair it with skill `cognitive-bias-check` when the plan was championed by the same agent or person reviewing it.
