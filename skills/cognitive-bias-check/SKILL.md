---
name: cognitive-bias-check
description: Use when reviewing a recommendation, forecast, estimate, research conclusion or decision to detect common reasoning biases (confirmation, anchoring, overconfidence, sunk cost, survivorship, base-rate neglect and others) and apply debiasing techniques. Complements red-team-review and pre-mortem. Don't use for code correctness.
---

# Cognitive bias check

## Iron law
> **Check the reasoning, not just the conclusion.** A right answer reached by biased reasoning is luck. Name the bias, show where it appears, and apply the counter-technique.

## Procedure
1. List the **key claims and numbers** the conclusion depends on.
2. For each bias below, ask its detection question. Note where it applies, quoting the text.
3. Apply the matching **debiasing technique** and record whether the conclusion changes.
4. Report only biases with concrete evidence in the text. Don't list every bias for completeness.

## Bias table
| Bias | Detection question | Debiasing technique |
|---|---|---|
| **Confirmation bias** | Were sources sought that could *disprove* the conclusion? Are contrary findings missing or dismissed? | Search explicitly for disconfirming evidence; steelman the opposite |
| **Anchoring** | Did the first number seen (vendor quote, last year's figure, the user's guess) shape the estimate? | Re-estimate from an independent method; use reference classes |
| **Overconfidence** | Are ranges narrow or missing? Is confidence "high" with thin evidence? | Use ranges (90% intervals); state what would change your mind |
| **Planning fallacy** | Are time and cost estimates built bottom-up from an ideal path? | **Reference class forecasting:** how long or costly were similar projects *actually*? |
| **Base-rate neglect** | Does the reasoning ignore how often this kind of thing succeeds or fails in general? | Start from the base rate, then adjust for specifics |
| **Survivorship bias** | Is evidence drawn only from successes (case studies, winners, "companies that did X")? | Ask where the failures are, and what fraction failed |
| **Sunk cost** | Does "we've already invested" justify continuing? | Decide only on future costs and benefits |
| **Status quo / default bias** | Is "keep doing what we do" assumed safe without analysis? | Evaluate "do nothing" as an explicit option with its own risks |
| **Availability bias** | Is a vivid recent event driving the risk assessment? | Use frequencies and data, not memorable anecdotes |
| **Authority / halo** | Is a claim accepted because of who said it (vendor, big company, expert)? | Evaluate the evidence independently of the source |
| **Groupthink / shared assumptions** | Did all agents or sources agree suspiciously easily, perhaps from the same upstream source? | Independent generation before discussion; a designated dissenter (Rook) |
| **Narrative fallacy** | Is a clean causal story told with weak causal evidence? | Ask for the mechanism and the counterfactual |
| **Correlation ≠ causation** | Is causation inferred from co-occurrence? | Look for confounders, reverse causation, controlled comparisons |
| **Scope insensitivity** | Would the conclusion be the same if the numbers were 10× bigger or smaller? | Do a sensitivity check (skill `quantitative-modeling`) |
| **Optimism bias** | Are benefits concrete but risks vague? | Pre-mortem (skill `pre-mortem`) |
| **Automation bias** (AI-specific) | Was a model's or tool's output accepted without verification? | Independent verification stage; check citations |
| **Sycophancy** (AI-specific) | Does the conclusion mirror the user's stated preference rather than the evidence? | Re-derive the answer as if the user had expressed the opposite preference |

## Output format
```
## Key claims
## Biases detected
| bias | where (quote) | effect on conclusion | debiasing applied | result |
## Revised conclusion   # unchanged / changed (how) / confidence adjusted
```
