---
name: python-engineering
description: Use for any Python work, including scripts, services, libraries, data pipelines and tests. Applies modern tooling (uv, ruff, type checking, pytest), typing at boundaries, safe subprocess, file and deserialization handling, and packaging. Don't use for other languages.
---

# Python engineering

## Iron laws
> 1. **Type hints on every public function, and the type checker runs clean.**
> 2. **No `eval`/`exec`, `pickle`/`yaml.load` or `shell=True` on untrusted data.**
> 3. **Reproducible environments:** a lockfile is committed, and the build installs from it.

## First, read the project
`pyproject.toml` (build backend, dependencies, tool config), the lockfile (`uv.lock`, `poetry.lock`, `requirements*.txt`), `.python-version`, CI config, and the test layout. **Use the tools the project already uses.** For new projects, the defaults below apply.

## Tooling (defaults for new projects)
| Job | Tool | Command |
|---|---|---|
| Env + deps + lock | uv | `uv init`, `uv add httpx`, `uv sync --locked`, `uv run …` |
| Lint + format | ruff | `ruff check --fix .`, `ruff format .` |
| Types | pyright or mypy (strict) | `pyright` / `mypy --strict src` |
| Tests | pytest (+ pytest-cov, hypothesis) | `uv run pytest -q` |
| Security | pip-audit, bandit (or ruff `S` rules) | `uv run pip-audit`, `ruff check --select S` |

Typical `pyproject.toml` ruff selection: `select = ["E","F","W","I","B","UP","S","SIM","RUF","PT","TID","C4"]`.

## Code rules
- **Structure:** `src/<package>/` layout; small modules; no logic at import time; `if __name__ == "__main__":` entry points or console scripts.
- **Types:** `from __future__ import annotations` where helpful; `list[str]`, `dict[str, int]`, `X | None`; `Protocol` for duck-typed interfaces; `TypedDict` / `dataclass(frozen=True, slots=True)` for data; avoid `Any`.
- **Boundaries:** parse external input (JSON, env, CLI, HTTP) into validated models once (pydantic or dataclasses + validation), then pass typed objects inward.
- **Errors:** raise specific exceptions; never bare `except:`; `except Exception` only at top-level boundaries, with logging; chain with `raise … from err`.
- **Resources:** `with` for files, locks, connections; `pathlib.Path` for paths; explicit `encoding="utf-8"`.
- **No mutable default arguments** (`def f(x=[])`). Use `None` + create inside.
- **Logging:** `logger = logging.getLogger(__name__)`; lazy formatting `logger.info("paid %s", order_id)`; no `print` in libraries or services.
- **Config:** environment variables via a typed settings object (e.g. pydantic-settings); secrets never in code or committed `.env`.
- **Time:** timezone-aware `datetime.now(tz=UTC)`; inject a clock for testability.
- **Async:** don't mix blocking I/O into `async` code (use `httpx.AsyncClient`, `asyncio.to_thread` for blocking calls); always set timeouts; `asyncio.TaskGroup` (3.11+) for structured concurrency.
- **Performance:** profile first (`py-spy`, `cProfile`); use vectorized libraries (numpy, polars) for data; generators for streaming large inputs.

## Security sinks
| Sink | Safe alternative |
|---|---|
| `subprocess.run(cmd, shell=True)` with input | `subprocess.run(["git", "log", ref], check=True)`; validate args; never `shell=True` with user data |
| `eval`, `exec`, `compile` on input | `ast.literal_eval` for literals; a real parser |
| `pickle.loads`, `marshal`, `shelve` on untrusted data | JSON + schema validation |
| `yaml.load` | `yaml.safe_load` |
| SQL via f-strings | DB-API parameters (`cursor.execute("… WHERE id = %s", (id,))`), SQLAlchemy bound params |
| `open(base / user_path)` | `p = (base / name).resolve(); p.is_relative_to(base.resolve())` check |
| `requests.get(user_url)` | Host allow-list; block private IPs (SSRF); timeouts always |
| `random` for tokens | `secrets.token_urlsafe()`, `secrets.compare_digest()` |
| `xml.etree` on untrusted XML | `defusedxml` |
| `tarfile.extractall` | `extractall(filter="data")` (3.12+) or validate member paths |
| Jinja2 HTML templates | `autoescape=True` (or `select_autoescape`) |

## Tests (with skill `test-driven-development`)
- `tests/` mirrors `src/`; plain `assert`; fixtures for setup; `@pytest.mark.parametrize` for tables.
- `tmp_path` for files; `monkeypatch` for env vars; `freezegun` / `time-machine` or an injected clock for time.
- `hypothesis` for property-based tests on parsers and pure functions.
- Integration tests against real services in containers (testcontainers-python).

## Checklist
- [ ] `ruff check` and `ruff format --check` clean
- [ ] Type checker clean (no new `# type: ignore` without a reason)
- [ ] `pytest` green; output in run log
- [ ] No unsafe sinks; `pip-audit` clean for new dependencies
- [ ] Lockfile updated and committed
