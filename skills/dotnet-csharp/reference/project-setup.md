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
