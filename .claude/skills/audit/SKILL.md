---
name: audit
description: Run a full project health audit covering pyproject.toml configuration drift, dependency freshness, and code quality against this project's AGENTS.md principles. Use when the user asks to audit, review, or health-check the project, its config, or its dependencies.
disable-model-invocation: true
allowed-tools: Bash(uv tree *) Bash(uv pip list *) Bash(ruff check *) Bash(mypy *) Read Grep Glob
---

# Project Audit

Run this three-part audit and report findings before changing anything. Do not
auto-fix — every fix is a branching decision per `AGENTS.md` and needs
confirmation first.

## Part 1 — Config Audit (`pyproject.toml`)

1. Read `pyproject.toml` in full.
2. Check `[tool.ruff]` for:
   - Rule codes that no longer exist in the installed Ruff version (dead codes)
   - Glob/exclude patterns whose depth doesn't match the actual directory layout
   - Settings duplicated between `[tool.ruff]` and `[tool.ruff.lint]`, or already
     covered by Ruff's defaults
3. Check `[tool.pytest.ini_options]` for stale paths, unused markers, and
   parallelization settings that don't match actual `pytest-xdist` usage (e.g.
   missing `parallel = true` / `sigterm = true` for coverage file cleanup).
4. Check `[tool.mypy]` / `[tool.coverage.run]` for settings referencing modules
   or paths that no longer exist.
5. Confirm `requires-python` matches the syntax actually used in the codebase
   (e.g. no `match` statements if it allows Python < 3.10).
6. Run `` !`ruff check --statistics` `` and cross-reference against what's
   actually configured vs. actually firing.

## Part 2 — Dependency Audit

1. Run `` !`uv tree` `` to see the full dependency graph.
2. Run `` !`uv pip list --outdated` `` to flag stale packages.
3. Grep the codebase for `import` statements and cross-reference against
   `[project.dependencies]`:
   - Declared dependencies with no matching import anywhere → unused
   - Imports with no matching declared dependency → undeclared/transient
4. Note any dependency that looks abandoned (no release in 2+ years) or has a
   widely known CVE — don't guess at CVE details, only flag what you can verify.

## Part 3 — Code Quality Audit

Spot-check recently modified files (or files the user names) against the
principles in `AGENTS.md`:

- Functions doing more than one job (fetch + validate + save in one function)
- Unnecessary indirection (pass-through wrappers, single-implementation
  interfaces/ABCs)
- Readability — one-liners or comprehensions that need a comment to explain
  themselves
- Missing type hints on public function signatures

## Output Format

Report findings grouped by the three parts above, one line per item:

```
[severity] file:line — issue — suggested fix
```

Severity is one of `critical` (breaks something), `warning` (drift/waste), or
`note` (minor/stylistic). End with a per-severity count, then ask which
findings to act on — don't apply any fix without confirmation.
