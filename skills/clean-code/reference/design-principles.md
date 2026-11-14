# Design principles and when they don't apply

Principles are tools for managing change. Apply one when it reduces the cost of a **likely** change; skip it when it only adds indirection.

## SOLID

| Principle | Means | Apply when | Over-applied looks like |
|---|---|---|---|
| **S**ingle responsibility | One reason to change | A class changes for unrelated reasons (UI + persistence + rules) | Dozens of 5-line classes nobody can navigate |
| **O**pen/closed | Extend behavior without editing stable code | A variation point that *actually* varies (payment providers, export formats) | Plugin architecture for something with one implementation |
| **L**iskov substitution | Subtypes honor the base contract | Any inheritance | n/a: violating it is always a bug (e.g. `Square : Rectangle` breaking `SetWidth`) |
| **I**nterface segregation | Small, role-specific interfaces | Clients use only part of a big interface | One interface per method |
| **D**ependency inversion | Depend on abstractions at boundaries | I/O, time, randomness, external services, for testability | Interfaces for every class "just in case" (`IFoo` with one `Foo`, never mocked) |

## Others

- **DRY.** One authoritative place for each piece of *knowledge*. Two blocks of identical code that represent different concepts aren't duplication; merging them couples unrelated things.
- **KISS.** Choose the simplest design that meets the current requirements.
- **YAGNI.** Don't build for imagined requirements. Make it easy to change instead.
- **Law of Demeter.** Talk to direct collaborators only (`order.Total()`, not `order.Lines.Sum(l => l.Price.Amount)` scattered everywhere).
- **Functional core, imperative shell.** Keep business logic pure (data in, data out), and push I/O to the edges. Pure code is trivial to test.
- **Make illegal states unrepresentable.** Use types (enums, discriminated unions, value objects, non-nullable references) so invalid combinations can't compile.
- **Parse, don't validate.** Convert raw input into a validated type once at the boundary, then pass the typed value inward.
- **Composition over inheritance.** Inheritance for true is-a with shared invariants; composition for everything else.
- **Explicit over implicit.** No hidden global state, magic conventions or surprising side effects.

## Architecture-level heuristics

- **Organize by feature, not by layer,** when the codebase is large (`Orders/`, `Billing/` rather than `Controllers/`, `Services/`, `Repositories/`). Follow existing structure if it's consistent.
- **Dependencies point inward:** domain logic doesn't reference frameworks, databases or HTTP.
- **Stable abstractions:** things many modules depend on should change rarely.
- **Boundaries are where you put interfaces, validation, logging and error translation.**

## Decision rule

Before adding an abstraction, answer: *what concrete, likely change does this make cheaper, and what does it cost every reader today?* If you can't name the change, don't add it.
