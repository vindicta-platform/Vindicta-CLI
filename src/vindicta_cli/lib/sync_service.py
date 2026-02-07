"""Sync service — T037.

Parallel repository synchronization with configurable fetch/pull.
"""

from __future__ import annotations

import asyncio
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from vindicta_cli.lib.logger import get_logger

logger = get_logger("sync_service")


@dataclass
class SyncResult:
    """Result of syncing a single repository."""

    name: str
    success: bool
    action: str  # "fetched", "pulled", "skipped", "failed"
    ahead: int = 0
    behind: int = 0
    message: str = ""


async def sync_repos(
    repos: list[tuple[str, Path]],
    pull: bool = False,
    force: bool = False,
    parallel_count: int = 4,
    timeout: int = 120,
    on_progress: Callable[[str, str], None] | None = None,
) -> list[SyncResult]:
    """Synchronize multiple repositories in parallel.

    Args:
        repos: List of (name, path) tuples.
        pull: Also pull changes (not just fetch).
        force: Force sync even on dirty repos.
        parallel_count: Max concurrent operations.
        timeout: Per-repo timeout in seconds.
        on_progress: Callback(repo_name, status).

    Returns:
        List of SyncResult for each repo.
    """
    semaphore = asyncio.Semaphore(parallel_count)
    results: list[SyncResult] = []

    async def _sync_one(name: str, path: Path) -> SyncResult:
        async with semaphore:
            if on_progress:
                on_progress(name, "syncing...")

            # Check if dirty
            if not force:
                is_dirty = _check_dirty(path)
                if is_dirty:
                    if on_progress:
                        on_progress(name, "skipped (dirty)")
                    return SyncResult(
                        name=name,
                        success=True,
                        action="skipped",
                        message="Working tree has uncommitted changes",
                    )

            # Fetch
            try:
                fetch_ok = await _run_git_async(
                    ["git", "fetch", "--prune"], path, timeout
                )
                if not fetch_ok:
                    return SyncResult(
                        name=name,
                        success=False,
                        action="failed",
                        message="Fetch failed",
                    )
            except asyncio.TimeoutError:
                return SyncResult(
                    name=name,
                    success=False,
                    action="failed",
                    message=f"Fetch timed out after {timeout}s",
                )

            # Get ahead/behind
            ahead, behind = _get_ahead_behind(path)

            # Pull if requested
            action = "fetched"
            if pull and behind > 0:
                try:
                    pull_ok = await _run_git_async(
                        ["git", "pull", "--ff-only"], path, timeout
                    )
                    action = "pulled" if pull_ok else "failed"
                except asyncio.TimeoutError:
                    action = "failed"

            if on_progress:
                on_progress(name, f"✓ {action}")

            return SyncResult(
                name=name,
                success=True,
                action=action,
                ahead=ahead,
                behind=behind,
            )

    tasks = [_sync_one(name, path) for name, path in repos]
    results = await asyncio.gather(*tasks)
    return list(results)


def _check_dirty(path: Path) -> bool:
    """Check if repo has uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=5,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def _get_ahead_behind(path: Path) -> tuple[int, int]:
    """Get ahead/behind counts relative to tracking branch."""
    try:
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                return int(parts[0]), int(parts[1])
    except Exception:
        pass
    return 0, 0


async def _run_git_async(cmd: list[str], cwd: Path, timeout: int) -> bool:
    """Run a git command asynchronously."""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(cwd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        await asyncio.wait_for(process.communicate(), timeout=timeout)
        return process.returncode == 0
    except asyncio.TimeoutError:
        process.kill()
        raise
