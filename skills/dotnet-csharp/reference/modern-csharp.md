# Modern C# idioms

Use features the project's `LangVersion` supports. Don't rewrite working code just to use a newer feature.

## Types and data
- **Records** for immutable data: `public sealed record OrderCreated(OrderId Id, Money Total);`. Use `with` expressions for copies. Use `record struct` for small value types.
- **Value objects** instead of primitives: `readonly record struct OrderId(Guid Value);`, so you can't pass a `CustomerId` where an `OrderId` is expected.
- **`required` members** (C# 11) for mandatory init-only properties.
- **Primary constructors** (C# 12) for DI-heavy services: `public sealed class OrderService(IOrderRepository repo, TimeProvider clock)`. Parameters are captured, mutable and not `readonly`, so assign to `readonly` fields if mutation would be a bug.
- **Collection expressions** (C# 12): `int[] xs = [1, 2, 3];`, `List<string> names = [];`, spread `[..a, ..b]`.
- **`sealed` by default** for classes not designed for inheritance. It's clearer and enables devirtualization.
- **`file`-scoped types** for helpers that shouldn't leak outside a file.
- Newer language versions add features like `params` collections and `System.Threading.Lock` (C# 13), and extension members, the `field` keyword and null-conditional assignment (C# 14). Use them only when `LangVersion` allows.

## Nullability
- Enable it project-wide (`<Nullable>enable</Nullable>`).
- Validate at boundaries (API input, deserialization, config), then trust the types inside.
- Use `[NotNullWhen(true)]`, `[MaybeNullWhen(false)]` and `[MemberNotNull]` on Try-pattern methods.
- Never sprinkle `!`. Each use is a claim you should be able to justify in a comment.

## Pattern matching
```csharp
decimal Fee(Payment p) => p switch
{
    { Method: PaymentMethod.Card, Amount: > 1000m } => 0m,
    { Method: PaymentMethod.Card }                  => p.Amount * 0.029m,
    { Method: PaymentMethod.BankTransfer }          => 0.50m,
    _ => throw new UnreachableException($"Unknown method {p.Method}")
};
```
- Exhaustive `switch` expressions over enums and closed hierarchies; throw `UnreachableException` for impossible defaults.
- List patterns `[first, .., last]` and property patterns instead of manual index or null checks.

## Async
- Return `Task` / `Task<T>`; use `ValueTask` only on proven hot paths, and never await a `ValueTask` twice.
- **Pass `CancellationToken`** to every async API, and accept one in your own async methods (last parameter).
- Libraries: `ConfigureAwait(false)`. App code (ASP.NET Core) doesn't need it.
- `await foreach` with `IAsyncEnumerable<T>` for streaming; `Channel<T>` for producer-consumer.
- `Task.WhenAll` for independent concurrent I/O; bound concurrency with `Parallel.ForEachAsync(..., new ParallelOptions { MaxDegreeOfParallelism = n })` or `SemaphoreSlim`.
- Never: `async void`, `.Result`, `.Wait()`, `GetAwaiter().GetResult()` in request paths, fire-and-forget without error handling (use a hosted service or background queue).
- Timeouts: `CancellationTokenSource.CancelAfter`, or `WaitAsync(timeout, ct)`.

## Collections and LINQ
- Expose `IReadOnlyList<T>` / `IReadOnlyCollection<T>` / `IEnumerable<T>`, never mutable `List<T>` fields.
- Watch for **multiple enumeration** of `IEnumerable<T>` (deferred execution). Materialize once with `ToList()` / `ToArray()` when needed.
- `FrozenDictionary` / `FrozenSet` (.NET 8+) for read-mostly lookup tables built once.
- `Dictionary.TryGetValue` instead of `ContainsKey` + indexer.
- Avoid LINQ in tight, hot loops (allocations); it's fine everywhere else for clarity.

## Errors and results
- Exceptions for exceptional cases; a `Result<T>` / `OneOf` style only if the codebase already uses it consistently.
- Guard helpers: `ArgumentNullException.ThrowIfNull(x)`, `ArgumentException.ThrowIfNullOrWhiteSpace(s)`, `ArgumentOutOfRangeException.ThrowIfNegativeOrZero(n)`.
- Preserve stack traces: `throw;` not `throw ex;`. Wrap with context: `throw new OrderProcessingException($"Order {id}", ex);`.

## Resource management
- `using` declarations (`using var conn = …;`) and `await using` for `IAsyncDisposable`.
- Implement `IDisposable` only when you own unmanaged resources or disposables; prefer `SafeHandle`.

## Strings
- `StringComparison.Ordinal` / `OrdinalIgnoreCase` for identifiers, keys and protocol strings; culture-aware comparisons only for user-facing text.
- Interpolated strings for building text (not for log messages; use templates there).
- Use `string.IsNullOrWhiteSpace` and the raw string literals `"""…"""` for JSON and SQL in tests.
- `[GeneratedRegex]` source-generated regexes; always set a timeout or use `RegexOptions.NonBacktracking` for untrusted input.
