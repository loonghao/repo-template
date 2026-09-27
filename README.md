# Your Project Name

<div align="center">

[![PyPI version](https://badge.fury.io/py/your-project-name.svg)](https://badge.fury.io/py/your-project-name)
[![Build Status](https://github.com/username/your-project-name/workflows/Build%20and%20Release/badge.svg)](https://github.com/username/your-project-name/actions)
[![Documentation Status](https://readthedocs.org/projects/your-project-name/badge/?version=latest)](https://your-project-name.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/pypi/pyversions/your-project-name.svg)](https://pypi.org/project/your-project-name/)
[![License](https://img.shields.io/github/license/username/your-project-name.svg)](https://github.com/username/your-project-name/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/your-project-name)](https://pepy.tech/project/your-project-name)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen)](https://github.com/astral-sh/ruff)

</div>

Your project description

## From this template to a working repository

Three steps. Everything below is already wired up; you are renaming, not building.

1. **Create the repository and name the package.**
   Click **Use this template**, or run
   `python scripts/apply_template.py ../my-new-repo --name my-new-repo` to drop
   the same contract files into a repository that already exists. Then rename
   `src/your_project_name/` to `src/<your_package>/` and replace
   `your-project-name` / `yourusername` in `pyproject.toml` and this README.

2. **Pin the toolchain and install.**
   Edit `[tools]` in `vx.toml` to the versions your project actually needs, then
   run `just install`. Recipes live in the `justfile`: `just lint`, `just test`,
   `just docs`, `just ci`.

3. **Let the contract gate watch the repository.**
   `.github/workflows/repo-contract.yml` runs the
   [`dcc-mcp` repository contract](https://github.com/dcc-mcp/.github/blob/main/docs/repo-contract.md)
   on every pull request: no build artifacts at the root, a lowercase `justfile`,
   an `AGENTS.md`, resolvable `vx.toml` pins, and a root directory limited to the
   allowlist. It passes as-is — check locally with:

   ```bash
   python <dcc-mcp/.github>/scripts/check_repo_contract.py --root . --profile strict
   ```

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install your-project-name
```

Or with Poetry:

```bash
poetry add your-project-name
```

## Usage

```python
import your_project_name

# Add usage examples here
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/your-project-name.git
cd your-project-name

# Install dependencies with Poetry
poetry install
```

### Testing

```bash
# Everything through the justfile; nox runs underneath
just lint        # ruff + mypy
just lint-fix    # apply the automatic fixes
just test        # pytest with coverage
just ci          # lint + test, the pair CI runs

# Or call nox directly
nox -s pytest
nox -s lint
nox -s lint-fix
```

### Documentation

```bash
just docs         # build the Sphinx documentation
just docs-serve   # serve it with live reloading
```

### Repository contract

```bash
# Check this repository against the dcc-mcp contract
python <dcc-mcp/.github>/scripts/check_repo_contract.py --root . --profile strict
```

`AGENTS.md` is the single source of truth for coding-agent instructions;
`CLAUDE.md`, `GEMINI.md`, `CURSOR.md` and the rest are symlinks to it. Lint
configuration lives in `pyproject.toml` — there is no `.flake8`, `.pylintrc`, or
`.coveragerc`, and adding one back would fail the contract gate.

## License

MIT

## GitHub Actions Configuration

This template uses GitHub Actions for CI/CD. The following workflows are included:

- **Build and Release**: Tests the package on multiple Python versions and operating systems, and publishes to PyPI when a new release is created.
- **Documentation**: Builds and deploys documentation to GitHub Pages.
- **Dependency Review**: Scans dependencies for security vulnerabilities.
- **Scorecards**: Analyzes the security health of the project.

The release workflow uses PyPI's trusted publishing, which means you don't need to set up any PyPI API tokens. Instead, you'll need to configure trusted publishing in your PyPI project settings once you've created your package. See [PyPI's documentation on trusted publishing](https://docs.pypi.org/trusted-publishers/) for more information.

### Release Process

To create a new release:

1. Update the version in `pyproject.toml`
2. Update the `CHANGELOG.md` with the new version and changes
3. Commit and push the changes
4. Create a new tag with the version number (e.g., `1.0.0`)
5. Push the tag to GitHub

```bash
# Example release process
git add pyproject.toml CHANGELOG.md
git commit -m "Release 1.0.0"
git tag 1.0.0
git push && git push --tags
```

The GitHub Actions workflow will automatically build and publish the package to PyPI.
