"""vindicta dev init — T031.

Initialize workspace by cloning platform repositories.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.registry import filter_by_name, filter_by_tier, get_registry
from vindicta_cli.lib.repository import clone_repos
from vindicta_cli.lib.setup_service import setup_repo
from vindicta_cli.lib.workspace import save_config
from vindicta_cli.models.workspace_config import WorkspaceConfig

console = Console()


def init_cmd(
    workspace: Path = typer.Option(
        Path("."), "-w", "--workspace", help="Workspace root directory"
    ),
    tier: list[str] = typer.Option(
        ["all"], "-t", "--tier", help="Tiers to clone (P0, P1, P2, P3, all)"
    ),
    repo: list[str] = typer.Option(
        ["all"], "-r", "--repo", help="Specific repos to clone"
    ),
    skip_setup: bool = typer.Option(
        False, "--skip-setup", help="Skip dependency installation"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Initialize workspace with platform repositories."""
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    setup_logging()

    # Get repos
    repos = get_registry()
    repos = filter_by_tier(repos, tier)
    repos = filter_by_name(repos, repo)

    if json_output:
        results = asyncio.run(clone_repos(repos, workspace))
        output = {
            "workspace": str(workspace),
            "repos_requested": len(repos),
            "repos_cloned": sum(1 for v in results.values() if v),
            "repos_failed": sum(1 for v in results.values() if not v),
            "results": results,
        }
        typer.echo(json.dumps(output, indent=2))
    else:
        console.print(f"[bold]Initializing workspace:[/bold] {workspace}")
        console.print(f"Repos: {len(repos)} | Tiers: {', '.join(tier)}\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Cloning repositories...", total=len(repos))

            def on_progress(name: str, status: str) -> None:
                progress.update(task, description=f"{name}: {status}")
                if "✓" in status or "skipping" in status:
                    progress.advance(task)

            results = asyncio.run(
                clone_repos(repos, workspace, on_progress=on_progress)
            )

        succeeded = sum(1 for v in results.values() if v)
        failed = sum(1 for v in results.values() if not v)
        console.print(f"\n✓ Cloned: {succeeded} | ✗ Failed: {failed}")

    # Create workspace config
    config = WorkspaceConfig(workspace_root=str(workspace))
    save_config(config, workspace)

    # Run setup if not skipped
    if not skip_setup:
        for entry in repos:
            if entry.present and entry.local_path:
                setup_repo(entry.local_path, entry.repo_type)

    if failed > 0:
        raise typer.Exit(code=1)
