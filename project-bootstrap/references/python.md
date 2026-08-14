# Python setup

## Project + package manager

Prefer `uv` for new projects (fast, manages Python versions and lockfile): `uv init` scaffolds pyproject.toml. Otherwise plain pip + `pyproject.toml`. Detect existing setup from `uv.lock`, `poetry.lock`, `requirements.txt`.

## Format + lint: Ruff

One tool, replaces black + isort + flake8 + pyupgrade:

```bash
uv add --dev ruff   # or: pip install ruff
```

`pyproject.toml`:

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

The contract: `ruff format` (fix) / `ruff format --check` (CI), `ruff check` (lint, `--fix` locally).

## Typecheck: mypy (or pyright)

```toml
[tool.mypy]
strict = true
```

If the codebase isn't typed yet, `strict = true` will drown the user in errors — start with default settings and ratchet up strictness over time, or scope mypy to the directories that are typed.

## Tests

`pytest`. Add `pytest-cov` only if the user asks about coverage.

## Pre-commit: the `pre-commit` framework

This is the ecosystem standard and stores hooks in the repo (`.pre-commit-config.yaml`), so contributors get identical hooks after `pre-commit install`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        pass_filenames: false   # mypy needs the whole project, not staged files
        args: [src]
```

Mypy with `pass_filenames: false` can be slow on big projects — if it exceeds ~10s, move it to `stages: [pre-push]`.

## CI notes

- `astral-sh/setup-uv@v3` (or `actions/setup-python@v5` with `cache: pip`).
- Release: Python CLIs are usually published to PyPI (`uv publish` on tag) and/or as standalone binaries via PyInstaller/`uv tool install`. For a curl install script, build binaries per OS/arch in a matrix job and adapt `assets/install.sh` — see `references/release.md`.
