"""Repository data models — T014, T015.

RepoEntry: Registry entry for a known platform repository.
RepoInfo: Runtime state of a repository in the workspace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

VALID_TIERS = {"P0", "P1", "P2", "P3"}
VALID_REPO_TYPES = {"python", "nodejs", "mixed"}


@dataclass
class RepoEntry:
    """Single repository in the workspace registry."""

    name: str
    tier: str
    repo_type: str
    github_url: str
    local_path: Path | None = None
    present: bool = False

    def __post_init__(self) -> None:
        """Validate tier and repo_type."""
        if self.tier not in VALID_TIERS:
            raise ValueError(
                f"Invalid tier '{self.tier}'. Must be one of: {VALID_TIERS}"
            )
        if self.repo_type not in VALID_REPO_TYPES:
            raise ValueError(
                f"Invalid repo_type '{self.repo_type}'. "
                f"Must be one of: {VALID_REPO_TYPES}"
            )


@dataclass
class RepoInfo:
    """Runtime state of a single repository."""

    # Identity
    name: str
    tier: str
    repo_type: str
    local_path: Path

    # Git State
    current_branch: str = "main"
    default_branch: str = "main"
    is_dirty: bool = False
    ahead: int = 0
    behind: int = 0
    uncommitted_files: list[str] = field(default_factory=list)

    # Remote State
    ci_status: str | None = None
    open_pr_count: int = 0
    last_commit_hash: str = ""
    last_commit_message: str = ""
    last_commit_date: str = ""

    @property
    def is_on_default(self) -> bool:
        """Check if repository is on the default branch."""
        return self.current_branch == self.default_branch
