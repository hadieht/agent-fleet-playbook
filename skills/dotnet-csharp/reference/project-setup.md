# .NET solution setup and hygiene

## Pin the SDK: `global.json`
```json
{ "sdk": { "version": "10.0.100", "rollForward": "latestFeature" } }
```
Use the SDK version your team and CI actually have (`dotnet --list-sdks`).

## Shared build settings: `Directory.Build.props` (solution root)
```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <Deterministic>true</Deterministic>
    <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
    <NuGetAudit>true</NuGetAudit>
    <NuGetAuditMode>all</NuGetAuditMode>
    <NuGetAuditLevel>low</NuGetAuditLevel>
  </PropertyGroup>
</Project>
```
Introduce `TreatWarningsAsErrors` gradually in legacy solutions: fix warnings per project, or use `WarningsAsErrors` for specific IDs first.

## Central Package Management: `Directory.Packages.props`
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Microsoft.EntityFrameworkCore.SqlServer" Version="10.0.0" />
  </ItemGroup>
</Project>
```
Project files then use `<PackageReference Include="…" />` without versions.

## NuGet sources: `nuget.config`
- `<clear />` the inherited sources, add only the feeds you need, and use **`<packageSourceMapping>`** so internal package IDs can only come from the internal feed (this prevents dependency confusion).
- CI restores with `dotnet restore --locked-mode` so lockfile drift fails the build.

## Code style: `.editorconfig`
- Commit one at the root; CI runs `dotnet format --verify-no-changes`.
- Set analyzer severities here (e.g. `dotnet_diagnostic.CA2007.severity = none` for app code where `ConfigureAwait` isn't needed).

## Adding a package (checklist)
1. Is it really needed? Can the BCL do it?
2. Check it with skill `supply-chain-security`: maintainer, downloads, last release, license, open advisories, transitive footprint.
3. Add it centrally; restore; commit the lockfile changes.
4. `dotnet list package --vulnerable --include-transitive` is clean.

## Upgrading .NET versions
1. Read the official "Breaking changes in .NET N" page for every version you cross.
2. Upgrade in a dedicated branch: SDK in `global.json` → `TargetFramework` → packages (Microsoft.* to the matching major) → fix build errors → fix new analyzer warnings.
3. Run the full test suite plus integration tests; compare performance on key endpoints.
4. Update Docker base images and the CI SDK version in the same change.
5. Never mix a framework upgrade with feature work.

## Useful templates and commands
```bash
dotnet new sln -n Shop
dotnet new webapi -n Shop.Api -o src/Shop.Api
dotnet new xunit -n Shop.Api.Tests -o tests/Shop.Api.Tests
dotnet sln add src/Shop.Api/Shop.Api.csproj tests/Shop.Api.Tests/Shop.Api.Tests.csproj
dotnet new editorconfig
dotnet new buildprops        # Directory.Build.props
dotnet new packagesprops     # Directory.Packages.props
dotnet new nugetconfig
```

## First-build pitfalls on a strict scaffold
Each of these failed a first build of a new .NET 10 solution with the settings above.

| Symptom | Cause → fix |
|---|---|
| Scripts or CI can't find `<Name>.sln` | SDK 10 `dotnet new sln` creates **`.slnx`**. Don't hardcode `.sln`; bare `dotnet build` / `dotnet test` find it |
| NU1008 / NU1015 on restore | `dotnet new` templates add `Version="…"` to `PackageReference`. With central package management, strip them; versions live only in `Directory.Packages.props` |
| CA1707 errors on every test | Underscores in test names (`Method_Scenario_Result`). Set `dotnet_diagnostic.CA1707.severity = none` for test projects |
| `var` usage turns into errors | Don't enable IDE0008 if you want `var` style; under warnings-as-errors it fights `csharp_style_var_when_type_is_apparent` |
| NU1903 breaks the build | NuGet audit flags a vulnerable **transitive** package. Pin the patched version in `Directory.Packages.props` (works because of transitive pinning) |
| CS0234 on `Microsoft.AspNetCore.OpenApi` | `AddOpenApi()` / `MapOpenApi()` need an explicit package reference; it isn't in the shared framework |
| `WebApplicationFactory` won't compile in tests | The test project needs `<FrameworkReference Include="Microsoft.AspNetCore.App" />` |
| A reflection test can't see a referenced assembly | Assemblies load lazily; call `Assembly.Load("<Name>")` instead of scanning `AppDomain.CurrentDomain.GetAssemblies()` |
| CS8122 inside a FluentAssertions predicate | Predicates are expression trees, where `is` patterns are illegal. Use `==` / `||` |
| CS8361 in `$"…{cond ? 1 : 0}…"` | The `:` ends the interpolation hole. Write `{(cond ? 1 : 0)}` |
| Minimal-API delegate fails parameter binding at startup | Mark service parameters `[FromServices]` in complex `MapGet`/`MapPost` delegates (streaming endpoints especially) |
| `ASPNETCORE_ENVIRONMENT=Testing` is ignored by `dotnet run` | `launchSettings.json` sets the environment and wins. Use `DOTNET_ENVIRONMENT`, or `--no-launch-profile` |
| Host crashes at startup after a new interface | Missing DI registration. Register in the same commit and run the app once |

**A scaffold is done only when a live process answered:** `dotnet build` with 0 warnings, `dotnet test` green, then start the app and `curl` the health endpoint.
