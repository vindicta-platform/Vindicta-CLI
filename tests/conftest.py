"""Shared test fixtures for Vindicta CLI tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace directory structure."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def mock_workspace_config(tmp_workspace: Path) -> Path:
    """Create a minimal workspace config file for testing."""
    config_path = tmp_workspace / ".vindicta-workspace.yml"
    config_path.write_text(
        "schema_version: '1.0.0'\n"
        "parallel_count: 4\n"
        "auto_pull: false\n"
        "repositories: []\n"
    )
    return config_path


@pytest.fixture
def mock_repo(tmp_workspace: Path) -> Path:
    """Create a mock git repository in the workspace."""
    repo = tmp_workspace / "test-repo"
    repo.mkdir()
    git_dir = repo / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n")
    return repo


@pytest.fixture
def vindicta_logs_dir(tmp_path: Path) -> Path:
    """Create a temporary .vindicta/logs directory."""
    logs_dir = tmp_path / ".vindicta" / "logs"
    logs_dir.mkdir(parents=True)
    return logs_dir
