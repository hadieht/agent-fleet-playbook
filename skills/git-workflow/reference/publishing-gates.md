# Publishing gates: before a push to a shared or public remote

Pushing is a gated action (`approval-gating`). This is what to check before you ask for that approval, and how to publish safely once you have it.

## 1. Scrub host-specific data
Workers often run read-only checks on the real host and paste real names into reports, docs and fixtures. Before **every** commit to a public repo, grep the staged tree, including new untracked docs and review files, for:
- hostnames, LAN / VPN IPs and subnets
- real container, volume, project and usernames
- absolute home-directory paths
- the commit author's email (`git log --format='%an <%ae>'`)

Replace them with generic names, then grep again. Keep the term list in a gitignored local folder, never in the repo.

## 2. Secret scan, with proof that it's narrow
- Scan the **full history**, not just the last commit: `gitleaks git <repo>` (or your scanner's equivalent). CI needs `fetch-depth: 0` to see the history.
- Repos that test redaction or secret handling contain **fake secrets on purpose**. Allowlist them by **exact path plus rule**, never by disabling a rule or allowlisting a whole directory.
- Reproduce the CI result locally first, listing only rule / file / commit / line (values masked).
- **Prove the allowlist is narrow with canaries:** a fake key in a non-allowlisted file and a fake private key inside an allowlisted file must both still be caught.
- Pin the scanner version; "latest" tags break.

## 3. Push only finished work
- Push the last commit of the last **finished and verified** phase, never a half-done HEAD.
- Gate script (kept locally): secret scan + host-term grep over `origin/main..<sha>` + refuse tracked `.env`, `*.db`, key files and the local-only folder. Push only when all pass.

## 4. Rewriting history (only with explicit owner approval)
1. Pause any automatic push job first, or it will re-push the old history.
2. Back up: `git bundle create ../backup.bundle --all && git bundle verify ../backup.bundle`.
3. Rewrite **once, as the last step**. If you rewrite earlier, later commits bring the data back: `git filter-repo --replace-text <terms-file>` for content, `--mailmap` for authors.
4. Prove it: `git log -p --all | grep -c <term>` returns 0. Then `git reflog expire --expire=now --all && git gc --prune=now`, and re-run the tests.
5. `filter-repo` removes `origin`; add it back.
6. Force-push with the lease pinned to the SHA you inspected: `git push --force-with-lease=main:<remote-sha> origin main`. It refuses if anything landed in the meantime.
7. Verify that `git ls-remote origin` equals the local HEAD.
8. **Tell the owner:** the old commits stay fetchable by hash until the host garbage-collects them. If they held private data, the only immediate fixes are the host's support team or deleting and recreating the repository.

## 5. Credentials for the push
- Prefer an SSH **deploy key scoped to one repository** over a personal token. Never accept tokens in chat.
- A successful `ssh -T` proves only **read** access. Confirm write access with `git push --dry-run` before relying on it.
- Some runtimes redact tokens before they reach the shell, so token-based HTTPS then fails with 401. Don't spend iterations debugging that; use the deploy key.
- A deploy key can't set the repo description or topics. Give the owner the text to paste.
- Push prompts that need live user consent abort when the consent times out. Explain what is pending and retry only after the user confirms.
