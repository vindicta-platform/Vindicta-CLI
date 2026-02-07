"""Unit tests for RepoEntry and RepoInfo models — T007, T008.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest


class TestRepoEntry:
    """Test RepoEntry dataclass."""

    def test_create_valid_entry(self):
        from vindicta_cli.models.repo_info import RepoEntry

        entry = RepoEntry(
            name="Vindicta-Core",
            tier="P0",
            repo_type="python",
            github_url="https://github.com/vindicta-platform/Vindicta-Core.git",
        )
        assert entry.name == "Vindicta-Core"
        assert entry.tier == "P0"
        assert entry.present is False

    def test_invalid_tier_raises(self):
        from vindicta_cli.models.repo_info import RepoEntry

        with pytest.raises(ValueError):
            RepoEntry(
                name="test",
                tier="P5",
                repo_type="python",
                github_url="https://example.com",
            )

    def test_invalid_repo_type_raises(self):
        from vindicta_cli.models.repo_info import RepoEntry

        with pytest.raises(ValueError):
            RepoEntry(
                name="test",
                tier="P0",
                repo_type="rust",
                github_url="https://example.com",
            )

    def test_valid_tiers(self):
        from vindicta_cli.models.repo_info import RepoEntry

        for tier in ["P0", "P1", "P2", "P3"]:
            entry = RepoEntry(
                name="test",
                tier=tier,
                repo_type="python",
                github_url="https://example.com",
            )
            assert entry.tier == tier

    def test_valid_repo_types(self):
        from vindicta_cli.models.repo_info import RepoEntry

        for rt in ["python", "nodejs", "mixed"]:
            entry = RepoEntry(
                name="test",
                tier="P0",
                repo_type=rt,
                github_url="https://example.com",
            )
            assert entry.repo_type == rt


class TestRepoInfo:
    """Test RepoInfo runtime state dataclass."""

    def test_defaults(self):
        from vindicta_cli.models.repo_info import RepoInfo

        info = RepoInfo(
            name="test",
            tier="P0",
            repo_type="python",
            local_path=Path("/tmp/test"),
        )
        assert info.current_branch == "main"
        assert info.is_dirty is False
        assert info.ahead == 0
        assert info.behind == 0
        assert info.ci_status is None
        assert info.open_pr_count == 0

    def test_is_on_default_branch(self):
        from vindicta_cli.models.repo_info import RepoInfo

        info = RepoInfo(
            name="test",
            tier="P0",
            repo_type="python",
            local_path=Path("/tmp/test"),
            current_branch="main",
            default_branch="main",
        )
        assert info.is_on_default is True

    def test_not_on_default_branch(self):
        from vindicta_cli.models.repo_info import RepoInfo

        info = RepoInfo(
            name="test",
            tier="P0",
            repo_type="python",
            local_path=Path("/tmp/test"),
            current_branch="feat/123",
            default_branch="main",
        )
        assert info.is_on_default is False

    def test_dirty_state_with_uncommitted(self):
        from vindicta_cli.models.repo_info import RepoInfo

        info = RepoInfo(
            name="test",
            tier="P0",
            repo_type="python",
            local_path=Path("/tmp/test"),
            is_dirty=True,
            uncommitted_files=["README.md", "src/main.py"],
        )
        assert info.is_dirty is True
        assert len(info.uncommitted_files) == 2
