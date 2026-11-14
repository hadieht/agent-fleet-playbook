# Code smells → refactorings

A smell is a hint, not a verdict. Fix a smell only when it hurts readability or changeability, and only with tests green before and after.

| Smell | How to recognize it | Refactoring |
|---|---|---|
| **Long function** | Scrolls; several comment-separated sections | Extract Function; Replace Temp with Query; Decompose Conditional |
| **Large class / god object** | Many unrelated fields; name ends in Manager/Service/Helper | Extract Class; Extract Interface; split by responsibility |
| **Long parameter list** | More than 3–4 params; same group passed together | Introduce Parameter Object; Preserve Whole Object |
| **Data clumps** | The same 3 fields travel together everywhere | Extract Class / value object |
| **Primitive obsession** | Strings for emails, ints for money, bare IDs | Replace Primitive with Value Object (`Email`, `Money`, `OrderId`) |
| **Duplicated code** | Same logic in 3+ places | Extract Function; Pull Up Method; Form Template Method |
| **Divergent change** | One class changes for many different reasons | Split Phase; Extract Class |
| **Shotgun surgery** | One change touches many classes | Move Function/Field to gather the concept in one place |
| **Feature envy** | A method uses another object's data more than its own | Move Function |
| **Switch on type** | `switch (type)` / `if isinstance` repeated in several places | Replace Conditional with Polymorphism, or a strategy map |
| **Flag argument** | `doThing(true)` | Split into two named functions; or an enum |
| **Speculative generality** | Hooks, params or abstract classes with one user | Inline Class; Remove Parameter; Collapse Hierarchy |
| **Temporary field** | Field only set in some code paths | Extract Class; Introduce Special Case |
| **Message chains** | `a.b().c().d()` | Hide Delegate; Extract Function |
| **Middle man** | Class only forwards calls | Remove Middle Man; Inline |
| **Inappropriate intimacy** | Classes poke at each other's internals | Move Function/Field; Extract Class; encapsulate |
| **Refused bequest** | Subclass ignores most of what it inherits | Replace Subclass with Delegate (composition) |
| **Comments as deodorant** | Comment explains what confusing code does | Rename; Extract Function with an intention-revealing name |
| **Dead code** | Unused functions, params, branches, flags | Remove it (git remembers) |
| **Mutable shared state** | Globals / statics changed from many places | Encapsulate Variable; make immutable; pass explicitly |
| **Deep nesting** | 3+ levels of if/for | Guard clauses; Extract Function; Replace Nested Conditional with Guard Clauses |
| **Boolean blindness** | `return true/false` with unclear meaning | Return a named enum or result type |
| **Hidden I/O** | Business logic calls clock, network or file system directly | Inject the dependency; pass values in (functional core, imperative shell) |

## Test smells

| Smell | Fix |
|---|---|
| Test asserts on mock calls, not outcomes | Assert on observable behavior or state |
| One test, many behaviors (`test_everything`) | One behavior per test; name describes it |
| Logic (if/loops) in tests | Use table-driven or parameterized tests |
| Shared mutable fixtures | Fresh fixture per test; builders and factories |
| Sleep-based waiting | Poll for a condition with a timeout |
| Testing private methods | Test via the public API; extract a class if it needs its own tests |
| Brittle snapshot of everything | Snapshot only the stable, meaningful part |
