---
name: performance-engineering
description: Use when code must be faster, use less memory or scale further, or when investigating a performance regression or latency problem. Measures before and after every change. Don't use for premature optimization of code that has no performance requirement.
---

# Performance engineering

## Iron law
> **Measure first, change one thing, measure again.** An optimization without before-and-after numbers is a guess and a maintenance cost.

## Procedure
1. **Define the target:** which metric (p50/p95/p99 latency, throughput, memory, CPU, cost), under which load, and what number counts as good enough. No target → no optimization.
2. **Reproduce under realistic conditions:** production-like data volume, a release build, warm-up excluded, the same hardware class.
3. **Profile to find the real bottleneck.** Use the profiler for your stack (`dotnet-trace` / `dotnet-counters`, `py-spy` / `cProfile`, Chrome DevTools / `clinic.js`, `perf`, database query plans). Intuition about hotspots is usually wrong.
4. **Classify the bottleneck:**
   - **I/O bound** (database, network, disk): fewer round trips, batching, caching, async concurrency, better queries and indexes (skill `database-design`).
   - **CPU bound:** better algorithm or data structure first; then avoid repeated work; then micro-optimizations.
   - **Memory or GC bound:** fewer allocations, pooling, streaming instead of loading everything, right-sized collections.
   - **Contention:** locks, connection pools, thread starvation, rate limits.
5. **Change one thing**, re-run the *same* benchmark, and record the numbers.
6. **Stop at the target.** Keep the readable version unless the gain is material.
7. **Guard it:** add a benchmark or performance test to CI for critical paths, and add metrics or alerts in production.

## Order of wins (biggest first)
1. Don't do the work at all (remove it, cache it, compute it once, push it to off-peak).
2. Do less work (better algorithm: O(n²) → O(n log n); indexes; pagination; projections).
3. Do the work in fewer round trips (batching, bulk APIs, joins instead of N+1).
4. Do the work concurrently (async I/O, parallelism for CPU-bound work, within pool limits).
5. Do the work more cheaply (allocation reduction, pooling, span-based or zero-copy APIs).

## Benchmarking rules
- Use a real harness (BenchmarkDotNet, `pytest-benchmark`, `hyperfine`, `k6`/`wrk` for load), never a single stopwatch run.
- Report distributions (mean ± stddev, p95/p99), not single numbers.
- Same machine, same data, release mode, warm-up, multiple iterations.
- Watch for dead-code elimination and caching effects that fake results.

## Caching rules
- Cache only with a clear invalidation story and a bounded size (TTL + max entries).
- Cache keys include everything that affects the result (tenant, user permissions, locale, version).
- Prevent cache stampedes (request coalescing, jittered TTLs).
- Never cache data across users or tenants by mistake. This is a security bug.

## Red flags
- "This should be faster" without numbers.
- Optimizing code that isn't in the profile.
- Adding a cache to hide an N+1 query.
- Parallelizing database calls until the connection pool is exhausted.
- Benchmarks run in debug mode or on a laptop on battery.

## Output format
```
## Target           # metric, load, goal
## Baseline         # numbers + how measured
## Bottleneck       # profiler evidence
## Change           # one change per row
| change | before | after | delta |
## Result vs target
## Guard            # benchmark/test/alert added
```
