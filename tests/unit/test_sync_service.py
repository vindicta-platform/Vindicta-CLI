"""Unit tests for sync service — T035.

Tests for parallel fetch, dirty skip, auto-pull, timeout, force flag.
"""

import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch

from vindicta_cli.lib.sync_service import (
    _check_dirty,
    _get_ahead_behind,
    sync_repos,
)


class TestSyncRepos:
    """Tests for sync_repos function."""

    def test_fetches_repos(self, tmp_path: Path):
        """Sync fetches all present repos."""
        repos = [
            ("RepoA", tmp_path / "RepoA"),
            ("RepoB", tmp_path / "RepoB"),
        ]
        for _, path in repos:
            path.mkdir()

        with (
            patch("vindicta_cli.lib.sync_service._check_dirty", return_value=False),
            patch("vindicta_cli.lib.sync_service._run_git_async") as mock_git,
            patch(
                "vindicta_cli.lib.sync_service._get_ahead_behind", return_value=(0, 0)
            ),
        ):
            mock_git.return_value = True
            results = asyncio.run(sync_repos(repos))

        assert len(results) == 2
        assert all(r.success for r in results)
        assert all(r.action == "fetched" for r in results)

    def test_skips_dirty_repos(self, tmp_path: Path):
        """Dirty repos are skipped without force flag."""
        repos = [("DirtyRepo", tmp_path / "DirtyRepo")]
        (tmp_path / "DirtyRepo").mkdir()

        with patch("vindicta_cli.lib.sync_service._check_dirty", return_value=True):
            results = asyncio.run(sync_repos(repos))

        assert len(results) == 1
        assert results[0].action == "skipped"
        assert results[0].success is True

    def test_force_syncs_dirty_repos(self, tmp_path: Path):
        """Force flag syncs dirty repos."""
        repos = [("DirtyRepo", tmp_path / "DirtyRepo")]
        (tmp_path / "DirtyRepo").mkdir()

        with (
            patch("vindicta_cli.lib.sync_service._check_dirty", return_value=True),
            patch("vindicta_cli.lib.sync_service._run_git_async", return_value=True),
            patch(
                "vindicta_cli.lib.sync_service._get_ahead_behind", return_value=(0, 2)
            ),
        ):
            results = asyncio.run(sync_repos(repos, force=True))

        assert results[0].action == "fetched"

    def test_pull_when_behind(self, tmp_path: Path):
        """Pull is executed when repo is behind and pull=True."""
        repos = [("BehindRepo", tmp_path / "BehindRepo")]
        (tmp_path / "BehindRepo").mkdir()

        with (
            patch("vindicta_cli.lib.sync_service._check_dirty", return_value=False),
            patch("vindicta_cli.lib.sync_service._run_git_async", return_value=True),
            patch(
                "vindicta_cli.lib.sync_service._get_ahead_behind", return_value=(0, 3)
            ),
        ):
            results = asyncio.run(sync_repos(repos, pull=True))

        assert results[0].action == "pulled"
        assert results[0].behind == 3

    def test_handles_fetch_failure(self, tmp_path: Path):
        """Failed fetch reports failure."""
        repos = [("FailRepo", tmp_path / "FailRepo")]
        (tmp_path / "FailRepo").mkdir()

        with (
            patch("vindicta_cli.lib.sync_service._check_dirty", return_value=False),
            patch("vindicta_cli.lib.sync_service._run_git_async", return_value=False),
        ):
            results = asyncio.run(sync_repos(repos))

        assert results[0].success is False
        assert results[0].action == "failed"


class TestCheckDirty:
    """Tests for _check_dirty helper."""

    def test_clean_repo(self, tmp_path: Path):
        with patch("vindicta_cli.lib.sync_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            assert _check_dirty(tmp_path) is False

    def test_dirty_repo(self, tmp_path: Path):
        with patch("vindicta_cli.lib.sync_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=" M file.py\n?? new.txt", returncode=0
            )
            assert _check_dirty(tmp_path) is True


class TestGetAheadBehind:
    """Tests for _get_ahead_behind helper."""

    def test_parses_output(self, tmp_path: Path):
        with patch("vindicta_cli.lib.sync_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="3\t5", returncode=0)
            ahead, behind = _get_ahead_behind(tmp_path)

        assert ahead == 3
        assert behind == 5

    def test_handles_error(self, tmp_path: Path):
        with patch("vindicta_cli.lib.sync_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=1)
            ahead, behind = _get_ahead_behind(tmp_path)

        assert ahead == 0
        assert behind == 0
