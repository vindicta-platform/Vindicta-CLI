"""Health status models — T017."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RepoHealthSummary:
    """Health summary for a single repository."""

    name: str
    tier: str
    git_healthy: bool
    ci_healthy: bool | None = None
    pr_count: int = 0
    issues: list[str] = field(default_factory=list)


@dataclass
class HealthStatus:
    """Workspace-wide health snapshot."""

    timestamp: str
    workspace_root: str
    total_repos: int
    healthy_count: int
    issue_count: int
    repos: list[RepoHealthSummary] = field(default_factory=list)
    tier_summary: dict[str, dict] = field(default_factory=dict)
