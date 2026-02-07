"""Unit tests for workspace service — T049.

Tests for workspace root discovery, config management,
repo scanning, and incremental workspace setup.
"""

from pathlib import Path

from vindicta_cli.lib.workspace import (
    CONFIG_FILENAME,
    discover_workspace_root,
    load_config,
    save_config,
    scan_repos,
)
from vindicta_cli.models.workspace_config import WorkspaceConfig


class TestDiscoverWorkspaceRoot:
    """Tests for discover_workspace_root."""

    def test_finds_config_in_current_dir(self, tmp_path: Path):
        (tmp_path / CONFIG_FILENAME).write_text("schema_version: '1.0.0'")
        result = discover_workspace_root(tmp_path)
        assert result == tmp_path

    def test_finds_config_in_parent(self, tmp_path: Path):
        (tmp_path / CONFIG_FILENAME).write_text("schema_version: '1.0.0'")
        child = tmp_path / "sub" / "dir"
        child.mkdir(parents=True)
        result = discover_workspace_root(child)
        assert result == tmp_path

    def test_returns_none_when_not_found(self, tmp_path: Path):
        result = discover_workspace_root(tmp_path)
        assert result is None


class TestLoadSaveConfig:
    """Tests for load_config and save_config."""

    def test_save_and_load_roundtrip(self, tmp_path: Path):
        config = WorkspaceConfig(parallel_count=8, auto_pull=True)
        save_config(config, tmp_path)

        loaded = load_config(tmp_path)
        assert loaded.parallel_count == 8
        assert loaded.auto_pull is True

    def test_load_missing_returns_defaults(self, tmp_path: Path):
        config = load_config(tmp_path)
        assert isinstance(config, WorkspaceConfig)
        assert config.parallel_count == 4

    def test_config_file_created(self, tmp_path: Path):
        config = WorkspaceConfig()
        save_config(config, tmp_path)
        assert (tmp_path / CONFIG_FILENAME).exists()


class TestScanRepos:
    """Tests for scan_repos function."""

    def test_detects_present_repos(self, tmp_path: Path):
        # Create a repo-like directory
        repo_dir = tmp_path / "Vindicta-Core"
        repo_dir.mkdir()
        (repo_dir / ".git").mkdir()

        repos = scan_repos(tmp_path)
        core_repos = [r for r in repos if r.name == "Vindicta-Core"]
        assert len(core_repos) == 1
        assert core_repos[0].present is True
        assert core_repos[0].local_path == repo_dir

    def test_detects_absent_repos(self, tmp_path: Path):
        repos = scan_repos(tmp_path)
        assert all(not r.present for r in repos)

    def test_tier_filter(self, tmp_path: Path):
        repos = scan_repos(tmp_path, tiers=["P0"])
        assert all(r.tier == "P0" for r in repos)
        assert len(repos) == 3  # Core, API, CLI

    def test_name_filter(self, tmp_path: Path):
        repos = scan_repos(tmp_path, names=["Vindicta-Core"])
        assert len(repos) == 1
        assert repos[0].name == "Vindicta-Core"

    def test_non_git_dir_not_detected(self, tmp_path: Path):
        """Directory without .git is not detected as present."""
        (tmp_path / "Vindicta-Core").mkdir()
        repos = scan_repos(tmp_path)
        core = [r for r in repos if r.name == "Vindicta-Core"]
        assert len(core) == 1
        assert core[0].present is False
