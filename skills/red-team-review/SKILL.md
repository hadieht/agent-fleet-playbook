---
name: red-team-review
description: Use to stress-test a plan, recommendation, design, code change or system before it becomes final. Selects a mode (decision, design/security, code, AI agent) and the supporting skills, then produces severity-ranked weaknesses with concrete scenarios and a proceed / proceed-with-changes / don't-proceed verdict. Don't use to rewrite or improve the work.
---

# Red-team review

## Iron laws
> 1. **Every weakness has a concrete scenario:** "If X happens, then Y, because Z." "This could be a problem" is rejected.
> 2. **Attack the evidence and the decision, not the author's reasoning chain.** Don't let their framing anchor you.
> 3. **Critique only.** Propose changes as a list; never rewrite the work.

## Pick the mode(s)
| Target | Mode | Load these skills |
|---|---|---|
| Recommendation, strategy, forecast, purchase, go/no-go | **Decision** | `pre-mortem`, `cognitive-bias-check` |
| Architecture, new feature, integration, data flow | **Design / security** | `threat-modeling`, `cloud-infra-security` (if infra) |
| Code change or repository | **Code / security** | `secure-code-review`, `security-finding-triage`, `supply-chain-security` (if deps changed) |
| LLM app, agent workflow, this fleet | **AI agent** | `llm-agent-security`, `threat-modeling` |

Several modes can apply. Run the most severe first.

## Procedure (all modes)
1. **Restate the claim** being attacked, and what "success" means for it, in two sentences.
2. **Assumptions:** list what must be true for it to work. For each, is it **verified** (cite the stage or `verify.md`) or **unverified**? What happens if it's false?
3. **Logic attacks:** circular evidence, cherry-picked sources, unstated consequences, deferred deal-breakers ("we'll handle security later"), correlation treated as causation, survivorship bias.
4. **Mode-specific attacks:** run the loaded skills' procedures. In decision mode, run a pre-mortem and a bias check. In security modes, attack along STRIDE and the OWASP categories, with source → sink evidence for code findings.
5. **Adversary thinking:** who benefits from this failing, or from abusing it? What would a motivated attacker, a careless user, a competitor or a hostile insider do?
6. **Scale and time:** what breaks at 10× load, data or cost? In 12 months? When the key person leaves?
7. **Reversibility:** how hard is it to undo? Irreversible + uncertain = needs the strongest evidence.
8. **Steelman** the strongest case *against* the recommendation once, then the strongest case *for* it.
9. **Severity:**
   - `deal-breaker`: the plan fails, or causes serious harm (security breach, data loss, legal exposure, major money loss), if this is true. Blocks the pipeline.
   - `significant`: materially worse outcome; needs a change or explicit, owned acceptance.
   - `minor`: worth noting; 3 at most.
10. **What survives**, then the **verdict**.

## Output format (`critique.md`)
```
## Claim under review
## Modes run              # decision / design-security / code-security / ai-agent
## Assumptions
| assumption | verified? (evidence) | if false → |
## Weaknesses
| # | severity | weakness | concrete scenario | evidence | suggested change |
## Security findings      # (security modes) per secure-code-review / llm-agent-security format
## Pre-mortem top risks   # (decision mode) cause → early signal → mitigation
## Biases detected        # (decision mode)
## Steelman (against / for)
## What survives
## Verdict                # proceed | proceed-with-changes (numbered list) | dont-proceed
```

## Rules
- Max 2 critique → revise rounds per task; then deliver with the open issues listed.
- Use a different model family from the author where possible.
- Security PoCs only in an authorized sandbox, on systems the requester owns or is authorized to assess.
- If evidence for a load-bearing claim is missing, that's itself a `significant` weakness.
- Don't nitpick style when substance is at stake.

## Red flags in your own critique
- All weaknesses rated the same severity.
- No deal-breaker considered for an irreversible, high-stakes decision.
- Weaknesses that restate the author's own listed risks without adding anything.
- A verdict that doesn't follow from the weaknesses.
