---
name: git-workflow
description: Use when preparing commits, branches and pull requests. Covers small focused commits, clear messages, clean history, no secrets, and PR descriptions reviewers can act on. Don't use for pushing, merging or force-pushing; those are gated actions that need approval.
---

# Git workflow

## Iron law
> **Every commit is small, builds, passes tests, does one thing and contains no secrets.**

## Commits
- **One logical change per commit.** A rename, a refactoring and a feature are three commits.
- **Builds and tests pass** at every commit, so `git bisect` works.
- **Stage deliberately:** review `git diff --staged` before committing. Never `git add -A` blindly in a repo with untracked files you haven't inspected.
- **Message format** (Conventional Commits style if the repo uses it; otherwise match the history):
  ```
  feat(orders): reject refunds larger than captured amount

  Refunds were validated only against the order total, so partial captures
  could be over-refunded. Validate against captured minus refunded amount.

  Fixes #412
  ```
  - Subject: imperative mood, ≤ 72 chars, no period. Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `build`, `ci`.
  - Body: **why** and the important **how**, wrapped at ~72 chars.
  - Trailers: issue refs; `BREAKING CHANGE:` when applicable; co-author lines if required.

## Branches
- Branch from the up-to-date default branch: `feat/<short-name>`, `fix/<issue>-<short-name>`.
- Keep branches short-lived; rebase or merge from main often to avoid big conflicts.
- Never commit directly to `main`/`master` unless the repo's workflow says so.

## Before every commit: secrets check
- Scan staged changes for keys, tokens, passwords, connection strings and private keys (`gitleaks protect --staged`, or `git diff --staged | grep -iE "key|secret|token|password"`).
- `.env`, credentials files and local settings are in `.gitignore`.
- **If a secret was committed:** treat it as leaked. Rotate it first, *then* clean the history. Removing it from history alone isn't enough once it has been pushed.

## Pull requests
```
## What        # one-paragraph summary
## Why         # problem / ticket link
## How         # key design decisions, alternatives rejected
## Testing     # commands run + results; screenshots for UI
## Risk        # migrations, config, flags, rollback plan
## Checklist   # tests, docs, changelog, no secrets
```
- Keep PRs under ~400 lines of logic where possible. Split stacked PRs for larger work.
- Self-review the diff on the hosting site before requesting review.

## Safety rules
- **Gated (need approval through `approval-gating`):** `push`, `push --force`, merging, deleting remote branches, rewriting published history, changing branch protection.
- Never `--no-verify` to skip hooks. Fix what the hook found.
- Never `reset --hard` or `clean -fd` without first checking what will be lost (`git status`, `git stash list`).
- Prefer `git revert` over history rewriting for anything already shared.
