---
name: quantitative-modeling
description: Use for any calculation, cost model, TCO, forecast, financial comparison or statistical question. All math is done in code, with assumptions, a sanity check and sensitivity analysis. Don't use for qualitative judgments.
---

# Quantitative modeling

## Procedure
1. **Restate as a computation:** output quantity, units, time horizon.
2. **List inputs:** value, unit, source (stage path or URL) or `assumed` with a rationale.
3. **Write the model in code** (`artifacts/model.py` or similar). Keep the inputs in one block at the top.
4. **Run it** and record the output.
5. **Sanity check** with an independent method (back-of-envelope, an alternative formula, a known benchmark). They should agree within a stated tolerance, or you explain the gap.
6. **Sensitivity:** vary the 2–3 most uncertain inputs (e.g. ±20% or a plausible range) and report the result range and which input dominates.
7. **Bottom line** in one plain sentence.

## Output format
```
## Question
## Assumptions   # table: input | value | unit | source/assumed
## Method        # formula + script path
## Result
## Sanity check
## Sensitivity   # table: input | low | high | result range
## Bottom line
```

## Rules
- No number without its derivation.
- Units on every number.
- Report a range when inputs are uncertain.
- An input that is unknown, not just uncertain: build a scenario table over its plausible range instead of picking one value.
- Keep "the model says" separate from "so the decision is". The numbers are yours; the decision belongs to `strategize` or `plan`.
