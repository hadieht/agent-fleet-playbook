---
name: dotnet-csharp
description: Use for any C# / .NET work, including ASP.NET Core APIs, EF Core data access, worker services, libraries, tests, NuGet, MSBuild, performance and upgrades. Applies modern C# idioms, project hygiene, async correctness and .NET-specific security rules. Load the matching reference file for depth. Don't use for other languages.
---

# .NET and C#

## Iron laws
> 1. **Nullable reference types on, warnings are errors**, and no new suppressions without a written reason.
> 2. **Async all the way:** no `.Result`, `.Wait()` or `async void` (except event handlers), and pass `CancellationToken` through.
> 3. **Never build SQL, shell commands, file paths or HTML from untrusted input by concatenation.**

## First, read the project
1. `global.json` (SDK pin), `*.csproj` (TargetFramework, LangVersion, Nullable), `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, `nuget.config`.
2. Find the test project(s) and how they run (`dotnet test`, Microsoft.Testing.Platform, xUnit / NUnit / MSTest).
3. Match the existing style: minimal APIs vs controllers, MediatR or not, folder-by-feature vs by-layer, primary constructors or not. **Consistency beats the newest idiom.**
4. Run the baseline: `dotnet build -warnaserror` and `dotnet test`. Record the results.

## Route to a reference
| Task | Read |
|---|---|
| Language idioms, nullability, records, pattern matching, async, collections | [reference/modern-csharp.md](reference/modern-csharp.md) |
| Web APIs, middleware, DI, config, auth, errors, resilience, health, OpenAPI | [reference/aspnetcore.md](reference/aspnetcore.md) |
| EF Core: modeling, queries, migrations, concurrency, performance | [reference/efcore.md](reference/efcore.md) |
| Unit, integration and architecture tests; test doubles; time | [reference/testing.md](reference/testing.md) |
| Profiling, allocations, benchmarks, diagnostics tools | [reference/performance-diagnostics.md](reference/performance-diagnostics.md) |
| Security review / secure coding in .NET | [reference/security.md](reference/security.md) |
| Solution setup, analyzers, NuGet, CPM, lockfiles, upgrades | [reference/project-setup.md](reference/project-setup.md) |

## Core rules (always)
- **Target the current LTS** unless the project pins otherwise (.NET 10 is the LTS released Nov 2025; check `dotnet --list-sdks` and the project's `global.json`). Don't upgrade frameworks as a side effect of another task.
- **Nullability:** honor annotations; don't use `!` (the null-forgiving operator) to silence warnings. Fix the flow or validate at the boundary.
- **Immutability by default:** `record` / `record struct` for DTOs and value objects, `init` setters, `readonly` fields, `IReadOnlyList<T>` in public signatures.
- **DI:** constructor injection; correct lifetimes (no scoped services captured in singletons; `DbContext` is scoped); avoid the service-locator pattern (`IServiceProvider.GetService` in business code).
- **Configuration:** strongly typed `IOptions<T>` with `.ValidateDataAnnotations().ValidateOnStart()`; secrets from User Secrets (dev) or a vault (prod), never `appsettings.json` in git.
- **Logging:** `ILogger<T>` with **message templates** (`logger.LogInformation("Order {OrderId} paid", id)`), never string interpolation. Use `[LoggerMessage]` source generation on hot paths. No secrets or PII.
- **Time and randomness:** inject `TimeProvider`; use `RandomNumberGenerator` for anything security-related.
- **HTTP clients:** `IHttpClientFactory` / typed clients plus a resilience handler; never `new HttpClient()` per call.
- **Exceptions:** throw specific exceptions; use guard helpers (`ArgumentNullException.ThrowIfNull`, `ArgumentOutOfRangeException.ThrowIfNegative`); don't catch `Exception` except at the top-level boundary that logs and translates it.
- **Public APIs:** XML doc comments; no breaking changes without a version bump (skill `api-design`).

## Commands
```bash
dotnet build -warnaserror                       # compile + analyzers as errors
dotnet test --no-build                          # run tests
dotnet format --verify-no-changes               # style check (CI)
dotnet list package --vulnerable --include-transitive   # known-vulnerable packages
dotnet list package --outdated                  # update candidates
dotnet ef migrations script --idempotent        # review migration SQL before applying
```

## Red flags in C# code
- `async void`, `.Result`, `.Wait()`, `Task.Run` wrapping I/O inside ASP.NET request handlers
- `catch (Exception) { }`, or `catch` that only logs and continues in business logic
- `new HttpClient()` in a method; `DateTime.Now` in domain logic; `static` mutable state
- `FromSqlRaw($"… {input}")`, `SqlCommand` text built with `+`
- `#pragma warning disable` / `!` sprinkled to silence nullability
- Entities returned directly from API endpoints (over-posting, data leaks)
- `TypeNameHandling` other than `None` in Newtonsoft.Json; any `BinaryFormatter` use

## Checklist
- [ ] Builds with `-warnaserror`; `dotnet format` clean
- [ ] Nullable clean without new `!` or suppressions
- [ ] Async correct; `CancellationToken` passed through
- [ ] DI lifetimes correct; options validated on start
- [ ] Tests added (see `reference/testing.md`); `dotnet test` output in run log
- [ ] No vulnerable packages introduced (`dotnet list package --vulnerable`)
