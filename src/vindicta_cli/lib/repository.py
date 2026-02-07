"""Repository operations service — T028.

Handles cloning repositories and detecting repo types.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable

from vindicta_cli.lib.gh_client import GhClient
from vindicta_cli.lib.logger import get_logger
from vindicta_cli.models.repo_info import RepoEntry

logger = get_logger("repository")


async def clone_repos(
    repos: list[RepoEntry],
    workspace_root: Path,
    parallel_count: int = 4,
    on_progress: Callable[[str, str], None] | None = None,
) -> dict[str, bool]:
    """Clone multiple repos in parallel.

    Args:
        repos: Registry entries to clone.
        workspace_root: Target workspace directory.
        parallel_count: Max concurrent clones.
        on_progress: Callback(repo_name, status_message).

    Returns:
        Dict of repo_name -> success boolean.
    """
    gh = GhClient()
    semaphore = asyncio.Semaphore(parallel_count)
    results: dict[str, bool] = {}

    async def _clone_one(entry: RepoEntry) -> None:
        async with semaphore:
            target = workspace_root / entry.name
            if target.exists():
                if on_progress:
                    on_progress(entry.name, "already exists — skipping")
                results[entry.name] = True
                return

            if on_progress:
                on_progress(entry.name, "cloning...")

            try:
                org_repo = entry.github_url.replace("https://github.com/", "").rstrip(
                    ".git"
                )
                await gh.clone_repo(org_repo, target)
                entry.present = True
                entry.local_path = target
                results[entry.name] = True
                if on_progress:
                    on_progress(entry.name, "✓ cloned")
            except Exception as e:
                results[entry.name] = False
                logger.error("Failed to clone %s: %s", entry.name, e)
                if on_progress:
                    on_progress(entry.name, f"✗ failed: {e}")

    tasks = [_clone_one(entry) for entry in repos]
    await asyncio.gather(*tasks, return_exceptions=True)

    return results


def detect_repo_type(repo_path: Path) -> str:
    """Detect repository type from its contents.

    Returns:
        "python", "nodejs", or "mixed".
    """
    has_python = (repo_path / "pyproject.toml").exists() or (
        repo_path / "setup.py"
    ).exists()
    has_node = (repo_path / "package.json").exists()

    if has_python and has_node:
        return "mixed"
    if has_python:
        return "python"
    if has_node:
        return "nodejs"
    return "mixed"
