# Security policy

## Threat model (what we defend against)
1. **Prompt injection** through web pages, emails, documents, issues or tool output, which tries to make an agent act.
2. **Over-privileged agents.** One compromised agent can do everything.
3. **Secret leakage** into prompts, logs, memory, URLs or third-party providers.
4. **Runaway loops** that burn budget or repeat side effects.
5. **Memory poisoning.** False or malicious content stored and reused as fact.
6. **Provider data exposure.** Sensitive data sent to providers that log or train on it.

## Controls
| # | Control | Enforced by |
|---|---|---|
| 1 | Deny-by-default tools, per agent | `tool-permissions.yaml` + runtime tool router |
| 2 | Agents that read untrusted content hold no gated tools and no secrets | invariants in `tool-permissions.yaml` |
| 3 | Untrusted content is wrapped and treated as data | `prompt-injection-defense` skill |
| 4 | Code runs only in a sandbox (container/VM, no host mounts, network off unless the brief needs it) | runtime |
| 5 | Secrets injected per agent at runtime from a secret store; never in files, prompts, memory or logs | runtime + `.gitignore` |
| 6 | Gated actions require human approval | Gatekeeper |
| 7 | Hard budgets and no-progress stop | `budgets.yaml` + `budget-control` skill |
| 8 | Memory needs sources, has a verified/unverified status, and nothing is deleted | Librarian + `knowledge-capture` |
| 9 | One user-facing entry point (the planner); specialists have no public bots or endpoints | deployment |
| 10 | Sensitive data only goes to providers with no-training/no-retention terms | model selection at deploy |
| 11 | Every action traced | `trace.jsonl` |

## Deployment checklist
- [ ] Secrets in a secret manager or `.env` (gitignored), never committed
- [ ] Each agent's credentials are separate and minimally scoped
- [ ] Sandbox image pinned; no host filesystem mounts
- [ ] Only the planner is reachable from messaging platforms
- [ ] Gatekeeper timeout = deny
- [ ] Budget alerts on
- [ ] Prompt-injection test cases in `evals/golden-tasks.yaml` pass
