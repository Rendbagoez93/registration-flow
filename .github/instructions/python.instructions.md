---
applyTo: "**/*.py"
---

# Python File Instructions

Applies whenever Copilot is completing, editing, or reviewing a `.py` file in this
repository. This narrows the repo-wide rules in `copilot-instructions.md` to
Python-specific style guidance.

## Before Suggesting Code

- Check `pyproject.toml` for the dependencies, Python version floor
  (`requires-python`), and tool config (`[tool.ruff]`, `[tool.pytest.ini_options]`,
  `[tool.mypy]`) already in place. Match existing conventions instead of
  introducing new ones.
- Prefer a library already listed in `pyproject.toml` over adding a new one for
  the same job.
- Don't suggest syntax newer than `requires-python` allows.

## Style

- Readability over cleverness — if a comprehension or one-liner needs a comment
  to explain itself, break it into named steps instead.
- One function, one job. Split any function that fetches, validates, transforms,
  and saves in a single body into separate, named steps.
- No unnecessary indirection: avoid wrapper functions with no added logic, and
  skip interfaces/ABCs for classes with a single implementation.
- Use type hints on function signatures.
- Follow the project's Ruff/mypy configuration rather than a personal style
  preference.

```python
# Avoid
def handle(x):
    return [i for i in x if i.status == "active" and i.score > 0.5]

# Prefer
def is_eligible(record: Record) -> bool:
    return record.status == "active" and record.score > 0.5

def filter_eligible(records: list[Record]) -> list[Record]:
    return [r for r in records if is_eligible(r)]
```

## Commands

This project uses `uv`. Suggest `uv run pytest`, `uv run python ...`, and
`uv add <package>` — never bare `python`, `pytest`, or `pip install`.

## When Unsure

If there's more than one reasonable way to implement something (new dependency
vs. hand-rolled, sync vs. async, a changed function signature), flag the options
in a comment or chat response instead of silently picking one.
