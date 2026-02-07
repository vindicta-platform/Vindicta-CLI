"""Workspace service — T023.

Discovers workspace root, manages .vindicta-workspace.yml config,
and merges registry entries with workspace state.
"""

from __future__ import annotations

import dataclasses
import subprocess
from pathlib import Path

from vindicta_cli.lib.logger import get_logger
from vindicta_cli.lib.registry import filter_by_name, filter_by_tier, get_registry
from vindicta_cli.models.repo_info import RepoEntry, RepoInfo
from vindicta_cli.models.workspace_config import WorkspaceConfig

logger = get_logger("workspace")

CONFIG_FILENAME = ".vindicta-workspace.yml"


def discover_workspace_root(start: Path | None = None) -> Path | None:
    """Walk up from start to find a directory containing config file.

    Args:
        start: Starting directory. Defaults to cwd.

    Returns:
        Path to workspace root, or None if not found.
    """
    current = (start or Path.cwd()).resolve()

    while current != current.parent:
        if (current / CONFIG_FILENAME).exists():
            return current
        current = current.parent

    # Check root
    if (current / CONFIG_FILENAME).exists():
        return current

    return None


def load_config(workspace_root: Path) -> WorkspaceConfig:
    """Load workspace configuration from file.

    Args:
        workspace_root: Path to workspace root directory.

    Returns:
        WorkspaceConfig instance.
    """
    config_path = workspace_root / CONFIG_FILENAME
    config = WorkspaceConfig.load(config_path)
    config.workspace_root = str(workspace_root)
    return config


def save_config(config: WorkspaceConfig, workspace_root: Path) -> None:
    """Save workspace configuration to file.

    Args:
        config: Configuration to save.
        workspace_root: Path to workspace root directory.
    """
    config_path = workspace_root / CONFIG_FILENAME
    config.save(config_path)


def scan_repos(
    workspace_root: Path,
    tiers: list[str] | None = None,
    names: list[str] | None = None,
) -> list[RepoEntry]:
    """Get filtered repository list with presence detection.

    Args:
        workspace_root: Path to workspace root.
        tiers: Filter by tiers. None = all.
        names: Filter by names. None = all.

    Returns:
        List of RepoEntry with `present` and `local_path` populated.
    """
    repos = get_registry()

    if tiers:
        repos = filter_by_tier(repos, tiers)
    if names:
        repos = filter_by_name(repos, names)

    # Create fresh copies and check which repos are present locally
    result = []
    for repo in repos:
        local_dir = workspace_root / repo.name
        if local_dir.exists() and (local_dir / ".git").exists():
            result.append(dataclasses.replace(repo, present=True, local_path=local_dir))
        else:
            result.append(dataclasses.replace(repo))

    return result


def get_repo_info(repo_path: Path, entry: RepoEntry) -> RepoInfo:
    """Gather git state information for a checked-out repository.

    Args:
        repo_path: Path to the repository.
        entry: Registry entry for the repo.

    Returns:
        RepoInfo with populated git fields.
    """
    info = RepoInfo(
        name=entry.name,
        tier=entry.tier,
        repo_type=entry.repo_type,
        local_path=repo_path,
    )

    try:
        # Current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            info.current_branch = result.stdout.strip()

        # Dirty check
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            changed = [line for line in result.stdout.strip().split("\n") if line]
            info.is_dirty = len(changed) > 0
            info.uncommitted_files = changed

        # Ahead/behind main
        result = subprocess.run(
            [
                "git",
                "rev-list",
                "--left-right",
                "--count",
                f"HEAD...origin/{info.default_branch}",
            ],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                info.ahead = int(parts[0])
                info.behind = int(parts[1])

    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        logger.warning("Failed to read git state for %s", entry.name)

    return info
