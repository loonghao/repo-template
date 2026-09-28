#!/usr/bin/env python3
"""Apply the repository contract files from this template to another repository.

GitHub's "Use this template" button copies the whole repository, which is what you
want for a brand-new project. This script is for the other case: an existing
repository that should adopt the dcc-mcp contract without being rebuilt from
scratch.

It copies the contract files, points the per-tool agent files at ``AGENTS.md``,
and merges the artifact patterns into ``.gitignore``. Nothing is overwritten
unless ``--force`` is passed, and ``--dry-run`` prints the plan first.

Usage:
    python scripts/apply_template.py --dry-run ../some-other-repo
    python scripts/apply_template.py ../some-other-repo

Exit codes:
    0 - the template was applied (or the dry run was clean)
    1 - a file would be overwritten and --force was not passed
    2 - the arguments or paths are unusable
"""

# Import future modules
from __future__ import annotations

# Import built-in modules
import argparse
from pathlib import Path
import re
import sys

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

# Files copied verbatim, with the project-name placeholders substituted.
COPY_FILES = (
    "AGENTS.md",
    "justfile",
    "vx.toml",
    ".github/workflows/repo-contract.yml",
)

# Per-tool agent files that must point at AGENTS.md (contract rule R008).
DERIVED_AGENT_FILES = ("CLAUDE.md", "GEMINI.md", "CURSOR.md", "COPILOT.md", "CODEBUDDY.md")

# Only the patterns under this banner in the template's .gitignore are propagated.
# Everything above it is the template's own housekeeping (poetry.lock, dist/,
# .venv/ ...), which an adopting repository decides for itself.
CONTRACT_SECTION_BANNER = "# --- Repository contract ---"


def derive_name(target: Path) -> tuple[str, str]:
    """Return the (dashed, underscored) forms of the target's project name."""
    raw = target.resolve().name
    dashed = re.sub(r"[_\s]+", "-", raw).strip("-").lower()
    underscored = dashed.replace("-", "_")
    if not underscored or not underscored.isidentifier():
        raise ValueError(f"cannot derive a package name from {raw!r}")
    return dashed, underscored


def substitute(text: str, dashed: str, underscored: str) -> str:
    """Replace the template's placeholders with the target project's names."""
    return text.replace("your-project-name", dashed).replace("your_project_name", underscored)


def contract_patterns(template_gitignore: Path) -> list[str]:
    """Return the artifact patterns listed below the contract banner."""
    lines = template_gitignore.read_text(encoding="utf-8").splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(CONTRACT_SECTION_BANNER):
            start = index
            break
    if start is None:
        return []
    patterns = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            patterns.append(line)
    return patterns


def merge_gitignore(target: Path, template: Path, dry_run: bool) -> list[str]:
    """Append the contract's artifact patterns that the target does not have yet."""
    destination = target / ".gitignore"
    existing = destination.read_text(encoding="utf-8") if destination.is_file() else ""
    have = {line.strip() for line in existing.splitlines()}
    missing = [line for line in contract_patterns(template) if line.strip() not in have]
    if not missing:
        return []
    if dry_run:
        return [f"append {len(missing)} pattern(s) to .gitignore"]
    with destination.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n# Added from loonghao/repo-template\n")
        handle.write("\n".join(missing) + "\n")
    return [f"appended {len(missing)} pattern(s) to .gitignore"]


def link_derived_agent_files(target: Path, dry_run: bool) -> list[str]:
    """Create CLAUDE.md and friends as symlinks to AGENTS.md."""
    actions = []
    if not (target / "AGENTS.md").is_file():
        return actions
    for name in DERIVED_AGENT_FILES:
        path = target / name
        if path.exists() or path.is_symlink():
            continue
        if dry_run:
            actions.append(f"link {name} -> AGENTS.md")
            continue
        try:
            path.symlink_to("AGENTS.md")
            actions.append(f"linked {name} -> AGENTS.md")
        except (OSError, NotImplementedError):
            # Windows without developer mode: fall back to a generated stub that
            # carries the provenance marker the contract accepts.
            path.write_text(
                "<!-- generated from AGENTS.md by scripts/apply_template.py; do not edit -->\n"
                "AGENTS.md\n",
                encoding="utf-8",
            )
            actions.append(f"wrote {name} (symlinks unavailable; edit AGENTS.md instead)")
    return actions


def main(argv: list[str] | None = None) -> int:
    """Apply the contract files to a target repository."""
    parser = argparse.ArgumentParser(
        description="Apply the contract files from loonghao/repo-template to a repository."
    )
    parser.add_argument("target", help="repository to apply the template to")
    parser.add_argument(
        "--template",
        default=str(TEMPLATE_ROOT),
        help=f"template root (default: {TEMPLATE_ROOT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print the plan and change nothing"
    )
    parser.add_argument(
        "--force", action="store_true", help="overwrite files that already exist"
    )
    args = parser.parse_args(argv)

    template = Path(args.template).resolve()
    target = Path(args.target).resolve()
    if not template.is_dir():
        print(f"error: template {template} is not a directory", file=sys.stderr)
        return 2
    if not target.is_dir():
        print(f"error: target {target} is not a directory", file=sys.stderr)
        return 2
    if target == template:
        print("error: the target must not be the template itself", file=sys.stderr)
        return 2

    try:
        dashed, underscored = derive_name(target)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    actions: list[str] = []
    conflicts: list[str] = []
    pending: list[tuple[Path, Path]] = []

    for relative in COPY_FILES:
        source = template / relative
        if not source.is_file():
            conflicts.append(f"{relative}: missing from the template")
            continue
        destination = target / relative
        if destination.exists() and not args.force:
            conflicts.append(f"{relative}: already exists (use --force to overwrite)")
            continue
        actions.append(f"{'overwrite' if destination.exists() else 'write'} {relative}")
        pending.append((source, destination))

    # Resolve every conflict before touching the target. Exiting 1 has to mean
    # that nothing happened, otherwise a later --force run silently builds on
    # half-applied changes the user never saw.
    if conflicts:
        for conflict in conflicts:
            print(f"skip  {conflict}", file=sys.stderr)
        return 1

    if not args.dry_run:
        for source, destination in pending:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                substitute(source.read_text(encoding="utf-8"), dashed, underscored),
                encoding="utf-8",
            )

    actions.extend(merge_gitignore(target, template / ".gitignore", args.dry_run))
    actions.extend(link_derived_agent_files(target, args.dry_run))

    prefix = "would " if args.dry_run else ""
    for action in actions:
        print(f"{prefix}{action}")

    if args.dry_run:
        print("\ndry run: nothing was changed")
        return 0

    print(
        "\nNext steps:\n"
        "  1. Replace the placeholder metadata in pyproject.toml if you copied it,\n"
        "     and rename src/<package>/ to match your project.\n"
        "  2. Run the gate: python <dcc-mcp/.github>/scripts/check_repo_contract.py --root . --profile strict\n"
        "  3. Enable the Repo contract workflow in .github/workflows/repo-contract.yml."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
