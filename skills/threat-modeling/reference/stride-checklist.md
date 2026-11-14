# STRIDE prompts

## Spoofing (authenticity) → control: authentication
- Can anyone call this endpoint, queue or webhook without proving who they are?
- Are webhooks from third parties signature-verified (HMAC + timestamp)?
- Can a user act as another user by changing a header, cookie, claim or ID?
- Service-to-service: mTLS or signed tokens, or just network location?
- Session fixation, credential stuffing, missing MFA for admins?
- Agents: can content an agent reads impersonate the planner or the user ("SYSTEM: …")?

## Tampering (integrity) → control: integrity checks, authorization, signing
- Can client-side values (price, role, user ID, quantity) change server behavior?
- Are messages on queues or files in storage writable by other components?
- Are build artifacts, container images and dependencies verified (digests, signatures)?
- Can an attacker modify data in transit (TLS everywhere? certificate validation on?)
- Mass assignment: can extra JSON fields update protected properties?
- Agents: can memory, notes or retrieval data be poisoned to change future behavior?

## Repudiation (accountability) → control: audit logging
- Are security-relevant actions (login, permission change, payment, delete, export) logged with who, what, when and where?
- Are logs tamper-resistant (append-only, shipped off the host)?
- Can a user deny placing an order or approving an action?
- Agents: is every tool call and approval decision traced?

## Information disclosure (confidentiality) → control: access control, encryption, minimization
- IDOR: can a user read another user's or tenant's object by ID?
- Verbose errors, stack traces, debug endpoints, directory listings?
- Secrets in code, logs, URLs, client bundles, container layers, CI logs?
- Data at rest encrypted; backups protected; PII minimized and masked in logs?
- Caches keyed so one user can't receive another's response?
- Side channels: timing differences in login or token checks, user enumeration via error messages?
- Agents: can an injected prompt make the agent exfiltrate data (send it in a URL, email or tool call)?

## Denial of service (availability) → control: limits, quotas, isolation
- Unbounded inputs: request size, collection length, pagination limit, file size, decompression bombs, regex backtracking?
- Expensive operations reachable anonymously (search, export, report generation, LLM calls)?
- Rate limits per user, IP and tenant? Timeouts on every outbound call? Circuit breakers?
- Resource exhaustion: connection pools, thread pools, disk, queue depth, token budgets?
- Agents: runaway loops, unbounded fan-out, cost explosions?

## Elevation of privilege (authorization) → control: least privilege, authorization checks
- Is authorization checked server-side on **every** request, for **every** object?
- Can a normal user reach admin functions (hidden URLs, missing role checks, GraphQL fields)?
- Injection paths to code execution: SQL, command, template, deserialization, path traversal to writable code locations?
- Do services run with more permissions than needed (cloud IAM wildcards, root containers, DB owner accounts)?
- Agents: can a low-trust agent (reading web content) trigger a high-privilege tool?
