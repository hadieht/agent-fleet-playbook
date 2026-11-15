# From an issue to a verified change

Use with `code-build-verify` when the brief is "fix issue #N" or "implement this feature request".

1. **Read the live issue: the body *and* the whole thread.** The body is a snapshot from filing time. The newest comments hold the live state: partial fixes already merged, new root-cause analysis, maintainer decisions, questions aimed at you. Also read the repo's contributor or agent instructions.
2. **Look for existing work before writing any.** Search pull requests by the issue number **and** by at least two keyword or synonym variants of the symptom. Check `git log --oneline -20 -- <relevant files>` for a fix that already landed. Duplicates waste the work.
3. **Validate the premise against the current code.** Reproduce it with a failing test on the default branch. Then ask the second question: is the "bug" deliberate design? `git log -p -S "<symbol>"` shows the original intent; a missing link or a restriction is often the feature. Challenge stale or wrong issue text instead of implementing it blindly.
4. **Define acceptance and risk:** criteria, interfaces, migrations, compatibility, security and privacy, rollout and rollback. Map every criterion to a test or a check.
5. **Fix the class, not the instance.** Once the fix works, search for the same bug shape at sibling call sites and fix them all, or rule each out explicitly. Every changed line traces to the issue; no drive-by cleanup.
6. **Sabotage run:** temporarily restore the old behavior of the exact function under test, confirm the new test **fails**, then restore the fix. A regression test that passes with and without the fix proves nothing.
7. **Gates, then hand off quickly.** Run formatter, lint, type checks and the repo's canonical tests. Opening the PR (which starts CI) is a gated action; request it right away rather than sitting on finished work.
8. **Report CI honestly.** Separate failures your diff caused from pre-existing or infrastructure failures (reproduce on the default branch when unsure; re-run once, and only for real infrastructure flakes). Never say "green", "merged" or "released" without live evidence of that exact state.

## Red flags
- Coding before reading the thread or checking for duplicate PRs.
- "Fixing" behavior the history shows is intentional.
- One call site fixed while its siblings keep the bug.
- Claiming the issue is solved because a PR exists.
