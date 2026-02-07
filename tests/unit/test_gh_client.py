"""Unit tests for GitHub CLI wrapper — T012.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations


class TestGhClient:
    """Test GitHub CLI wrapper."""

    def test_check_auth_returns_bool(self):
        from vindicta_cli.lib.gh_client import GhClient

        client = GhClient()
        # Should return bool without raising
        result = client.check_auth()
        assert isinstance(result, bool)

    def test_build_clone_command(self):
        from vindicta_cli.lib.gh_client import GhClient

        client = GhClient()
        cmd = client._build_clone_command(
            "vindicta-platform/Vindicta-Core",
            "/tmp/workspace/Vindicta-Core",
        )
        assert "gh" in cmd
        assert "repo" in cmd
        assert "clone" in cmd
        assert "vindicta-platform/Vindicta-Core" in cmd

    def test_build_pr_list_command(self):
        from vindicta_cli.lib.gh_client import GhClient

        client = GhClient()
        cmd = client._build_pr_list_command("vindicta-platform/Vindicta-Core")
        assert "gh" in cmd
        assert "pr" in cmd
        assert "list" in cmd
        assert "--json" in cmd

    def test_build_ci_status_command(self):
        from vindicta_cli.lib.gh_client import GhClient

        client = GhClient()
        cmd = client._build_ci_status_command("vindicta-platform/Vindicta-Core")
        assert "gh" in cmd
        assert "run" in cmd or "status" in cmd
