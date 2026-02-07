"""Clean service — T051.

Build artifact cleanup with disk space accounting.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from vindicta_cli.lib.logger import get_logger

logger = get_logger("clean_service")

# Artifact patterns by type
ARTIFACT_PATTERNS = {
    "python": [
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        "*.egg-info",
        ".mypy_cache",
    ],
    "venv": [".venv", "venv"],
    "node": ["node_modules"],
    "build": ["dist", "build", ".next", "out"],
    "coverage": [".coverage", "htmlcov", "coverage"],
}


@dataclass
class CleanResult:
    """Result of cleaning a single repository."""

    name: str
    items_found: int = 0
    items_removed: int = 0
    bytes_reclaimed: int = 0
    details: list[str] = field(default_factory=list)


def clean_repo(
    repo_path: Path,
    repo_name: str,
    types: list[str] | None = None,
    dry_run: bool = False,
) -> CleanResult:
    """Clean build artifacts from a repository.

    Args:
        repo_path: Path to the repository.
        repo_name: Name for reporting.
        types: Artifact types to clean. None = all.
        dry_run: Report but don't delete.

    Returns:
        CleanResult with cleanup details.
    """
    result = CleanResult(name=repo_name)
    target_types = types or list(ARTIFACT_PATTERNS.keys())

    for artifact_type in target_types:
        patterns = ARTIFACT_PATTERNS.get(artifact_type, [])
        for pattern in patterns:
            # Search for matching dirs/files
            if "*" in pattern:
                matches = list(repo_path.glob(f"**/{pattern}"))
            else:
                matches = list(repo_path.glob(f"**/{pattern}"))

            for match in matches:
                # Skip .git internals
                if ".git" in match.parts:
                    continue

                size = _get_size(match)
                result.items_found += 1
                result.details.append(
                    f"{'[DRY] ' if dry_run else ''}Remove: "
                    f"{match.relative_to(repo_path)} ({_format_size(size)})"
                )

                if not dry_run:
                    try:
                        if match.is_dir():
                            shutil.rmtree(str(match))
                        else:
                            match.unlink()
                        result.items_removed += 1
                        result.bytes_reclaimed += size
                    except OSError as e:
                        logger.warning("Failed to remove %s: %s", match, e)
                else:
                    result.bytes_reclaimed += size

    return result


def _get_size(path: Path) -> int:
    """Get total size of a file or directory."""
    if path.is_file():
        return path.stat().st_size
    total = 0
    try:
        for f in path.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
    except OSError:
        pass
    return total


def _format_size(bytes_count: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} TB"
