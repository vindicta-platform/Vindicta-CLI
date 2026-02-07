"""Unit tests for validate service — T039.

Tests for constitution check, context artifacts, link validation,
hooks, auto-fix, and compliance score.
"""

from pathlib import Path

from vindicta_cli.lib.validate_service import (
    _check_constitution,
    _check_context_artifacts,
    _check_markdown_links,
    _check_pre_commit_hooks,
    _find_broken_links,
    validate_repo,
)
from vindicta_cli.models.validation_result import ValidationResult


class TestCheckConstitution:
    """Tests for _check_constitution helper."""

    def test_finds_constitution_in_specify_dir(self, tmp_path: Path):
        const_path = tmp_path / ".specify" / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True)
        const_path.write_text("# Constitution")
        result = _check_constitution(tmp_path)
        assert result.passed is True

    def test_finds_constitution_at_root(self, tmp_path: Path):
        (tmp_path / "CONSTITUTION.md").write_text("# Constitution")
        result = _check_constitution(tmp_path)
        assert result.passed is True

    def test_missing_constitution(self, tmp_path: Path):
        result = _check_constitution(tmp_path)
        assert result.passed is False
        assert result.auto_fixable is True


class TestCheckContextArtifacts:
    """Tests for _check_context_artifacts helper."""

    def test_finds_artifacts(self, tmp_path: Path):
        ctx = tmp_path / ".antigravity"
        ctx.mkdir()
        (ctx / "architecture.md").write_text("# Arch")
        result = _check_context_artifacts(tmp_path)
        assert result.passed is True

    def test_missing_artifacts(self, tmp_path: Path):
        result = _check_context_artifacts(tmp_path)
        assert result.passed is False


class TestCheckMarkdownLinks:
    """Tests for _check_markdown_links helper."""

    def test_valid_links(self, tmp_path: Path):
        readme = tmp_path / "README.md"
        readme.write_text("[link](https://example.com)")
        results = _check_markdown_links(tmp_path)
        assert all(c.passed for c in results)

    def test_broken_relative_links(self, tmp_path: Path):
        readme = tmp_path / "README.md"
        readme.write_text("[missing](nonexistent-file.md)")
        results = _check_markdown_links(tmp_path)
        broken = [c for c in results if not c.passed]
        assert len(broken) > 0

    def test_skips_urls(self, tmp_path: Path):
        """External URLs are not validated."""
        content = "[google](https://google.com)\n[anchor](#heading)"
        broken = _find_broken_links(content, tmp_path)
        assert len(broken) == 0


class TestCheckPreCommitHooks:
    """Tests for _check_pre_commit_hooks helper."""

    def test_no_config(self, tmp_path: Path):
        result = _check_pre_commit_hooks(tmp_path)
        assert result.passed is False

    def test_config_exists_hooks_installed(self, tmp_path: Path):
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []")
        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        (git_hooks / "pre-commit").write_text("#!/bin/sh")
        result = _check_pre_commit_hooks(tmp_path)
        assert result.passed is True

    def test_config_exists_hooks_not_installed(self, tmp_path: Path):
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []")
        (tmp_path / ".git").mkdir()
        result = _check_pre_commit_hooks(tmp_path)
        assert result.passed is False
        assert result.auto_fixable is True


class TestValidateRepo:
    """Tests for validate_repo orchestrator."""

    def test_returns_validation_result(self, tmp_path: Path):
        result = validate_repo(tmp_path, "TestRepo")
        assert isinstance(result, ValidationResult)
        assert result.repo_name == "TestRepo"

    def test_compliance_score(self, tmp_path: Path):
        """Compliance score reflects pass/fail ratio."""
        result = validate_repo(tmp_path, "TestRepo")
        assert 0 <= result.compliance_score <= 100

    def test_filter_checks(self, tmp_path: Path):
        """Only runs specified checks."""
        result = validate_repo(tmp_path, "TestRepo", checks=["constitution"])
        check_names = [c.name for c in result.checks]
        assert "constitution_presence" in check_names
        assert "pre_commit_config" not in check_names
