# Contract-first port: new backend, unchanged client

Use when you rebuild an existing API in another language or framework while the existing client (web frontend, SDK, mobile app) must keep working **without a single change**.

## Core principle
**The client is the contract.** Read the client's types, API hooks, event names, cookie handling and error parsing, not just the old backend's docs, which drift. Measure every backend decision with one question: *does the unchanged client accept this shape, status and event?*

**Latent bugs:** where the original has a bug and the fix is cheap and doesn't change the wire format, fix it in the port and record it in the progress file. The contract is the wire format, not the bug. Check the original's **source** (not its docs) before deciding whether a quirk is a bug or part of the contract.

## Scaffold phase
1. Copy the client verbatim into the new repo. It is never modified afterwards.
2. Scaffold the backend with strict gates (nullable/strict types, warnings as errors, analyzers, central dependency versions).
3. Implement a minimal skeleton: health endpoint with the **exact** original contract, static client serving, an API description.
4. Verify: backend build with 0 warnings, tests green, **client build green**, client folder unchanged (`git diff --exit-code -- <client-dir>`).

## Wire-format checklist (must match exactly)
| Area | Check |
|---|---|
| Error envelope | Shape, the code table, `details` present or absent |
| Status codes | Every code per error class, including 409 variants and `429` + `Retry-After` |
| Auth | Cookie names and flags (`HttpOnly`, `SameSite`, `Secure`, host prefix), CSRF header name, `Origin` checks, 401 vs 403 semantics, login rate limits |
| JSON | Field casing, `null` vs absent, `null` vs empty array, timestamp format |
| Streaming (SSE / WebSocket) | Event names, payload shapes, heartbeat interval, auth re-validation, back-pressure close, final event |
| Routes | Every path, method, query parameter and request/response shape |
| Storage | Schema ported verbatim from the original migrations; existing data files open unchanged |
| Crypto | Same parameters and output format; unit test: decrypt or verify a value **produced by the original** |

## Phase discipline
- Each phase ends at a coherent, tested checkpoint, and **the client build stays green at every commit**. A broken client build means a contract violation.
- Every phase appends its decisions to the progress file; workers read it first (see `task-board-orchestration`).
- Every worker brief says: "Wire format must be exact; client unchanged. On any doubt, read the original source, then the client's view of the contract."

## Verify parity by testing differentially
- Write **one shared cases file** of inputs. Run it through the original implementation and the port with small harnesses, then diff the outputs.
- **Compare pipelines, not just functions.** The original may also scrub every response, every log line and the error envelope in global hooks; make sure the port has the equivalent before you trust per-call logic.
- Build the port's harness in a scratch folder that references the port's project, with the repo's strict build settings switched off for the harness only.
