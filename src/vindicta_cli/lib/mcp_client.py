"""MCP filesystem client with fallback — T020.

Wraps MCP filesystem operations with automatic fallback
to pathlib/shutil when MCP server is unavailable.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from vindicta_cli.lib.logger import get_logger

logger = get_logger("mcp_client")


class McpClient:
    """File system operations with MCP server fallback.

    Tries MCP filesystem server first, falls back to
    native pathlib/shutil operations if unavailable.
    """

    def __init__(self) -> None:
        self._available: bool | None = None

    @property
    def is_available(self) -> bool:
        """Check if MCP filesystem server is reachable."""
        if self._available is None:
            self._available = self._check_availability()
        return self._available

    def _check_availability(self) -> bool:
        """Probe for MCP filesystem server."""
        # In production, this would check for a running MCP server
        # For now, always fallback to native operations
        return False

    def read_file(self, path: Path) -> str:
        """Read file contents."""
        if self.is_available:
            return self._mcp_read(path)
        return path.read_text(encoding="utf-8")

    def write_file(self, path: Path, content: str) -> None:
        """Write content to file."""
        if self.is_available:
            self._mcp_write(path, content)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def list_directory(self, path: Path) -> list[Path]:
        """List directory entries."""
        if self.is_available:
            return self._mcp_list(path)
        return list(path.iterdir())

    def create_directory(self, path: Path) -> None:
        """Create directory and parents."""
        if self.is_available:
            self._mcp_mkdir(path)
        else:
            path.mkdir(parents=True, exist_ok=True)

    def copy_file(self, src: Path, dst: Path) -> None:
        """Copy file from src to dst."""
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))

    def remove_directory(self, path: Path) -> None:
        """Remove directory recursively."""
        if path.exists():
            shutil.rmtree(str(path))

    def _mcp_read(self, path: Path) -> str:
        """Read via MCP server (placeholder)."""
        raise NotImplementedError("MCP read not yet implemented")

    def _mcp_write(self, path: Path, content: str) -> None:
        """Write via MCP server (placeholder)."""
        raise NotImplementedError("MCP write not yet implemented")

    def _mcp_list(self, path: Path) -> list[Path]:
        """List via MCP server (placeholder)."""
        raise NotImplementedError("MCP list not yet implemented")

    def _mcp_mkdir(self, path: Path) -> None:
        """Mkdir via MCP server (placeholder)."""
        raise NotImplementedError("MCP mkdir not yet implemented")
