# .NET performance and diagnostics

Apply skill `performance-engineering`: target → measure → change one thing → measure.

## Diagnostic tools (`dotnet tool install -g <tool>`)
| Tool | Use |
|---|---|
| `dotnet-counters monitor -p <pid>` | Live CPU, GC, allocation rate, thread pool queue, exceptions/sec, request rate |
| `dotnet-trace collect -p <pid>` | CPU sampling / event traces → open in PerfView, Visual Studio or speedscope |
| `dotnet-dump collect` / `analyze` | Hangs, deadlocks, crashes (`clrstack`, `dumpheap -stat`, `syncblk`) |
| `dotnet-gcdump collect` | Heap snapshot for memory leaks |
| `dotnet-stack report -p <pid>` | Quick managed stacks of all threads |
| BenchmarkDotNet | Micro-benchmarks; always use `[MemoryDiagnoser]` and Release builds |

## Symptoms → likely causes
| Symptom | Check |
|---|---|
| Throughput collapses under load, CPU low | **Thread pool starvation:** sync-over-async (`.Result`), blocking I/O; look at the thread pool queue length in counters |
| High GC % / allocation rate | LINQ in hot loops, boxing, string concatenation, large buffers per request, `params object[]` logging |
| Memory grows forever | Static caches without bounds, event handler leaks, `HttpClient` misuse, captured scopes in singletons |
| Slow endpoints, low CPU | Database (N+1, missing index), external calls without timeouts, lock contention |
| Socket exhaustion | `new HttpClient()` per request; use `IHttpClientFactory` |
| Startup slow | Large EF model (compiled model), reflection-heavy DI scanning, synchronous warmups |

## Allocation-reducing techniques (hot paths only, after profiling)
- `Span<T>` / `ReadOnlySpan<T>` / `Memory<T>` for slicing without copies; `stackalloc` for small buffers.
- `ArrayPool<T>.Shared` for temporary arrays (always return them, in `finally`).
- `StringBuilder` or `string.Create` for building strings in loops; `SearchValues<T>` for repeated character and substring searches (.NET 8+).
- `FrozenDictionary` / `FrozenSet` for static lookups.
- Source generators: `JsonSerializerContext` (System.Text.Json), `[LoggerMessage]`, `[GeneratedRegex]`. They avoid runtime reflection and help Native AOT.
- Pre-size collections when the count is known (`new List<T>(n)`).
- Avoid closures capturing variables in hot lambdas; use `static` lambdas where possible.
- `ValueTask` for methods that usually complete synchronously, and only when measured.

## Async performance
- Bound concurrency for fan-out (`Parallel.ForEachAsync` with `MaxDegreeOfParallelism`, `SemaphoreSlim`). Unbounded `Task.WhenAll` over thousands of items exhausts pools.
- Stream with `IAsyncEnumerable<T>` instead of buffering huge lists.
- `Channel<T>` with bounded capacity for producer-consumer back-pressure.

## Production observability
- OpenTelemetry metrics: request duration histograms (p95/p99), GC, thread pool, `HttpClient` and EF Core instrumentation.
- Custom metrics with `System.Diagnostics.Metrics.Meter`; traces with `ActivitySource`.
- Alert on SLOs (latency or error rate), not on raw CPU.
