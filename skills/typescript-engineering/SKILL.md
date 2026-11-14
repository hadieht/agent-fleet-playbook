---
name: typescript-engineering
description: Use for TypeScript or JavaScript work on Node.js backends, web frontends (React and similar), libraries, CLIs and tests. Applies strict typing, runtime validation at boundaries, async correctness, safe DOM and Node patterns, and lockfile hygiene. Don't use for other languages.
---

# TypeScript engineering

## Iron laws
> 1. **`strict: true`, with no `any` in new code.** Use `unknown` and narrow it.
> 2. **Validate all external data at runtime.** Types vanish at runtime, and input from HTTP, JSON, env or storage is `unknown` until parsed.
> 3. **No floating promises.** Every promise is awaited, returned or explicitly handled.

## First, read the project
`package.json` (scripts, engines, package manager), lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`), `tsconfig*.json`, ESLint and Prettier config, test runner. Use the project's package manager and scripts. Never switch package managers or mix lockfiles.

## Compiler settings (new projects)
```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "verbatimModuleSyntax": true,
    "module": "NodeNext", "moduleResolution": "NodeNext", "target": "ES2022",
    "skipLibCheck": true
  }
}
```
Lint with `typescript-eslint` type-checked configs (`strictTypeChecked`), including `no-floating-promises`, `no-misused-promises`, `no-explicit-any`, `switch-exhaustiveness-check`.

## Code rules
- **Model with types:** discriminated unions for states (`{ status: "loading" } | { status: "ok"; data: T } | { status: "error"; error: E }`), exhaustive `switch` with a `never` check, `readonly` arrays and properties, branded types for IDs (`type OrderId = string & { readonly __brand: "OrderId" }`).
- **Parse at boundaries** with a schema library (zod, valibot or similar): `const body = CreateOrder.parse(await req.json())`. Derive types from schemas (`z.infer`).
- **No type assertions** (`as Foo`) to silence errors; use narrowing and type guards. Use `as const` and `satisfies` for literal configs.
- **Errors:** throw `Error` subclasses with context; `catch (e: unknown)` and narrow; never swallow; use `cause` (`new Error("…", { cause: e })`).
- **Async:** `await` everything; `Promise.all` for independent work with bounded concurrency (p-limit) for large fans; `AbortController` + `signal` for timeouts and cancellation on `fetch`.
- **Modules:** small, pure where possible; side effects at the edges; no circular imports.
- **Env/config:** parse `process.env` once into a typed, validated config object at startup; fail fast on missing values.
- **Node specifics:** use `node:` prefixed imports; stream large files; handle `SIGTERM` for graceful shutdown; never block the event loop with sync I/O or heavy CPU in request handlers (use worker threads).

## Security sinks
| Sink | Safe alternative |
|---|---|
| `innerHTML`, `dangerouslySetInnerHTML`, `document.write` with user data | Text nodes / JSX auto-escaping; DOMPurify for unavoidable rich HTML; CSP |
| `eval`, `new Function`, `setTimeout("string")` | Never with input; a real parser |
| `child_process.exec(\`git ${arg}\`)` | `execFile`/`spawn` with an args array; allow-list |
| SQL template strings | Parameterized queries or a query builder/ORM with bound params |
| `path.join(root, userPath)` | `const p = path.resolve(root, name); if (!p.startsWith(path.resolve(root) + path.sep)) reject` |
| Object merge of untrusted JSON (`Object.assign`, deep merge, `obj[key] = v`) | Block `__proto__`, `constructor`, `prototype` keys; `Object.create(null)` maps; `Map` |
| `fetch(userUrl)` server-side | Host allow-list; block private IPs (SSRF); timeouts |
| `Math.random()` for tokens | `crypto.randomUUID()`, `crypto.getRandomValues`, `crypto.randomBytes` |
| JWT verify without algorithm pinning | Pin `algorithms`; verify `iss`, `aud`, `exp` |
| `res.redirect(req.query.next)` | Allow-list or relative paths only |
| Regex on user input with nested quantifiers | Linear-time patterns; input length limits |

## Supply chain
- Commit the lockfile; CI installs with `npm ci` / `pnpm install --frozen-lockfile`.
- Review new dependencies (skill `supply-chain-security`): install scripts, maintainers, weekly downloads, typosquats.
- `npm audit --omit=dev` (or the equivalent) in CI; consider `ignore-scripts` for installs where feasible.

## Tests
- Vitest or Jest (whatever the project uses); Testing Library for UI (query by role and label, not test IDs, where possible); Playwright for a few critical end-to-end flows.
- Fake timers for time; MSW (Mock Service Worker) for HTTP boundaries.
- Type tests (`expectTypeOf`) for public library types.

## Checklist
- [ ] `tsc --noEmit` clean; ESLint clean (type-checked rules)
- [ ] No new `any` / `as` / `@ts-ignore` without a written reason (`@ts-expect-error` with a comment if unavoidable)
- [ ] External input parsed with a schema
- [ ] No floating promises; timeouts on network calls
- [ ] Tests green; lockfile committed; audit clean for new deps
