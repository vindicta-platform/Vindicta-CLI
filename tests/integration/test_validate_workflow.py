"""Integration test for validation workflow — T040.

Tests end-to-end validation across a simulated workspace.
"""

from pathlib import Path

from vindicta_cli.lib.validate_service import validate_repo


class TestValidateWorkflowIntegration:
    """Integration tests for the validation workflow."""

    def test_full_validation_on_healthy_repo(self, tmp_path: Path):
        """Repo with all required artifacts passes validation."""
        # Set up a "healthy" repo
        (tmp_path / "CONSTITUTION.md").write_text("# Constitution v1.0")
        ctx = tmp_path / ".antigravity"
        ctx.mkdir()
        (ctx / "architecture.md").write_text("# Architecture")
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []")
        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        (git_hooks / "pre-commit").write_text("#!/bin/sh")
        (tmp_path / "README.md").write_text("# Readme\n[link](https://example.com)")

        result = validate_repo(tmp_path, "HealthyRepo")
        assert result.compliance_score >= 80
        assert result.total_failed == 0

    def test_full_validation_on_bare_repo(self, tmp_path: Path):
        """Bare repo without required artifacts fails multiple checks."""
        result = validate_repo(tmp_path, "BareRepo")
        assert result.total_failed > 0
        assert result.compliance_score < 100

    def test_validation_with_broken_links(self, tmp_path: Path):
        """Repo with broken markdown links reports failures."""
        (tmp_path / "CONSTITUTION.md").write_text("# Constitution")
        ctx = tmp_path / ".antigravity"
        ctx.mkdir()
        (ctx / "arch.md").write_text("# Arch")
        (tmp_path / "README.md").write_text("[broken](missing-file.md)")
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []")
        git_hooks = tmp_path / ".git" / "hooks"
        git_hooks.mkdir(parents=True)
        (git_hooks / "pre-commit").write_text("#!/bin/sh")

        result = validate_repo(tmp_path, "BrokenLinksRepo")
        link_checks = [c for c in result.checks if c.name == "markdown_links"]
        broken = [c for c in link_checks if not c.passed]
        assert len(broken) > 0
