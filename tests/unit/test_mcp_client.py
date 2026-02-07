"""Unit tests for MCP client — T011.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations

from pathlib import Path


class TestMcpClient:
    """Test MCP filesystem client with fallback."""

    def test_detects_mcp_unavailable(self):
        from vindicta_cli.lib.mcp_client import McpClient

        client = McpClient()
        # In test environment, MCP server is not running
        assert client.is_available is False

    def test_fallback_read_file(self, tmp_path: Path):
        from vindicta_cli.lib.mcp_client import McpClient

        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        client = McpClient()
        content = client.read_file(test_file)
        assert content == "hello world"

    def test_fallback_write_file(self, tmp_path: Path):
        from vindicta_cli.lib.mcp_client import McpClient

        test_file = tmp_path / "output.txt"
        client = McpClient()
        client.write_file(test_file, "test content")
        assert test_file.read_text() == "test content"

    def test_fallback_list_directory(self, tmp_path: Path):
        from vindicta_cli.lib.mcp_client import McpClient

        (tmp_path / "file1.txt").write_text("a")
        (tmp_path / "file2.txt").write_text("b")
        (tmp_path / "subdir").mkdir()

        client = McpClient()
        entries = client.list_directory(tmp_path)
        names = [e.name for e in entries]
        assert "file1.txt" in names
        assert "file2.txt" in names
        assert "subdir" in names

    def test_fallback_create_directory(self, tmp_path: Path):
        from vindicta_cli.lib.mcp_client import McpClient

        new_dir = tmp_path / "nested" / "dir"
        client = McpClient()
        client.create_directory(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()
