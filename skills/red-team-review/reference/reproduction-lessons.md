# Reproduction lessons for code and security red-teaming

How to turn a suspected weakness into evidence, on hosts that also run real workloads.

## Boundaries
- On a shared or dev host where the owner's real resources run on the same daemon or database, **probe only resources you created**, under a test prefix and label (e.g. `<test-prefix>-*` with label `<project>.test=true`). Never act on the owner's resources.
- A **read-only census** of real resources is allowed and is strong evidence (e.g. counting orphaned volumes), as long as nothing is changed.
- Don't pull images or packages the environment rules forbid. If tests fail because a fixture image is missing, report that; don't "fix" it by pulling.
- Clean up afterwards and prove it: list containers, volumes, networks and images **by your label**; the count must be 0.

## Procedure
1. Read the diff (`git diff`, plus `git status` for new files) and the spec or decision record it amends.
2. Write the probe as a **real test** in the project's own test harness (`<feature>-redteam` test file).
3. **Run it before any fix**, so the critique can quote the real failure lines.
4. If a fix is made (by the builder, not by you), re-run the probe and the project's full gates.
5. **Prove the test discriminates:** revert the fix locally, watch the test fail, restore it.
6. Give each test case its own resource label, so one case's bulk cleanup can't delete another's fixtures.

## Weakness patterns worth hunting
- **Safety checks built on filtered views.** A check like "is this in use?" or "does this project exist?" that reads a list filtered by visibility or scope is wrong whenever a filter is active. Safety must read the unfiltered source. Always add a second test instance with the filter switched on.
- **"Not discovered" isn't "deleted".** Discovery may only see items with live members or a registry entry. Simulate the torn-down-but-still-has-data case explicitly.
- **Exception filters, not just try/catch.** `catch (... when e is A or B)` lists that miss one exception type, or that rely on cancellation being excluded, leave jobs stuck in "running" or kill background loops that never restart.
- **Single-flight caches.** A "fresh" read can join a fetch that started before the write you're checking; invalidation that clears only the cache doesn't help. Look for stale-read windows right after deploys and restarts.
- **Post-deploy windows.** Right after a replace/redeploy, listings may still include the replaced, stopped instances. Health gates that use pre-deploy IDs hit the stale window.
- **Private isn't unreachable.** Internal types and methods can be reached through reflection or test hooks; don't rate a risk lower because a method is "internal".
- **Redaction and validation per call vs per pipeline** (see `api-design/reference/contract-first-port.md`).

## Tooling constraints you may hit
- Some sandboxes block heredocs, inline interpreters (`python -c`, `node -e`), recursive deletes or commands containing cloud-metadata addresses. Write scripts to files, use fresh folder names instead of deleting, and test link-local policy with another address in the same range, never the metadata address.
- Long integration suites can exceed a single command's time limit. Run them in the background and poll.
