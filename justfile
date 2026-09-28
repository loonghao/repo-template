# Task entry points for the repository.
#
# The quality sessions themselves are defined in noxfile.py / nox_actions/; this
# file is the front door so there is one command to remember. Keep it in sync
# with the [tool.nox.session.*] tables in pyproject.toml.

# List every recipe.
default:
    @just --list

# Install the package together with its development dependencies.
install:
    poetry install --with dev

# Run ruff and mypy.
lint:
    nox -s lint

# Apply the automatic fixes: ruff --fix, ruff format, isort.
lint-fix:
    nox -s lint-fix

# Run the test suite with coverage.
test:
    nox -s pytest

# Build the Sphinx documentation.
docs:
    nox -s docs

# Serve the documentation locally with autoreload.
docs-serve:
    nox -s docs-serve

# The pair CI runs: lint then test.
ci: lint test

# Remove build and test artifacts.
clean:
    -rm -rf dist build .nox .pytest_cache .mypy_cache .ruff_cache htmlcov
    -rm -f coverage.xml coverage.json .coverage
    -find . -type d -name __pycache__ -prune -exec rm -rf {} +
