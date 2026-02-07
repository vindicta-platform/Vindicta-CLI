"""Repository registry — T022.

Hardcoded list of all Vindicta Platform repositories with tier
classification. Supports runtime override via workspace config.
"""

from __future__ import annotations

from vindicta_cli.models.repo_info import RepoEntry

# Organization base URL
_ORG = "https://github.com/vindicta-platform"

# Default platform repository registry
DEFAULT_REGISTRY: list[RepoEntry] = [
    # P0 — Core (Critical path, always needed)
    RepoEntry(
        name="Vindicta-Core",
        tier="P0",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Core.git",
    ),
    RepoEntry(
        name="Vindicta-API",
        tier="P0",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-API.git",
    ),
    RepoEntry(
        name="Vindicta-CLI",
        tier="P0",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-CLI.git",
    ),
    # P1 — Primary Services
    RepoEntry(
        name="Vindicta-Web",
        tier="P1",
        repo_type="nodejs",
        github_url=f"{_ORG}/Vindicta-Web.git",
    ),
    RepoEntry(
        name="Vindicta-Auth",
        tier="P1",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Auth.git",
    ),
    RepoEntry(
        name="Vindicta-DB",
        tier="P1",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-DB.git",
    ),
    RepoEntry(
        name="Vindicta-Events",
        tier="P1",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Events.git",
    ),
    # P2 — Secondary Services
    RepoEntry(
        name="Vindicta-Dice",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Dice.git",
    ),
    RepoEntry(
        name="Vindicta-Match",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Match.git",
    ),
    RepoEntry(
        name="Vindicta-Oracle",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Oracle.git",
    ),
    RepoEntry(
        name="Vindicta-Economy",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Economy.git",
    ),
    RepoEntry(
        name="Vindicta-Warscribe",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Warscribe.git",
    ),
    RepoEntry(
        name="Vindicta-Notifications",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Notifications.git",
    ),
    RepoEntry(
        name="Vindicta-Analytics",
        tier="P2",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Analytics.git",
    ),
    # P3 — Auxiliary / Tooling
    RepoEntry(
        name="Vindicta-Docs",
        tier="P3",
        repo_type="nodejs",
        github_url=f"{_ORG}/Vindicta-Docs.git",
    ),
    RepoEntry(
        name="Vindicta-Infra",
        tier="P3",
        repo_type="mixed",
        github_url=f"{_ORG}/Vindicta-Infra.git",
    ),
    RepoEntry(
        name="Vindicta-CI",
        tier="P3",
        repo_type="mixed",
        github_url=f"{_ORG}/Vindicta-CI.git",
    ),
    RepoEntry(
        name="Vindicta-SDK",
        tier="P3",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-SDK.git",
    ),
    RepoEntry(
        name="Vindicta-Mobile",
        tier="P3",
        repo_type="nodejs",
        github_url=f"{_ORG}/Vindicta-Mobile.git",
    ),
    RepoEntry(
        name="Vindicta-Admin",
        tier="P3",
        repo_type="nodejs",
        github_url=f"{_ORG}/Vindicta-Admin.git",
    ),
    RepoEntry(
        name="Vindicta-Plugins",
        tier="P3",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Plugins.git",
    ),
    RepoEntry(
        name="Vindicta-Templates",
        tier="P3",
        repo_type="mixed",
        github_url=f"{_ORG}/Vindicta-Templates.git",
    ),
    RepoEntry(
        name="Vindicta-Benchmark",
        tier="P3",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Benchmark.git",
    ),
    RepoEntry(
        name="vindicta-platform",
        tier="P3",
        repo_type="mixed",
        github_url=f"{_ORG}/vindicta-platform.git",
    ),
    RepoEntry(
        name="Vindicta-Status",
        tier="P3",
        repo_type="nodejs",
        github_url=f"{_ORG}/Vindicta-Status.git",
    ),
    RepoEntry(
        name="Vindicta-Shared",
        tier="P3",
        repo_type="python",
        github_url=f"{_ORG}/Vindicta-Shared.git",
    ),
]


def get_registry() -> list[RepoEntry]:
    """Return a copy of the default registry."""
    return list(DEFAULT_REGISTRY)


def filter_by_tier(repos: list[RepoEntry], tiers: list[str]) -> list[RepoEntry]:
    """Filter repos by tier(s).

    Args:
        repos: List of repository entries.
        tiers: List of tier names to include (e.g. ["P0", "P1"]).
               If ["all"], returns all repos.

    Returns:
        Filtered list of repos.
    """
    if "all" in tiers:
        return repos
    return [r for r in repos if r.tier in tiers]


def filter_by_name(repos: list[RepoEntry], names: list[str]) -> list[RepoEntry]:
    """Filter repos by name(s).

    Args:
        repos: List of repository entries.
        names: List of repo names to include.
               If ["all"], returns all repos.

    Returns:
        Filtered list of repos.
    """
    if "all" in names:
        return repos
    return [r for r in repos if r.name in names]
