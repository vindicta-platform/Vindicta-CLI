"""GitHub CLI wrapper — T021.

Wraps `gh` CLI for authentication, repo cloning, PR listing,
and CI status queries. Uses asyncio.subprocess for non-blocking
execution.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

from vindicta_cli.lib.logger import get_logger
from vindicta_cli.lib.retry import with_retry

logger = get_logger("gh_client")


class GhClient:
    """Wrapper around the GitHub CLI (gh)."""

    def check_auth(self) -> bool:
        """Check if gh CLI is authenticated.

        Returns:
            True if authenticated, False otherwise.
        """
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _build_clone_command(self, repo: str, target_dir: str) -> list[str]:
        """Build gh repo clone command.

        Args:
            repo: Repo in owner/name format.
            target_dir: Local directory to clone into.
        """
        return ["gh", "repo", "clone", repo, target_dir]

    def _build_pr_list_command(self, repo: str) -> list[str]:
        """Build gh PR list command.

        Args:
            repo: Repo in owner/name format.
        """
        return [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--json",
            "number,title,state,author",
            "--limit",
            "50",
        ]

    def _build_ci_status_command(self, repo: str) -> list[str]:
        """Build gh CI run status command.

        Args:
            repo: Repo in owner/name format.
        """
        return [
            "gh",
            "run",
            "list",
            "--repo",
            repo,
            "--json",
            "status,conclusion,name",
            "--limit",
            "5",
        ]

    @with_retry
    async def clone_repo(self, repo: str, target_dir: Path) -> bool:
        """Clone a repository using gh CLI.

        Args:
            repo: Repo in owner/name format.
            target_dir: Local directory to clone into.

        Returns:
            True if clone succeeded.
        """
        cmd = self._build_clone_command(repo, str(target_dir))
        logger.info("Cloning %s → %s", repo, target_dir)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error = stderr.decode().strip()
            logger.error("Clone failed for %s: %s", repo, error)
            raise ConnectionError(f"Failed to clone {repo}: {error}")

        return True

    @with_retry
    async def get_pr_count(self, repo: str) -> int:
        """Get open PR count for a repository.

        Args:
            repo: Repo in owner/name format.

        Returns:
            Number of open PRs.
        """
        cmd = self._build_pr_list_command(repo)
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            return 0

        try:
            prs = json.loads(stdout.decode())
            return len(prs)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return 0

    @with_retry
    async def get_ci_status(self, repo: str) -> str | None:
        """Get latest CI run status for a repository.

        Args:
            repo: Repo in owner/name format.

        Returns:
            Status string ("passing", "failing", "pending") or None.
        """
        cmd = self._build_ci_status_command(repo)
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            return None

        try:
            runs = json.loads(stdout.decode())
            if not runs:
                return None
            latest = runs[0]
            if latest.get("status") == "completed":
                return "passing" if latest.get("conclusion") == "success" else "failing"
            return "pending"
        except (json.JSONDecodeError, UnicodeDecodeError, IndexError):
            return None
