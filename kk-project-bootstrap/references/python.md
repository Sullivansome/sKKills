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
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

Ruff infers its target version from `[project] requires-python`; set `target-version` only when that field is absent, and keep it consistent with the supported minimum.

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
  - repo: local
    hooks:
      - id: ruff-check
        name: Ruff lint
        entry: uv run --locked ruff check
        language: system
        types_or: [python, pyi]
      - id: ruff-format
        name: Ruff format check
        entry: uv run --locked ruff format --check
        language: system
        types_or: [python, pyi]
```

These hooks use the same locked tools as CI. Adapt the launcher for an existing Poetry/pip environment. Run whole-project mypy in CI or pre-push; add it to pre-commit only if measured fast enough. Remote hook environments are an alternative, but their versions and typing dependencies must match the project.

## CI notes

- `astral-sh/setup-uv@v10.2.0` (or `actions/setup-python@v7` with `cache: pip`).
- Release: preserve the agreed trigger and channel. Python CLIs can be published to PyPI with `uv publish` from a protected job using Trusted Publishing (OIDC, with PyPI's attestations) rather than a long-lived token, and installed with `uv tool install`, or packaged as standalone binaries with tools such as PyInstaller. For a curl install script, build binaries per OS/arch in a matrix job and adapt [assets/install.sh](../assets/install.sh) — see [references/release.md](release.md).
