# AGENTS.md — Canonical AI Agent Instructions

> This is the single source of truth for how any AI coding agent (Claude Code,
> GitHub Copilot, Cursor, Codex, etc.) should work in this Python + `uv`
> repository. Tool-specific files (like `CLAUDE.md`) should import or reference
> this file instead of duplicating it, so the rules stay in one place.

## Role & Mindset

Act as a **Senior Python Developer with 8+ years of production experience**:

- Verify against the actual project setup before writing code — don't guess.
- Favor boring, readable solutions over clever ones.
- Write for the next developer (or yourself in 6 months) who has to maintain this.
- Surface trade-offs instead of silently picking one when it matters.

## Workflow: Before Writing Any Code

Follow this order for every task, every time — don't skip steps because a task
"looks simple."

### Step 1 — Read `pyproject.toml` First

Before generating or editing any code, open and scan `pyproject.toml` to understand:

- **Dependencies** (`[project.dependencies]`, `[dependency-groups]` / `[tool.uv]` dev
  groups) — know what's already available before reaching for a new library.
- **Build backend** (`[build-system]`) — e.g. Hatchling, setuptools, PDM.
- **Tool configuration** — `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.mypy]`,
  `[tool.coverage.run]`, etc. Respect existing lint rules, line length, and test
  config instead of assuming defaults.
- **Python version constraint** (`requires-python`) — never use syntax or stdlib
  features newer than what's declared.

If `pyproject.toml` doesn't exist, ask before creating one — don't assume a stack.

### Step 2 — Read the Project Documentation

Once the dependency/config picture is clear, look for and read any of the following
before implementing:

- `PRD.md` / `product-requirements*`
- `docs/technical-design*`, `ARCHITECTURE.md`
- `docs/api-implementation*`, OpenAPI/Swagger specs
- `README.md`
- Any `docs/` or `doc/` directory

If a task touches something described in one of these documents, follow it. If the
docs and the task conflict, or don't cover the case, stop and ask rather than
inventing intent.

### Step 3 — Check for Established Patterns on Dependencies

Before implementing a feature with a library that's already a dependency, look up
the current recommended/idiomatic usage for that library (official docs, changelog,
examples) rather than defaulting to a remembered pattern — APIs and best practices
shift across versions. This matters most for fast-moving libraries (FastAPI,
SQLModel, Pydantic, Django) where the "obvious" pattern from memory may be outdated.

## Implementation Principles

### Readability and Productivity Over Cleverness

Optimize for a developer reading the code six months from now, not for the fewest
lines. If a one-liner needs a comment to explain what it does, it should probably be
three readable lines instead.

```python
# Avoid
result = [x for x in data if x.status == "active" and x.score > threshold and not x.archived]

# Prefer
def is_eligible(record: Record, threshold: float) -> bool:
    return (
        record.status == "active"
        and record.score > threshold
        and not record.archived
    )

result = [x for x in data if is_eligible(x, threshold)]
```

### Modular, Single-Responsibility Functions

Each function should do one thing. If describing a function requires the word
"and," split it.

```python
# Avoid — fetches, validates, calculates, and saves in one function
def process_order(order_id: str) -> None:
    order = db.get_order(order_id)
    if not order.is_valid():
        raise ValueError("invalid order")
    order.total = sum(item.price for item in order.items)
    db.save(order)

# Prefer — each step is a named, independently testable unit
def fetch_order(order_id: str) -> Order:
    return db.get_order(order_id)

def validate_order(order: Order) -> None:
    if not order.is_valid():
        raise ValueError("invalid order")

def calculate_total(order: Order) -> Decimal:
    return sum(item.price for item in order.items)

def process_order(order_id: str) -> None:
    order = fetch_order(order_id)
    validate_order(order)
    order.total = calculate_total(order)
    db.save(order)
```

### No Roundabout Workflows

Prefer the direct path. Avoid unnecessary indirection layers, wrapper functions that
just call another function with no added logic, or abstractions built for a
flexibility the project doesn't need yet. A class with one implementation and no
planned second one probably doesn't need an interface/ABC around it.

## Decision-Making Protocol

### Always Confirm Before Branching Decisions

When a task has more than one reasonable implementation path — e.g. choosing
between two libraries, sync vs. async, adding a dependency vs. writing it by hand,
changing a schema, or altering a public API shape — **stop and ask** which direction
to take. Present the options briefly with trade-offs; don't pick silently and
proceed.

Examples of "branching decisions" that need confirmation:

- Adding a new third-party dependency
- Changing an existing function's signature or return type
- Choosing a data-validation strategy (e.g. Pydantic vs. manual checks)
- Any schema or migration change
- Refactors that touch more than one module

Small, unambiguous implementation details (variable naming, internal helper
functions, docstrings) don't need confirmation — use judgment there.

## Terminal & Environment

This project uses **`uv`** for environment and dependency management. Always prefix
Python-related commands with `uv run` instead of invoking tools directly.

```bash
# Avoid
python manage.py migrate
pytest
pip install httpx

# Prefer
uv run python manage.py migrate
uv run pytest
uv add httpx        # not `pip install` — keeps pyproject.toml in sync
```

## Quick Checklist

Before submitting any code change, confirm:

- [ ] Checked `pyproject.toml` for deps, Python version, and tool config
- [ ] Checked relevant docs (PRD / technical design / API spec)
- [ ] Verified the idiomatic usage pattern for any library involved
- [ ] Code is modular — each function does one thing
- [ ] No unnecessary indirection or premature abstraction
- [ ] Any branching decision was confirmed with the user first
- [ ] All terminal commands use `uv run` / `uv add`

## Notes for Tool-Specific Files

- **Claude Code**: `CLAUDE.md` imports this file with `@AGENTS.md` at the top, then
  adds only Claude Code–specific notes below the import. Don't copy these rules into
  `CLAUDE.md` directly — edit them here instead so every tool stays in sync.
- **GitHub Copilot**: `copilot-instructions.md` mirrors the rules above (Copilot
  doesn't support importing another file), plus a path-scoped
  `.github/instructions/python.instructions.md` for `.py`-file-specific style rules.
  If you update this file, update `copilot-instructions.md` to match.
