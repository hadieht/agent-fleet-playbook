---
name: decision-framing
description: Use when the user must choose between options (buy vs build, vendor A vs B, go/no-go, strategy). Produces a decision frame, option comparison, scenarios, one recommendation and a tripwire. Don't use for factual questions.
---

# Decision framing

## Procedure
1. **Frame:** what's being decided, by whom, by when; the criteria (weighted if possible); the cost of being wrong; whether it's reversible.
2. **Options:** 3–5 realistic options, always including **do nothing** and **wait and see**.
3. **Evaluate each option:** upside, downside, key risks, what it forecloses, second-order effects. Use only verified evidence and label assumptions.
4. **Scenarios:** define best, base and worst worlds (what's true in each) and score every option in each.
5. **Stress-test your favorite:** what would have to be true for it to be wrong?
6. **Recommend one option** with the single decisive reason.
7. **Tripwire:** an observable signal plus a threshold that would change the recommendation.

## Output format
```
## Decision frame
## Options        # table
## Scenarios      # table: option × best/base/worst
## Recommendation
## Tripwire
```

## Rules
- "It depends" must name what it depends on and what to do in each case.
- One recommendation, not a menu.
