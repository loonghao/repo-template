# AGENTS.md

Instructions for coding agents working in a repository created from
`loonghao/repo-template`. This file is the single source of truth: `CLAUDE.md`,
`GEMINI.md`, `CURSOR.md` and the other per-tool files are symlinks to it, so edit
this file and never the copies.

## Layout

| Path | Purpose |
|---|---|
| `src/<package>/` | Source. Poetry package, published from here. |
| `tests/` | `pytest` suite. |
| `docs/` | Sphinx documentation. |
| `nox_actions/` | The nox session bodies imported by `noxfile.py`. |
| `justfile` | The task entry points. Prefer `just <recipe>` over raw commands. |
| `vx.toml` | Toolchain pins. `[tools]` only — tasks live in the `justfile`. |
| `pyproject.toml` | Poetry metadata plus ruff, mypy, coverage, nox, and pytest config. |

## Commands

```bash
just install     # install the package with its dev dependencies
just lint        # ruff + mypy
just lint-fix    # ruff --fix, ruff format, isort
just test        # pytest with coverage
just docs        # build the Sphinx docs
just ci          # lint + test, the same pair CI runs
```

`nox` is the engine behind the quality sessions; the `justfile` is the entry
point so there is one command to remember.

## Conventions

- **Python:** typed (`mypy --strict` on the package), docstrings enforced by
  ruff's `D` rules, `ruff format` for formatting. Line length 120.
- **Lint config lives in `pyproject.toml`.** There is no `.flake8`, `.pylintrc`,
  or `.coveragerc` — if you are tempted to add one, put the setting under
  `[tool.ruff]` or `[tool.coverage]` instead.
- **Never commit build artifacts.** `coverage.xml`, `*.o`, `*.pyc`,
  `audit-result.json` and friends are gitignored, and CI rejects them at the
  repository root.
- **No ad-hoc markdown at the root.** Design notes, analyses, and summaries go
  under `docs/`. `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md` are the only
  top-level documents.
- **Releases** are cut by release-please from Conventional Commits. Do not edit
  `CHANGELOG.md` or bump the version by hand.

## CI

- `.github/workflows/repo-contract.yml` checks this repository against the
  `dcc-mcp` repository contract: no root artifacts, lowercase `justfile`,
  `AGENTS.md` present, `vx.toml` pins resolvable, root entries allowlisted.
- Run it locally before pushing:
  ```bash
  python /path/to/dcc-mcp/.github/scripts/check_repo_contract.py --root . --profile strict
  ```
