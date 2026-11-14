---
name: database-design
description: Use when designing schemas, writing or reviewing migrations, writing non-trivial queries, adding indexes, or fixing data-access performance (N+1, slow queries, locking). Covers relational databases primarily. Don't use for in-memory data structures.
---

# Database design and data access

## Iron law
> **Every schema change must be safe to deploy while the old code is still running, and must have a tested way back.**

## Schema design
- **Model the domain first:** entities, relationships, cardinality, invariants. Then normalize to 3NF, and denormalize only for a *measured* read need.
- **Enforce invariants in the database**, not only in code: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys. The database is the last line of defense against bad writes from any client.
- **Keys:** surrogate primary keys (bigint identity or UUIDv7 for distributed or ordered inserts); natural keys as `UNIQUE` constraints.
- **Types:** exact decimal for money (`numeric(19,4)`), `timestamptz` / `datetimeoffset` for instants (store UTC), proper enums or lookup tables, sized strings where the domain has limits.
- **Audit columns** where needed (`created_at`, `updated_at`, `created_by`). Choose soft delete deliberately, since it complicates every query and unique constraint.
- **Personal data:** know which columns hold PII; encrypt or minimize it, and plan for deletion requests.

## Migrations: expand → migrate → contract
1. **Expand:** add new columns or tables as nullable or with defaults; add new indexes *concurrently* where the database supports it.
2. **Deploy code** that writes both old and new forms, and reads the new form with a fallback.
3. **Backfill** in batches (e.g. 1–10k rows per batch with pauses), idempotent and resumable.
4. **Switch reads** to the new form only.
5. **Contract:** drop the old column or table in a *later* release.

**Dangerous operations** (lock or rewrite large tables; check your database's behavior): adding a non-null column without a default on old engines, changing a column type, adding a foreign key without `NOT VALID` then validating, creating an index non-concurrently, renaming columns in use. Always:
- Generate and **read the SQL** a migration tool produces before running it.
- Test the migration on a production-sized copy, and time it.
- Have a down migration or a documented roll-forward fix.

## Queries
- **Parameterize everything.** Never build SQL with string concatenation of input (see `secure-code-review`).
- Select only the columns you need; never `SELECT *` in application code.
- **N+1:** a loop that runs one query per item. Fix it with joins, batch `IN (...)` loads, or eager loading. Detect it with query logging in tests.
- **Pagination:** keyset (`WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 50`) instead of deep `OFFSET`.
- **Transactions:** keep them short; never call external services inside one. Choose the isolation level deliberately.
- **Concurrency:** optimistic (version column) for user edits; `SELECT … FOR UPDATE` / `UPDLOCK` only for short critical sections; consistent lock ordering to avoid deadlocks.
- Bulk operations: set-based `UPDATE`/`DELETE`, not row-by-row loops.

## Indexes
- Index for the queries you actually run: `WHERE`, `JOIN` and `ORDER BY` columns. Put the most selective equality columns first, then range columns.
- Covering or included columns for hot read paths.
- Every foreign key column usually needs an index.
- Each index costs write speed and storage. Remove unused ones (check the database's index usage stats).
- **Verify with the plan:** `EXPLAIN ANALYZE` (PostgreSQL), actual execution plan (SQL Server). Don't guess.

## Performance investigation
1. Find the slow query (slow query log, `pg_stat_statements`, Query Store, APM traces).
2. Get the actual plan. Look for sequential scans on large tables, row-estimate mismatches, sorts spilling to disk, nested loops over large sets.
3. Fix in order: query shape → index → schema → caching. Measure after each change.

## Checklist
- [ ] Constraints enforce invariants (NOT NULL, UNIQUE, FK, CHECK)
- [ ] Migration follows expand/contract; SQL reviewed; tested on realistic data size
- [ ] No string-built SQL; no `SELECT *`
- [ ] No N+1; pagination bounded
- [ ] New queries have supporting indexes, verified with a plan
- [ ] Rollback or roll-forward path documented
