---
name: supply-chain-security
description: Use when adding, updating or auditing third-party dependencies (NuGet, npm, PyPI, Go, containers, GitHub Actions, agent skills/plugins/MCP servers), or hardening the build pipeline against supply-chain attacks. Covers known vulnerabilities, package trust signals, typosquatting, install scripts, lockfiles, pinning, SBOMs and provenance. Don't use for first-party code review.
---

# Supply-chain security

## Iron law
> **Every new dependency is code you run with your privileges. Justify it, vet it, pin it.**

## Before adding a dependency
1. **Need:** can the standard library or an existing dependency do this? A 20-line function beats a package for trivial helpers.
2. **Identity:** exact package name and publisher; watch for **typosquats** (`reqeusts`, `colourama`, `Microsoft.Extensions.Logging.Abstracions`) and **dependency confusion** (a public package with the same name as an internal one).
3. **Trust signals** (gather them, don't guess):
   | Signal | Concern if… |
   |---|---|
   | Maintainers / publisher | Single anonymous maintainer for a critical package; recent ownership transfer |
   | Activity | No release in 2+ years with open security issues; or a sudden release after long dormancy |
   | Adoption | Very low downloads for a "popular-sounding" name |
   | Repository | No source repo, or the repo doesn't match the published package |
   | Install-time code | npm `preinstall`/`postinstall` scripts, Python build-time code, MSBuild `.targets` that run tasks |
   | Advisories | Open CVEs/GHSAs (check OSV.dev, GitHub Advisory Database) |
   | License | Incompatible with your distribution model (GPL in proprietary, non-commercial licenses, recent license changes) |
   | Transitive footprint | Pulls in dozens of transitive packages for a small feature |
   | OpenSSF Scorecard | Low score on branch protection, code review, signed releases |
4. **Record** the decision in the output: package, version, why, signals checked.

## Audit commands
```bash
dotnet list package --vulnerable --include-transitive
npm audit --omit=dev              # or: pnpm audit / yarn npm audit
pip-audit                         # or: uv run pip-audit
osv-scanner -r .                  # multi-ecosystem, uses OSV.dev
trivy fs . / trivy image <img>    # deps + OS packages in images
```

## Pinning and reproducibility
- **Lockfiles committed** (`packages.lock.json`, `package-lock.json`/`pnpm-lock.yaml`, `uv.lock`/`poetry.lock`, `go.sum`); CI installs in locked mode.
- **Pin container base images by digest**, and **GitHub Actions by full commit SHA**.
- **Private feeds:** package source mapping (NuGet), scoped registries (`@company:registry=` for npm), `--index-url` with a single trusted proxy for Python. These prevent dependency confusion.
- **Update deliberately:** Dependabot or Renovate with grouped PRs, CI gates, and a short soak time for new releases of critical packages (new versions are a common attack window).

## Provenance and inventory
- Generate an **SBOM** (CycloneDX or SPDX) per release (`dotnet CycloneDX`, `cyclonedx-npm`, `syft`).
- Verify signatures and provenance where ecosystems support it (npm provenance, Sigstore/cosign for images, NuGet signed packages).
- Sign your own artifacts and publish build attestations.

## AI agent ecosystem (skills, plugins, MCP servers, prompts)
- Treat third-party **skills, plugins and MCP servers as executable code plus instructions**: read every file (SKILL.md, scripts, hooks) before installing.
- Watch for instructions that fetch and execute remote content at runtime, request broad tool permissions, exfiltrate data, or auto-load other repositories.
- Pin them to a commit; review diffs on update; prefer official or reputable sources.
- Run them with least privilege (skill `llm-agent-security`).

## Incident: a compromised dependency
1. Identify the affected versions and where they're deployed (SBOM, lockfiles).
2. Pin or roll back to a known-good version; block the bad version in the registry proxy.
3. Assume secrets available to builds and runtime were exposed. **Rotate them.**
4. Look for indicators: unexpected network calls, new files, modified build outputs.
5. Write up the timeline and add detection (alerts on install scripts, new outbound domains).

## Output format
```
## Dependencies reviewed   # name@version, ecosystem, direct/transitive
## Findings                # advisory/trust issue → severity → recommendation
## Decision                # add / update / replace / remove + rationale
## Commands run            # audit output excerpts
```
