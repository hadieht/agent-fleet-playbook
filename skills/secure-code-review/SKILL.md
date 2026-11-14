---
name: secure-code-review
description: Use for a security-focused review of code, a pull request diff or a whole repository, covering injection, broken access control, authentication, crypto, secrets, insecure defaults, deserialization, SSRF, error handling and dependency risk. Traces untrusted input from source to sink and reports only validated findings with severity. Only for code the user owns or is authorized to assess. Don't use for general code quality (use code-review).
---

# Secure code review

## Iron laws
> 1. **No finding without a source → sink path.** Show where attacker-controlled data enters, how it flows, and where it does damage. Otherwise it's a hypothesis.
> 2. **Every finding passes triage** (skill `security-finding-triage`) before it's reported. False positives destroy trust in the review.
> 3. **Authorized scope only.** Review only code and systems the requester owns or is authorized to assess. Proofs of concept run only in a sandbox, never against production or third-party systems.

## Procedure

### 1. Build context first
- Read the README, architecture docs and any threat model (skill `threat-modeling`).
- Identify the **entry points**: HTTP routes, message handlers, CLI args, file and upload parsers, webhooks, scheduled jobs, deserializers, LLM prompts and tool calls.
- Identify the **trust model**: who is authenticated, what roles and tenants exist, which data is sensitive.
- Map the framework's built-in protections (auto-escaping, ORM parameterization, CSRF middleware) so you know what's protected by default, and where code opts out.

### 2. Choose a mode
| Mode | When | Approach |
|---|---|---|
| **Differential** | PR or diff | Review changed lines *plus* their callers and callees; focus on new entry points, new sinks, changed auth checks, changed defaults |
| **Full audit** | Repo or service | Entry-point-driven: for each entry point, trace inputs to sinks; then sweep the sink categories |
| **Targeted** | A specific concern | Grep for the sink family, then trace back to sources |

### 3. Run tools as leads, not verdicts
SAST (Semgrep, CodeQL), secret scanners (gitleaks), dependency audit (`npm audit`, `pip-audit`, `dotnet list package --vulnerable`, `osv-scanner`), IaC scanners. Every tool hit is a **lead** to triage, not a finding.

### 4. Manual review: source → sink
For each entry point: what input does it take → what validation or normalization happens → where does the input end up? Check every category in [reference/vulnerability-checklist.md](reference/vulnerability-checklist.md) (OWASP Top 10:2025 with CWEs). Pay extra attention to:
- **Access control on every object access** (IDOR/BOLA). This is the most common serious bug in APIs.
- **Insecure defaults and fail-open logic:** auth checks that pass on an exception, `if (config.Missing) allowAll`, debug modes, permissive CORS, disabled TLS validation, default credentials.
- **Sharp edges:** APIs that are easy to misuse (string-built SQL helpers, `Path.Combine` with absolute paths, `yaml.load`, regex on user input).
- **Error handling:** exceptions that skip security checks, leak details, or leave state half-updated (A10:2025).
- **Secrets:** hard-coded keys, secrets in logs, tokens in URLs.
- Language specifics: .NET → `dotnet-csharp/reference/security.md`; Python and TypeScript → the security tables in those skills.

### 5. Triage and variant analysis
For each candidate: run skill `security-finding-triage` (reachability, attacker control, impact, false-positive gates, severity). For each confirmed bug, **search for variants**: the same pattern elsewhere in the codebase.

### 6. Report

## Finding format
```
### [HIGH] IDOR on GET /orders/{id} (CWE-639, A01:2025)
Location: src/Orders/OrderEndpoints.cs:42
Source → sink: route param `id` → OrderQueries.FindAsync(id) → returned to caller; no owner/tenant filter.
Attacker: any authenticated user.
Impact: read any customer's order (name, address, items).
Evidence: integration test `Get_OtherUsersOrder_Returns200` (sandbox) / code path above.
Severity: CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N → <score + rating from the FIRST v4.0 calculator>
Fix: filter by tenant and owner in the query, or resource-based authorization; add a test for 404 on another user's order.
Variants: same pattern in InvoiceEndpoints.cs:31 (also vulnerable), ShipmentEndpoints.cs:28 (safe: filtered).
```

## Output format
```
## Scope & mode            # what was reviewed, commit/ref, what was NOT reviewed
## Entry points & trust model
## Findings                # ranked critical → low, format above
## Rejected leads          # tool hits triaged as false positives + why (brief)
## Hardening suggestions   # non-vulnerability improvements
## Coverage gaps           # areas not reviewed / needing runtime testing
```

## Red flags in your own review
- Reporting scanner output without tracing it.
- "Possible XSS" with no sink and no input path.
- Severity inflated to look thorough, or deflated because the fix is hard.
- No statement of what *wasn't* reviewed.
