# Testing in .NET

Follow the test framework the solution already uses (xUnit, NUnit or MSTest). Apply skill `test-driven-development` for the workflow.

## Layout
```
src/Shop.Orders/
tests/Shop.Orders.UnitTests/          # fast, no I/O
tests/Shop.Orders.IntegrationTests/   # real DB/HTTP pipeline via containers
tests/Shop.ArchitectureTests/         # optional: dependency rules
```
- Test names describe behavior: `Refund_IsRejected_WhenAmountExceedsCaptured`.
- Arrange / Act / Assert, with builders for test data (`new OrderBuilder().WithCapturedAmount(10m).Build()`).
- Parameterized tests: xUnit `[Theory]` + `[InlineData]` / `[MemberData]`; NUnit `[TestCase]`; MSTest `[DataRow]`.

## Unit tests
- Test domain logic and services through public APIs.
- Doubles: hand-written fakes for repositories and ports (often clearer than mocks); a mocking library (NSubstitute, Moq) for boundary interfaces only.
- Assert outcomes, not interactions, unless the interaction *is* the behavior (e.g. "an email was sent").
- **Time:** inject `TimeProvider`; in tests use `FakeTimeProvider` (Microsoft.Extensions.TimeProvider.Testing) and `Advance(...)`.
- **Assertions library:** use what the solution already has. Note that FluentAssertions v8+ uses a commercial license; check licensing before adding it. Shouldly or built-in asserts are alternatives.

## Integration tests (ASP.NET Core)
```csharp
public sealed class OrdersApiTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    [Fact]
    public async Task Get_ReturnsNotFound_ForOtherUsersOrder()
    {
        var client = factory.CreateClientFor(user: "alice");
        var bobsOrderId = await factory.SeedOrderFor("bob");

        var res = await client.GetAsync($"/orders/{bobsOrderId}");

        Assert.Equal(HttpStatusCode.NotFound, res.StatusCode); // object-level authz
    }
}
```
- `WebApplicationFactory<Program>` runs the real pipeline in memory. Projects using top-level statements may need `public partial class Program { }` so tests can reference it.
- Replace external dependencies in `ConfigureTestServices`: fake payment gateway, test auth handler. Keep the **real database** via Testcontainers.
- Always include **authorization tests**: anonymous → 401; wrong user → 403/404; right user → 200.
- Test Problem Details shape for error responses.

## What to cover
| Area | Must-have tests |
|---|---|
| Domain rules | Happy path, each invariant violation, boundary values |
| Endpoints | Status codes, validation errors, authz (anonymous / other user / owner) |
| Data access | Queries return the right rows; constraints enforced; concurrency conflict → 409 |
| Serialization | Contract shape (snapshot of the public JSON) for public APIs |
| Background jobs | Idempotency (run twice → same result); cancellation honored |

## Quality tools
- Coverage: `dotnet test --collect:"XPlat Code Coverage"` (coverlet) or Microsoft.Testing.Platform coverage extensions. Use coverage to find gaps, not as a target.
- Mutation testing: Stryker.NET (`dotnet stryker`) to find weak assertions.
- Architecture rules: NetArchTest or ArchUnitNET (e.g. "Domain doesn't reference Infrastructure").
- Flaky tests: run with `--blame` and repeated runs; fix shared state, time and ordering issues; never just add retries.
