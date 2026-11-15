---
name: api-design
description: Use when designing, changing or reviewing an HTTP/REST API, RPC interface, webhook or public library API (resources, methods, status codes, errors, pagination, versioning, idempotency, compatibility). Don't use for internal private functions.
---

# API design

## Iron law
> **An API is a promise. Never break a published contract silently.** Additive changes are safe; anything else needs versioning and a migration path.

## Procedure
1. **Start from the consumer:** write 3–5 example requests and responses for the real use cases *before* writing code.
2. **Model resources** as nouns (`/orders/{id}/refunds`), with actions expressed through methods.
3. **Pick methods and status codes** from the tables below.
4. **Define errors** in one consistent format.
5. **Design for scale from day one:** pagination, filtering, rate limits, idempotency.
6. **Write the contract** (OpenAPI, protobuf, or typed interfaces) and generate docs and clients from it.
7. **Run the compatibility check** on every change (below).

## Methods
| Method | Use | Safe | Idempotent |
|---|---|---|---|
| GET | Read | yes | yes |
| POST | Create / non-idempotent action | no | no (make it idempotent with an `Idempotency-Key` header) |
| PUT | Full replace | no | yes |
| PATCH | Partial update | no | not necessarily |
| DELETE | Remove | no | yes |

## Status codes (use precisely)
`200` OK · `201` Created (+ `Location` header) · `202` Accepted (async) · `204` No Content · `400` malformed request · `401` not authenticated · `403` authenticated but not allowed · `404` not found (also when hiding existence from unauthorized callers) · `409` conflict / version mismatch · `412` precondition failed (ETag) · `422` validation failed · `429` rate limited (+ `Retry-After`) · `500` server bug · `503` temporarily unavailable.

## Errors
Use **Problem Details (RFC 9457)**, `application/problem+json`:
```json
{"type":"https://api.example.com/errors/insufficient-funds","title":"Insufficient funds",
 "status":422,"detail":"Balance 30.00 is less than 50.00","instance":"/payments/abc123",
 "errors":{"amount":["must be ≤ balance"]},"traceId":"00-4bf9..."}
```
- Use stable machine-readable `type` values; clients branch on `type`, never on `detail` text.
- Never leak stack traces, SQL or internal hostnames.

## Collections
- **Pagination:** cursor-based (`?cursor=…&limit=50`, response `next_cursor`) for large or changing data; offset only for small, stable sets. Enforce a maximum `limit`.
- **Filtering and sorting:** explicit allow-listed fields (`?status=paid&sort=-created_at`).
- **Sparse fields / expansion** only when there's a measured need.

## Reliability
- **Idempotency keys** on POSTs that create money movement or side effects; store key → response for 24h or more.
- **Optimistic concurrency** with `ETag` + `If-Match` → `412` on a mismatch.
- **Timeouts and retries:** document which operations are safe to retry.
- **Rate limits:** return `429` + `Retry-After`; publish the limits.
- **Async:** `202` + a status resource for long operations; webhooks signed (HMAC) with a timestamp to prevent replay.

## Compatibility
| Safe (additive) | Breaking |
|---|---|
| New endpoint | Removing or renaming a field or endpoint |
| New optional request field | New **required** request field |
| New response field | Changing a type or format (`int` → `string`, date formats) |
| New enum value *if clients were told to tolerate unknowns* | Changing status codes or error `type`s |
| | Changing default behavior or sort order clients rely on |

Breaking change → new version (`/v2/` or a media-type version), a deprecation notice (`Deprecation` and `Sunset` headers), and a migration guide. Run both versions in parallel for a published period.

## Conventions
- JSON field naming: pick one (`camelCase` or `snake_case`) and never mix them.
- Timestamps in RFC 3339, UTC (`2026-11-14T10:02:11Z`). Money as an integer of minor units, or a decimal string with a currency code; never floats.
- IDs are opaque strings; don't expose sequential database IDs if enumeration is a risk.
- Every endpoint is authenticated and authorized unless explicitly public (skill `secure-code-review`).

## Porting an existing API
Keeping the existing client unchanged while you replace the backend? Treat the client as the contract: [reference/contract-first-port.md](reference/contract-first-port.md).

## Review checklist
- [ ] Example requests and responses exist for each use case
- [ ] Correct methods and status codes; Problem Details errors
- [ ] Pagination with a max limit on every collection
- [ ] Idempotency for side-effecting POSTs
- [ ] AuthN and AuthZ on every endpoint; object-level checks (no IDOR)
- [ ] Contract file updated; compatibility check passed
