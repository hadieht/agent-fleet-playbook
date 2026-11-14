---
name: containers-and-ci
description: Use when writing or reviewing Dockerfiles, container configs, Kubernetes manifests or CI/CD pipelines (GitHub Actions, Azure DevOps, GitLab CI). Covers reproducible builds, small secure images and hardened pipelines. Don't use for application logic.
---

# Containers and CI/CD

## Iron law
> **Builds are reproducible and least-privileged: pinned inputs, no secrets in artifacts, minimal permissions.**

## Dockerfile
- **Multi-stage:** build in an SDK image, run in a minimal runtime image (distroless, `-alpine` or chiseled/`-noble-chiseled` variants for .NET).
- **Pin base images** by version and, for production, by digest: `FROM mcr.microsoft.com/dotnet/aspnet:10.0@sha256:…`.
- **Order layers for caching:** copy dependency manifests (`*.csproj`, `package.json`, `pyproject.toml` + lockfile) → restore → copy source → build.
- **Non-root:** `USER app` (or a numeric UID); never run as root in production.
- **No secrets in layers:** use BuildKit secrets (`RUN --mount=type=secret,id=npmrc …`), never `ARG`/`ENV` for secrets. Every layer is readable.
- **`.dockerignore`:** exclude `.git`, `bin/`, `obj/`, `node_modules`, `.env`, test data.
- **One process per container;** `HEALTHCHECK` or orchestrator probes; `exec`-form `ENTRYPOINT ["dotnet","App.dll"]` so signals reach the process.
- **Scan images** (`trivy image`, `grype`, `docker scout`) and fail CI on critical vulnerabilities that have fixes.

## Kubernetes / runtime
- `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, drop `ALL` capabilities.
- Resource `requests` and `limits` on every container.
- Liveness, readiness and startup probes that check real dependencies appropriately (readiness can check them; liveness shouldn't, to avoid cascading restarts).
- Secrets from a secret store (CSI driver, External Secrets), never plain manifests in git.
- `NetworkPolicy` default-deny; least-privilege RBAC; no `cluster-admin` for workloads.

## CI pipelines (GitHub Actions specifics; same ideas elsewhere)
- **Pin third-party actions to a full commit SHA** (`uses: actions/checkout@<40-char-sha> # v7.0.1`). Tags are mutable; SHAs aren't. Let Dependabot or Renovate bump them.
- **Least privilege:** top-level `permissions: contents: read`, and grant more per job only where needed.
- **Script injection:** never interpolate untrusted context directly into `run:`:
  ```yaml
  # BAD:  run: echo "${{ github.event.issue.title }}"
  env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "$TITLE"
  ```
- **`pull_request_target` and `workflow_run`** run with secrets in the base repo context. Never check out and execute PR head code in them.
- **Cloud credentials via OIDC** (short-lived federated tokens), not long-lived secrets.
- **Secrets:** only in the jobs that need them; masked; never echoed; never passed to steps that run untrusted code.
- **Self-hosted runners:** never for public repos; ephemeral where possible.
- **Caching:** key caches on lockfile hashes; don't cache secrets or build outputs across trust boundaries.
- **Reproducibility:** lockfiles committed; `--locked` / `npm ci` / `dotnet restore --locked-mode`; SDK pinned (`global.json`, `.python-version`, `.nvmrc`).
- **Quality gates:** build → lint/format check → unit tests → integration tests → security scans (SAST, dependency audit, secrets scan, image scan) → package → deploy (gated by environment approval).
- **Artifacts and provenance:** generate an SBOM; sign artifacts and images (Sigstore/cosign); publish build provenance attestations where supported.

## Deployment
- Environment protection rules or manual approval for production.
- Progressive rollout (canary or blue-green) with automatic rollback on health or SLO failure.
- Database migrations run as a separate, observable step (skill `database-design`).

## Review checklist
- [ ] Base images and actions pinned (digest / SHA)
- [ ] Runs as non-root; minimal runtime image
- [ ] No secrets in images, logs or `run:` interpolation
- [ ] `permissions:` minimal; OIDC for cloud
- [ ] No untrusted code executed with secrets (`pull_request_target`)
- [ ] Lockfiles and locked restore; SDK pinned
- [ ] Scans (deps, secrets, image) gate the pipeline
