# Import third-party modules
import nox


def lint(session: nox.Session) -> None:
    session.install("isort", "ruff")
    # The package lives under src/, so passing its name as a path never
    # resolved. Check the repository root instead, matching `lint-fix`.
    session.run("isort", "--check-only", ".")
    session.run("ruff", "check")


def lint_fix(session: nox.Session) -> None:
    session.install("isort", "ruff", "pre-commit", "autoflake")
    session.run("ruff", "check", "--fix")
    session.run("isort", ".")
    session.run("pre-commit", "run", "--all-files")
    session.run("autoflake", "--in-place", "--remove-all-unused-imports", "--remove-unused-variables")
