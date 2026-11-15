# Recovery playbook for long-running cards

Lessons from multi-phase builds run as serial card chains. Each one cost at least one wasted run before it was written down.

## Budget-exhausted card
1. **Verify the state yourself.** `git status` (clean tree?), `git log --oneline` (which commits landed?), re-run the gates (build + tests). Check leftover test resources by label and creation time; pre-existing fixtures aren't the run's.
2. **Adjudicate open questions against the code.** Reference docs and your own brief can be wrong; the worker's push-back is often right. Answer each question in a comment.
3. **Post the resume brief** as a comment (format in `SKILL.md` §5).
4. **Unblock.** The next run's context carries the full comment thread, so there's no need to re-brief.

## Interface / implementation drift in partial work
Symptoms: duplicate DTOs in two layers, an interface and its implementation returning different types, half-wired services. The partial work is a liability, not a head start.
1. Save everything on `salvage-<card>-run<N>`, with a commit message saying it's broken and must not be built on.
2. Reset the main branch to the last coherent, tested commit.
3. Verify that baseline with a non-incremental build (incremental builds hide errors) and the full test suite.
4. Re-scope into serial cards that each fit one run (≤3 must-fix items each, with their regression tests). If a later phase already depends on the old card, add the last new card as an extra parent.
5. Complete the original card with the re-scope summary: commits, what each new card owns, the new parent for downstream work.

## Same-commit rules that prevent the next run's first failure
- Extending an interface? Update every test double that implements it **in the same commit**.
- Adding a service interface? Register it in dependency injection in the same commit, and start the app once. A missing registration often crashes only at host startup, with a cryptic trace.

## After a timeout
- **The worker process may still be alive.** List processes with their elapsed time (`ps -eo pid,etime,args`) and kill survivors **by PID**. Never `pkill -f <pattern>`: it can match your own shell.
- A test-host or build process hours old is a zombie from an earlier run. It holds locks and resources and will stall every new run; a stalled run then looks like a real hang.
- Delete the worker's debug scripts and oversized test-result directories (crash dumps can reach gigabytes and cause disk pressure and false flakes).
- If a file reads differently twice in a row, the tree was mid-write. Re-read before patching.
- Check side effects: test containers, networks and images the worker created, and whether the user's services still run.

## Test hangs and flakes
- A hang right after a change isn't proof the change broke a test. First check: does any test exercise that path *and* expect cancellation? Two builds sharing one output folder? Huge leftover test-result folders?
- **A full-suite pass can hide an isolated failure, and the reverse.** Before accepting a phase, run each tracked test in isolation too.
- **Shared-tree race:** when you verify a finished phase, the next phase's worker may already be building in the same folder. An error that disappears on a clean re-run is a race; re-run once before escalating.

## Protected instruction files
Files like `AGENTS.md` or `CLAUDE.md` may be write-protected by the runtime and need explicit user consent. A refused write is a consent gate, not a transient error: never retry it. Either get consent and write it yourself, record it as a known gap, or ask the user to add it.

## Resuming after a long gap
- Check for side effects you didn't set up: `git remote -v`, scheduled jobs, what the remote already holds.
- If the user's own resources vanished mid-run, ask whether they changed them before investigating. Once they confirm, tell every pending card not to inspect or depend on them.
- A watcher that re-arms prints a board snapshot. That isn't news; don't report it as a change.

## Runtime notes: Hermes
- Comments: `hermes kanban comment <id> "<body>"` (positional body); add `--max-len` for long notes.
- `hermes` may not be on `PATH` in system cron. Export its bin directory and test with `env -i HOME=$HOME bash -c ...`.
- Use system cron, not an LLM cron job, for mechanical polling (gated pushes, notifications). It costs no tokens. Wrap it in `flock` so runs don't overlap.
- For progress pings, skip the transient `ready` status: rate-limit requeues cycle running → ready → running and flood the chat.
