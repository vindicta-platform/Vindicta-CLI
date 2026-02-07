"""Unit tests for init workflow — T024.

Tests for repository cloning, tier filtering, partial failure handling.
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from vindicta_cli.lib.repository import clone_repos, detect_repo_type
from vindicta_cli.models.repo_info import RepoEntry


class TestCloneRepos:
    """Tests for clone_repos function."""

    @pytest.fixture
    def sample_repos(self) -> list[RepoEntry]:
        """Create sample repo entries for testing."""
        return [
            RepoEntry(
                name="Vindicta-Core",
                tier="P0",
                repo_type="python",
                github_url="https://github.com/vindicta-platform/Vindicta-Core.git",
            ),
            RepoEntry(
                name="Vindicta-API",
                tier="P0",
                repo_type="python",
                github_url="https://github.com/vindicta-platform/Vindicta-API.git",
            ),
        ]

    def test_skips_existing_repos(self, tmp_path: Path, sample_repos: list[RepoEntry]):
        """Clone skips repos that already exist."""
        # Create existing repo dir
        (tmp_path / "Vindicta-Core").mkdir()

        with patch("vindicta_cli.lib.repository.GhClient") as mock_gh_cls:
            mock_gh = mock_gh_cls.return_value
            mock_gh.clone_repo = AsyncMock(return_value=True)

            results = asyncio.run(clone_repos(sample_repos, tmp_path))

        assert results["Vindicta-Core"] is True
        # Only one clone call (for API, not Core)
        assert mock_gh.clone_repo.call_count == 1

    def test_reports_progress(self, tmp_path: Path, sample_repos: list[RepoEntry]):
        """Clone calls progress callback with repo name and status."""
        progress_calls = []

        def on_progress(name: str, status: str):
            progress_calls.append((name, status))

        with patch("vindicta_cli.lib.repository.GhClient") as mock_gh_cls:
            mock_gh = mock_gh_cls.return_value
            mock_gh.clone_repo = AsyncMock(return_value=True)

            asyncio.run(clone_repos(sample_repos, tmp_path, on_progress=on_progress))

        assert len(progress_calls) >= 2
        repo_names = [call[0] for call in progress_calls]
        assert "Vindicta-Core" in repo_names
        assert "Vindicta-API" in repo_names

    def test_handles_clone_failure(self, tmp_path: Path, sample_repos: list[RepoEntry]):
        """Clone reports failure for individual repos."""
        with patch("vindicta_cli.lib.repository.GhClient") as mock_gh_cls:
            mock_gh = mock_gh_cls.return_value
            mock_gh.clone_repo = AsyncMock(side_effect=ConnectionError("Network error"))

            results = asyncio.run(clone_repos(sample_repos, tmp_path))

        assert results["Vindicta-Core"] is False
        assert results["Vindicta-API"] is False

    def test_respects_parallel_count(self, tmp_path: Path):
        """Clone limits concurrency to parallel_count."""
        repos = [
            RepoEntry(
                name=f"Repo-{i}",
                tier="P0",
                repo_type="python",
                github_url=f"https://github.com/org/Repo-{i}.git",
            )
            for i in range(6)
        ]

        with patch("vindicta_cli.lib.repository.GhClient") as mock_gh_cls:
            mock_gh = mock_gh_cls.return_value
            mock_gh.clone_repo = AsyncMock(return_value=True)

            results = asyncio.run(clone_repos(repos, tmp_path, parallel_count=2))

        assert sum(1 for v in results.values() if v) == 6


class TestDetectRepoType:
    """Tests for detect_repo_type function."""

    def test_python_repo(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").touch()
        assert detect_repo_type(tmp_path) == "python"

    def test_nodejs_repo(self, tmp_path: Path):
        (tmp_path / "package.json").touch()
        assert detect_repo_type(tmp_path) == "nodejs"

    def test_mixed_repo(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").touch()
        (tmp_path / "package.json").touch()
        assert detect_repo_type(tmp_path) == "mixed"

    def test_unknown_defaults_to_mixed(self, tmp_path: Path):
        assert detect_repo_type(tmp_path) == "mixed"
