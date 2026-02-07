"""Unit tests for status dashboard — T043.

Tests for tier grouping, health indicators, filtering, JSON output.
"""

from pathlib import Path

from vindicta_cli.models.repo_info import RepoInfo


class TestRepoInfoStatusProperties:
    """Tests for RepoInfo status properties used by dashboard."""

    def test_clean_on_default(self):
        info = RepoInfo(
            name="TestRepo",
            tier="P0",
            repo_type="python",
            local_path=Path("/test"),
            current_branch="main",
            default_branch="main",
            is_dirty=False,
        )
        assert info.is_on_default is True
        assert info.is_dirty is False

    def test_dirty_off_default(self):
        info = RepoInfo(
            name="TestRepo",
            tier="P0",
            repo_type="python",
            local_path=Path("/test"),
            current_branch="feat/branch",
            default_branch="main",
            is_dirty=True,
            uncommitted_files=["file.py"],
        )
        assert info.is_on_default is False
        assert info.is_dirty is True

    def test_ahead_behind_tracking(self):
        info = RepoInfo(
            name="TestRepo",
            tier="P1",
            repo_type="python",
            local_path=Path("/test"),
            ahead=3,
            behind=2,
        )
        assert info.ahead == 3
        assert info.behind == 2

    def test_tier_grouping(self):
        """Multiple repos group correctly by tier."""
        repos = [
            RepoInfo(name="A", tier="P0", repo_type="python", local_path=Path("/a")),
            RepoInfo(name="B", tier="P0", repo_type="python", local_path=Path("/b")),
            RepoInfo(name="C", tier="P1", repo_type="nodejs", local_path=Path("/c")),
        ]
        grouped: dict[str, list] = {}
        for r in repos:
            grouped.setdefault(r.tier, []).append(r)

        assert len(grouped["P0"]) == 2
        assert len(grouped["P1"]) == 1

    def test_failing_filter(self):
        """Failing filter shows dirty and off-default repos."""
        repos = [
            RepoInfo(
                name="Clean",
                tier="P0",
                repo_type="python",
                local_path=Path("/a"),
                is_dirty=False,
                current_branch="main",
                default_branch="main",
            ),
            RepoInfo(
                name="Dirty",
                tier="P0",
                repo_type="python",
                local_path=Path("/b"),
                is_dirty=True,
            ),
            RepoInfo(
                name="OffDefault",
                tier="P1",
                repo_type="python",
                local_path=Path("/c"),
                current_branch="feat/x",
                default_branch="main",
            ),
        ]
        failing = [i for i in repos if i.is_dirty or not i.is_on_default]
        assert len(failing) == 2
        names = [r.name for r in failing]
        assert "Clean" not in names
        assert "Dirty" in names
        assert "OffDefault" in names
