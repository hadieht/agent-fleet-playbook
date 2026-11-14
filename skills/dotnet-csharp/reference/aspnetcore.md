# ASP.NET Core

## Structure
- Follow the project's existing style (minimal APIs or controllers). For minimal APIs, group endpoints per feature with `MapGroup` and extension methods:
```csharp
public static class OrderEndpoints
{
    public static RouteGroupBuilder MapOrders(this IEndpointRouteBuilder app)
    {
        var g = app.MapGroup("/orders").RequireAuthorization().WithTags("Orders");
        g.MapGet("/{id:guid}", GetById).WithName("GetOrder");
        g.MapPost("/", Create);
        return g;
    }

    static async Task<Results<Ok<OrderDto>, NotFound>> GetById(
        Guid id, IOrderQueries q, CancellationToken ct) =>
        await q.FindAsync(id, ct) is { } o ? TypedResults.Ok(o) : TypedResults.NotFound();
}
```
- Use `TypedResults` + `Results<…>` unions so OpenAPI and tests know every response type.
- **DTOs in, DTOs out.** Never bind to or return EF entities (over-posting, leaking fields, lazy-load surprises).

## Pipeline order (typical)
`UseExceptionHandler` → `UseHsts` (non-dev) → `UseHttpsRedirection` → `UseRouting` (implicit) → `UseCors` → `UseAuthentication` → `UseAuthorization` → `UseRateLimiter` → `UseOutputCache` → endpoints. Order matters: authentication before authorization, and CORS before auth for preflight.

## Errors
```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>(); // IExceptionHandler (.NET 8+)
app.UseExceptionHandler();
app.UseStatusCodePages();
```
- Map domain exceptions to Problem Details (RFC 9457) with stable `type` values; log once at the boundary with the trace ID.
- Never return exception messages or stack traces to clients in production.

## Validation
- Validate every input DTO: DataAnnotations, FluentValidation, or the built-in minimal-API validation (`builder.Services.AddValidation()` in .NET 10+). Return `422`/`400` with field errors.
- Enforce limits: max request body size, max collection lengths, string lengths, pagination `limit` caps.

## Auth
- Default-deny: `builder.Services.AddAuthorizationBuilder().SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());`, then `AllowAnonymous()` only where intended.
- Use policies, not role strings scattered around: `.RequireAuthorization("orders:write")`.
- **Object-level authorization:** check that the *current user may access this specific resource* (resource-based `IAuthorizationService.AuthorizeAsync(user, order, "CanEdit")`). Missing it is the #1 API vulnerability (IDOR / BOLA).
- JWT bearer: keep `ValidateIssuer`, `ValidateAudience`, `ValidateLifetime` and `ValidateIssuerSigningKey` true; small `ClockSkew`; `RequireHttpsMetadata = true`.
- Cookies: `HttpOnly`, `SecurePolicy = Always`, `SameSite = Lax/Strict`; antiforgery for cookie-authenticated form posts.

## Configuration and options
```csharp
builder.Services.AddOptions<PaymentOptions>()
    .BindConfiguration("Payments")
    .ValidateDataAnnotations()
    .ValidateOnStart();
```
- Layered config: appsettings → environment-specific → environment variables → secrets store. Secrets never in committed JSON.

## Outbound HTTP
```csharp
builder.Services.AddHttpClient<PaymentsClient>(c => c.BaseAddress = new(opts.BaseUrl))
    .AddStandardResilienceHandler();   // Microsoft.Extensions.Http.Resilience: retry, timeout, circuit breaker
```
- Typed clients; per-call `CancellationToken`; deserialize with `ReadFromJsonAsync<T>(ct)`.
- If the URL comes from user input, enforce an allow-list (SSRF; see `security.md`).

## Cross-cutting
- **Rate limiting:** `AddRateLimiter` with partitioning by user or IP; return `429`.
- **CORS:** explicit origins; never `AllowAnyOrigin()` together with credentials.
- **Health:** `AddHealthChecks()` with separate `/health/live` (process) and `/health/ready` (dependencies).
- **Observability:** OpenTelemetry for traces, metrics and logs; propagate `traceparent`; include trace IDs in Problem Details.
- **OpenAPI:** the built-in `AddOpenApi()` / `MapOpenApi()` (.NET 9+); keep it accurate with `TypedResults` and `Produces…` metadata.
- **Caching:** output caching for public GETs; `HybridCache` (Microsoft.Extensions.Caching.Hybrid) for app data with stampede protection; never cache per-user data under shared keys.
- **Background work:** `BackgroundService` / hosted services with scoped scopes created per unit of work (`IServiceScopeFactory`); respect `stoppingToken`.

## Checklist
- [ ] Fallback policy requires auth; object-level checks on every resource access
- [ ] DTOs only at the boundary; input validated with limits
- [ ] Problem Details errors; no stack traces leaked
- [ ] Options validated on start; no secrets in config files
- [ ] Typed HttpClient + resilience; CancellationToken everywhere
- [ ] Rate limits, CORS, health checks, telemetry configured
