---
name: llm-agent-security
description: Use to design, review or red-team LLM applications and AI agent systems, including this fleet, for prompt injection, data exfiltration, excessive agency, tool misuse, memory poisoning, insecure inter-agent communication, cascading failures and runaway cost. Maps to the OWASP Top 10 for LLM Applications (2025) and the OWASP Top 10 for Agentic Applications (2026). Only for systems the requester owns or is authorized to test.
---

# LLM and agent security

## Iron law
> **Assume every model will eventually follow an injected instruction.** Security must come from architecture (permissions, isolation, approvals), not from the prompt asking the model to behave.

## The lethal trifecta: check this first
An agent that has **all three** of these can be made to steal data:
1. Access to **private data** (files, memory, email, databases, secrets)
2. Exposure to **untrusted content** (web pages, emails, documents, issues, other agents' outputs)
3. A way to **communicate externally** (HTTP requests, email, messages, rendering images or links, writing to shared places)

**Break at least one leg for every agent.** In this fleet: Scout and Pulse read untrusted content, so they get no secrets and no outbound tools. Outbound actions go only through the Gatekeeper with human approval.

## Procedure
1. **Inventory:** list every agent and model call, with its inputs (and where each comes from), tools, data access, memory read/write, and output destinations.
2. **Trifecta check** for each agent (above).
3. **Walk both OWASP lists** (below) for each component.
4. **Test** with adversarial cases in a sandbox: indirect injections in fetched pages and documents, malicious tool outputs, poisoned memory notes, over-long inputs, cost bombs. Add them to `evals/golden-tasks.yaml`.
5. **Report** using the finding format from `secure-code-review`, with these IDs as the category.

## OWASP Top 10 for LLM Applications (2025)
| ID | Risk | Check / control |
|---|---|---|
| LLM01 | Prompt Injection (direct and indirect) | Untrusted content wrapped and labeled as data; no high-privilege tools in agents that read it; approvals for side effects; injection test cases |
| LLM02 | Sensitive Information Disclosure | No secrets in prompts; output filtering for PII and secrets; per-user data scoping in retrieval |
| LLM03 | Supply Chain | Models, datasets, skills, plugins, MCP servers vetted and pinned (skill `supply-chain-security`) |
| LLM04 | Data and Model Poisoning | Provenance for training, fine-tuning and RAG data; memory writes gated and sourced |
| LLM05 | Improper Output Handling | Model output treated as untrusted: encoded before HTML, parameterized before SQL, never `eval`'d, validated against a schema before acting |
| LLM06 | Excessive Agency | Minimal tools, minimal permissions, minimal autonomy; human approval for irreversible actions |
| LLM07 | System Prompt Leakage | No secrets or authz logic in system prompts; assume prompts are public |
| LLM08 | Vector and Embedding Weaknesses | Access control enforced at retrieval (tenant/user filters); no cross-tenant embeddings leakage; poisoning checks |
| LLM09 | Misinformation | Grounding with citations; verification stage; calibrated confidence; "could not verify" allowed |
| LLM10 | Unbounded Consumption | Token, step, time and cost budgets; rate limits per user; fan-out caps |

## OWASP Top 10 for Agentic Applications (2026)
| ID | Risk | Check / control |
|---|---|---|
| ASI01 | Agent Goal Hijack | Goals and instructions only from trusted channels (spec, brief, planner); injected goals detected and ignored; plans re-checked against the original request (`00-request.md`) |
| ASI02 | Tool Misuse and Exploitation | Narrow tools with typed, validated parameters; allow-listed targets; dry-run modes; approval gates |
| ASI03 | Identity and Privilege Abuse | Each agent has its own identity and scoped credentials; no credential sharing or inheritance between agents; short-lived tokens |
| ASI04 | Agentic Supply Chain Vulnerabilities | Skills, tools, prompts and MCP servers loaded at runtime are pinned and reviewed; no fetching and executing remote instructions |
| ASI05 | Unexpected Code Execution (RCE) | Generated code runs only in a sandbox (no host access, no secrets, network off by default); code-exec tools separated from data-access tools |
| ASI06 | Memory & Context Poisoning | Memory writes only via the Librarian, with sources and `verified`/`unverified` status; untrusted content never stored as fact; poisoned notes can be traced and superseded |
| ASI07 | Insecure Inter-Agent Communication | Inter-agent messages via the workspace with provenance; agents treat other agents' outputs as data; authenticated channels when distributed |
| ASI08 | Cascading Failures | Verification gates between stages; retry and fan-out limits; circuit breakers; one agent's failure can't silently propagate into the final answer |
| ASI09 | Human-Agent Trust Exploitation | Approvals show exact payloads, not persuasive summaries; confidence and gaps stated; no pressure language |
| ASI10 | Rogue Agents | Behavior monitoring via traces; budgets; kill switch; agents can't change their own permissions, policies or prompts |

## Design controls (summary)
- **Separate reading from acting:** agents that read untrusted content hand *data* to a planner; actions require a different, privileged path with approval.
- **Structured outputs** (JSON schema) between agents, validated before use.
- **Allow-list egress** for any agent with network access; block rendering of untrusted markdown images and links that could exfiltrate via URL.
- **Quarantine** suspicious content; log `injection_flagged` events.
- **Human-in-the-loop** for irreversible and outbound actions, with timeout = deny.

## Output format
```
## Inventory           # agents, inputs, tools, data, outputs
## Trifecta matrix     # agent × (private data, untrusted content, external comms) → broken leg
## Findings            # by LLM0x / ASI0x with scenario + fix
## Adversarial tests   # added to evals
## Residual risk
```
