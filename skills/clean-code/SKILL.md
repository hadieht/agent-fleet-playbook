---
name: clean-code
description: Use whenever you write or change production code in any language, to keep it readable, simple and easy to change (naming, function size, single responsibility, error handling, duplication, comments). Also use when asked to "clean up" code. Don't use for throwaway scripts the user explicitly marked as disposable.
---

# Clean code

Code is read far more often than it's written. Optimize for the next reader, who may be an agent with zero context.

## Iron law
> **Leave every file you touch at least as clean as you found it, and never mix a cleanup with a behavior change in the same step.**

## Procedure
1. **Read before writing.** Find 2–3 nearby examples of the same kind of code and match their conventions: naming, layout, error handling, test style. The project's conventions beat your preferences.
2. **Write the simplest thing that's correct:** no speculative options, layers or abstractions (YAGNI).
3. **Run the checks below** on everything you changed.
4. **Refactor in a separate step** (skill `refactoring-safely`), with tests green before and after.
5. **Run the formatter and linter** the project already uses. Don't introduce new ones without being asked.

## The checks

### Names
- Reveal intent: `elapsedDays`, not `d`; `isEligibleForRefund()`, not `check()`.
- Use one word per concept across the codebase (don't mix `fetch` / `get` / `retrieve` for the same thing).
- Booleans read as questions: `isActive`, `hasAccess`, `canRetry`.
- Name functions with verbs and types or values with nouns. Avoid `Manager`, `Helper`, `Util`, `Data`, `Info` unless the codebase already uses them consistently.
- Name length grows with scope: short in a 3-line lambda, descriptive for public APIs.

### Functions
- Each function does **one thing** at **one level of abstraction**. If describing it needs "and", split it.
- Keep functions short enough to read without scrolling. Around 20–30 lines is a signal to look, not a hard rule.
- Have 0–3 parameters. More suggests a parameter object or a missing concept.
- No boolean flag parameters that switch behavior (`render(true)`); use two functions or an enum.
- Separate commands from queries: a function either changes state or returns information, not both.
- Use guard clauses and early returns instead of deep nesting. Keep nesting to 2 levels or fewer where possible.

### Classes and modules
- Single responsibility: one reason to change.
- High cohesion, low coupling. Depend on abstractions at boundaries (I/O, time, randomness, network), not everywhere.
- Prefer composition over inheritance; keep inheritance shallow.
- Keep data private, and expose behavior rather than raw state.

### Errors
- Fail fast at boundaries: validate input where it enters the system.
- Never swallow exceptions silently. Either handle them meaningfully or let them propagate with context.
- Use exceptions or result types consistently with the codebase, and don't use exceptions for normal control flow.
- Error messages say what failed, with which input, and what to do next.
- Don't return `null` for "no result" when the language offers an option or result type or an empty collection.

### Duplication and simplicity
- Apply the rule of three: tolerate duplication twice, extract on the third occurrence, and only when it's truly the same concept.
- Delete dead code, commented-out code and unused parameters. Version control remembers them.
- Avoid magic numbers and strings; use named constants or enums.
- Prefer plain, boring code over clever code.

### Comments
- Comments explain **why** (intent, constraints, trade-offs, links to tickets or specs), never **what** the code already says.
- Public APIs get doc comments that state the contract: inputs, outputs, errors and side effects.
- `TODO` comments carry an owner or ticket; otherwise do it now or drop it.

## Red flags: stop and fix before returning
- You copied a block and changed one value.
- A function needs a comment to explain *what* it does.
- You added a parameter "for flexibility later".
- A diff mixes formatting churn with logic changes.
- You caught `Exception` / `catch (e) {}` without rethrowing or logging context.
- A name contains `2`, `New`, `Old`, `Temp` or `Final`.

## Rationalizations to reject
| Excuse | Reality |
|---|---|
| "I'll clean it up later" | Later never comes. Clean it now or open a ticket. |
| "It's just a small change" | Small changes are how codebases rot. |
| "The existing code is messy anyway" | Match conventions, but don't add to the mess. |
| "Abstraction makes it reusable" | Unneeded abstraction is cost with no benefit (YAGNI). |
| "Comments make it clear" | Clear names make comments unnecessary. |

## Deeper references
- [reference/code-smells.md](reference/code-smells.md): a catalog of smells and the refactoring that fixes each.
- [reference/design-principles.md](reference/design-principles.md): SOLID, DRY, KISS, YAGNI, Law of Demeter, and when they *don't* apply.

## Checklist
- [ ] Names reveal intent; one word per concept
- [ ] Each function does one thing; no flag arguments
- [ ] No swallowed errors; boundaries validate input
- [ ] No dead or commented-out code; no magic values
- [ ] Formatter and linter clean; conventions match neighbors
- [ ] Cleanup and behavior changes kept in separate steps
