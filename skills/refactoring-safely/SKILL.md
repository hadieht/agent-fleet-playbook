---
name: refactoring-safely
description: Use when restructuring existing code without changing its behavior (extracting, renaming, moving, splitting, removing duplication, modernizing legacy code). Keeps behavior locked with tests and moves in small reversible steps. Don't use when the goal is to change behavior; that's a feature or fix.
---

# Refactoring safely

## Iron law
> **Refactoring never changes behavior, and it never happens on red.** Tests must be green before you start and after every step.

## Procedure
1. **Lock behavior.** Are there tests covering the code you'll change?
   - Yes → run them; all green.
   - No → write **characterization tests** first: call the code with representative inputs and assert on what it *currently* does, even if that looks wrong. If it looks like a bug, note it but don't fix it in the refactoring.
2. **Name the goal:** which smell are you removing (see `clean-code/reference/code-smells.md`) and why does it matter now?
3. **Take the smallest step:** one rename, one extract, one move.
4. **Run tests** after every step. Commit when green (small commits make bisecting trivial).
5. **Repeat** until the goal is reached. **Stop** when it is. Don't drift into unrelated cleanups.
6. **Behavior changes go separately.** If you found bugs, fix them afterwards as their own change (skill `systematic-debugging`).

## Safe-step catalog
| Step | Notes |
|---|---|
| Rename (variable, function, class, file) | Use IDE or language-server rename, not find-replace |
| Extract function / variable | Name it for intent |
| Inline function / variable | When the indirection adds nothing |
| Move function / field | Toward the data it uses |
| Introduce parameter object / value object | For data clumps and primitive obsession |
| Replace conditional with polymorphism or a lookup table | For repeated type switches |
| Split phase | Separate parsing from processing from output |
| Encapsulate variable / collection | Before changing how it's stored |
| Remove dead code | Confirm no references, including reflection, config and serialization |

## Large-scale techniques
- **Strangler fig:** build the new implementation beside the old one, route traffic gradually, then delete the old.
- **Branch by abstraction:** introduce an interface over the old code, add the new implementation behind it, switch over, then remove the old one.
- **Parallel change (expand/contract):** add the new form, migrate callers, remove the old form. This applies to APIs, schemas and configs.
- **Feature flags** to switch implementations in production with instant rollback.

## Red flags
- "While I'm here, I'll also fix…"
- Tests were edited to pass after a refactoring step. That means behavior changed.
- A single commit touching dozens of files with mixed renames and logic.
- Refactoring code with no tests and no characterization tests.

## Output additions
```
## Refactoring goal
## Steps taken     # each step + test result
## Behavior        # "unchanged — N tests green before and after"
## Found bugs      # noted, not fixed here (ticket or follow-up)
```
