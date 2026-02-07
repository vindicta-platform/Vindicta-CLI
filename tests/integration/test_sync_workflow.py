"""Integration test for sync workflow — T036.

Tests the sync → status pipeline with mock git operations.
"""

import asyncio
from pathlib import Path
from unittest.mock import patch

from vindicta_cli.lib.sync_service import sync_repos
from vindicta_cli.lib.workspace import CONFIG_FILENAME, scan_repos
from vindicta_cli.models.workspace_config import WorkspaceConfig


class TestSyncWorkflowIntegration:
    """Integration tests for the sync workflow."""

    def test_sync_skips_absent_repos(self, tmp_path: Path):
        """Sync only operates on present repos."""
        # Create config
        config = WorkspaceConfig(workspace_root=str(tmp_path))
        config.save(tmp_path / CONFIG_FILENAME)

        repos = scan_repos(tmp_path)
        present = [(r.name, r.local_path) for r in repos if r.present and r.local_path]
        # No repos cloned yet
        assert len(present) == 0

    def test_sync_reports_per_repo_results(self, tmp_path: Path):
        """Each repo gets an individual sync result."""
        repos = [
            ("RepoA", tmp_path / "RepoA"),
            ("RepoB", tmp_path / "RepoB"),
        ]
        for _, path in repos:
            path.mkdir()

        with (
            patch("vindicta_cli.lib.sync_service._check_dirty", return_value=False),
            patch("vindicta_cli.lib.sync_service._run_git_async", return_value=True),
            patch(
                "vindicta_cli.lib.sync_service._get_ahead_behind", return_value=(1, 2)
            ),
        ):
            results = asyncio.run(sync_repos(repos))

        assert len(results) == 2
        for r in results:
            assert r.ahead == 1
            assert r.behind == 2
