# Entity Framework Core

## Modeling
- Configure with `IEntityTypeConfiguration<T>` classes (`modelBuilder.ApplyConfigurationsFromAssembly(...)`), not attributes scattered across the domain.
- Explicit constraints: `.IsRequired()`, `.HasMaxLength()`, `.HasPrecision(19, 4)` for money, unique indexes `.HasIndex(x => x.Email).IsUnique()`.
- Value objects via owned types or complex types; strongly typed IDs via value converters.
- Concurrency token on aggregates edited by users: `builder.Property(x => x.Version).IsRowVersion()` (SQL Server) or a concurrency-token column, and handle `DbUpdateConcurrencyException` → `409`.
- Avoid lazy loading proxies (hidden N+1). Load explicitly.

## Queries
- **Read paths:** `AsNoTracking()` and **project** to DTOs with `Select`. Load only what you need:
```csharp
var page = await db.Orders.AsNoTracking()
    .Where(o => o.CustomerId == customerId && o.CreatedAt < cursor)
    .OrderByDescending(o => o.CreatedAt)
    .Take(50)
    .Select(o => new OrderSummary(o.Id, o.Total, o.Status))
    .ToListAsync(ct);
```
- **N+1:** a loop that queries per item, or navigation access after materialization. Use projection or `Include`. Use `AsSplitQuery()` when multiple collection includes cause cartesian explosion.
- **Bulk changes:** `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF7+) instead of loading entities just to change a field. Note they bypass the change tracker and `SaveChanges` interceptors.
- **Raw SQL:** `FromSql($"SELECT … WHERE Id = {id}")` and `ExecuteSql($"…")` **parameterize** interpolated values. **`FromSqlRaw` / `ExecuteSqlRaw` with concatenated or interpolated user input is SQL injection.** Use them only with constant SQL plus explicit `DbParameter`s.
- Always pass the `CancellationToken` to `ToListAsync`, `FirstOrDefaultAsync`, `SaveChangesAsync`.
- Watch client evaluation: functions EF can't translate throw at runtime. Test queries against a real provider.
- Check generated SQL during development with `ToQueryString()` or logging at `Information` for `Microsoft.EntityFrameworkCore.Database.Command`.

## DbContext
- Scoped lifetime (one per request or unit of work). It's **not thread-safe**, so never run parallel queries on the same instance.
- `AddDbContextPool` for high-throughput apps (no per-request state in the context).
- `EnableSensitiveDataLogging()` and `EnableDetailedErrors()` in development only.
- Keep transactions short; for multiple `SaveChanges` that must be atomic, use `BeginTransactionAsync` together with the execution strategy (`db.Database.CreateExecutionStrategy()`) when retries are enabled.

## Migrations
```bash
dotnet ef migrations add AddOrderStatus
dotnet ef migrations script --idempotent -o artifacts/migration.sql   # READ THIS SQL
dotnet ef migrations bundle                                           # self-contained migrator for CI/CD
```
- **Review the generated SQL every time.** Look for table rebuilds, data loss (dropped or renamed columns that EF scaffolds as drop + add), long locks.
- Renames: EF may generate drop + add. Edit the migration to use `RenameColumn` when you mean a rename.
- Follow expand → migrate → contract for zero-downtime (skill `database-design`).
- Don't call `Database.Migrate()` at app startup in multi-instance production. Run migrations as a separate deployment step.
- Data migrations (backfills) go in batches, often outside EF migrations for large tables.

## Performance
- Index the columns you filter, join and sort on (`HasIndex`). Check with the actual execution plan.
- Compiled queries (`EF.CompileAsyncQuery`) for very hot queries; compiled models for large models with slow startup.
- Avoid `Include` chains that pull huge graphs. Project instead.
- `AsAsyncEnumerable()` to stream large result sets instead of buffering.

## Testing
- Use the **real provider** in a container (Testcontainers for SQL Server or PostgreSQL) for repository and query tests. The InMemory provider doesn't enforce relational behavior (constraints, transactions, SQL translation).
- SQLite in-memory is closer but still differs from SQL Server and PostgreSQL. Use it only when the queries are portable.
- Reset state per test: transaction rollback, Respawn, or a fresh database per test class.
