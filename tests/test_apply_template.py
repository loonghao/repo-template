"""Tests for the repository contract adoption script."""

# Import built-in modules
import importlib.util
from pathlib import Path
import sys

# Import third-party modules
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "apply_template.py"


def load_apply_template():
    """Import scripts/apply_template.py, which lives outside the package."""
    spec = importlib.util.spec_from_file_location("apply_template", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["apply_template"] = module
    spec.loader.exec_module(module)
    return module


apply_template = load_apply_template()

# A template .gitignore that mimics the real one: housekeeping above the banner,
# contract artifact globs below it.
FAKE_TEMPLATE_GITIGNORE = """\
# Distribution / packaging
dist/
build/

# Poetry
poetry.lock

# --- Repository contract ---
# Commented header that must not be copied
*.o
*.exe
*.log
"""


def make_template(tmp_path):
    """Write a minimal template tree and return its root."""
    template = tmp_path / "template"
    (template / ".github" / "workflows").mkdir(parents=True)
    (template / ".gitignore").write_text(FAKE_TEMPLATE_GITIGNORE, encoding="utf-8")
    (template / "AGENTS.md").write_text("Agent instructions.", encoding="utf-8")
    (template / "justfile").write_text("default:\n    @just --list\n", encoding="utf-8")
    (template / "vx.toml").write_text("[tools]\n", encoding="utf-8")
    (template / ".github" / "workflows" / "repo-contract.yml").write_text(
        "name: Repo contract\n", encoding="utf-8"
    )
    return template


def test_contract_patterns_skips_the_templates_own_housekeeping(tmp_path):
    """Only the patterns below the contract banner are propagated."""
    template = make_template(tmp_path)
    patterns = apply_template.contract_patterns(template / ".gitignore")
    assert patterns == ["*.o", "*.exe", "*.log"]
    assert "poetry.lock" not in patterns
    assert "dist/" not in patterns


def test_merge_gitignore_appends_only_the_contract_section(tmp_path):
    """The target keeps its own .gitignore and gains just the artifact globs."""
    template = make_template(tmp_path)
    target = tmp_path / "target"
    target.mkdir()
    (target / ".gitignore").write_text("dist/\n", encoding="utf-8")

    result = apply_template.merge_gitignore(target, template / ".gitignore", False)

    assert result == ["appended 3 pattern(s) to .gitignore"]
    merged = (target / ".gitignore").read_text(encoding="utf-8")
    assert "poetry.lock" not in merged
    assert "*.o" in merged
    assert "*.log" in merged
    # The pre-existing entry is left alone and not duplicated.
    assert merged.count("dist/") == 1


def test_merge_gitignore_is_idempotent(tmp_path):
    """A second run appends nothing."""
    template = make_template(tmp_path)
    target = tmp_path / "target"
    target.mkdir()

    apply_template.merge_gitignore(target, template / ".gitignore", False)
    assert apply_template.merge_gitignore(target, template / ".gitignore", False) == []


def test_conflict_leaves_the_target_completely_untouched(tmp_path):
    """Exit 1 must mean nothing happened, not that the work is half applied."""
    template = make_template(tmp_path)
    target = tmp_path / "target"
    target.mkdir()
    (target / "AGENTS.md").write_text("hand written", encoding="utf-8")
    (target / ".gitignore").write_text("dist/\n", encoding="utf-8")
    before = {path.name for path in target.rglob("*")}

    assert apply_template.main([str(target), "--template", str(template)]) == 1

    after = {path.name for path in target.rglob("*")}
    assert after == before, "a conflicting run must not create files or symlinks"
    assert (target / "justfile").exists() is False
    assert (target / ".gitignore").read_text(encoding="utf-8") == "dist/\n"
    assert (target / "AGENTS.md").read_text(encoding="utf-8") == "hand written"


def test_force_overwrites_and_then_applies_the_rest(tmp_path):
    """With --force the conflicting files are replaced and the rest runs."""
    template = make_template(tmp_path)
    target = tmp_path / "target"
    target.mkdir()
    (target / "AGENTS.md").write_text("hand written", encoding="utf-8")

    assert apply_template.main([str(target), "--template", str(template), "--force"]) == 0

    assert (target / "AGENTS.md").read_text(encoding="utf-8") == "Agent instructions."
    assert (target / "justfile").is_file()
    assert (target / "CLAUDE.md").is_file()


def test_dry_run_changes_nothing(tmp_path):
    """A dry run reports the plan and leaves the tree alone."""
    template = make_template(tmp_path)
    target = tmp_path / "target"
    target.mkdir()

    assert apply_template.main([str(target), "--template", str(template), "--dry-run"]) == 0

    assert not (target / "AGENTS.md").exists()
    assert not (target / ".gitignore").exists()


def test_substitute_replaces_both_placeholder_forms():
    """The dashed and underscored placeholders are replaced independently."""
    text = "name: your-project-name\npackage: your_project_name\n"
    assert apply_template.substitute(text, "my-thing", "my_thing") == (
        "name: my-thing\npackage: my_thing\n"
    )


def test_derive_name_normalises_the_target_directory(tmp_path):
    """Directory names are turned into a dashed/underscored pair."""
    target = tmp_path / "My Cool_Thing"
    target.mkdir()
    assert apply_template.derive_name(target) == ("my-cool-thing", "my_cool_thing")


def test_underivable_name_exits_two(tmp_path):
    """An unusable target name is a usage error (exit 2), not a conflict."""
    target = tmp_path / "not a valid.name"
    target.mkdir()
    template = make_template(tmp_path)
    with pytest.raises(ValueError):
        apply_template.derive_name(target)
    assert apply_template.main([str(target), "--template", str(template)]) == 2
