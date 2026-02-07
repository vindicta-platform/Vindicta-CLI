"""vindicta dev sync — T038.

Synchronize workspace repositories with remote.
"""

from __future__ import annotations

import asyncio
import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.sync_service import sync_repos
from vindicta_cli.lib.workspace import discover_workspace_root, scan_repos

console = Console()


def sync_cmd(
    pull: bool = typer.Option(False, "--pull", help="Also pull changes"),
    parallel: int = typer.Option(4, "--parallel", "-p", help="Concurrent ops"),
    tier: list[str] = typer.Option(["all"], "-t", "--tier", help="Filter by tier"),
    force: bool = typer.Option(False, "--force", help="Sync dirty repos too"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Synchronize all repositories with remote."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red] Run `vindicta dev init` first.")
        raise typer.Exit(code=1)

    repos = scan_repos(workspace_root, tiers=tier)
    present_repos = [
        (r.name, r.local_path) for r in repos if r.present and r.local_path
    ]

    if not present_repos:
        console.print("[yellow]No repos found in workspace.[/yellow]")
        raise typer.Exit(code=0)

    results = asyncio.run(
        sync_repos(
            repos=present_repos,
            pull=pull,
            force=force,
            parallel_count=parallel,
        )
    )

    if json_output:
        output = [
            {
                "name": r.name,
                "action": r.action,
                "success": r.success,
                "ahead": r.ahead,
                "behind": r.behind,
                "message": r.message,
            }
            for r in results
        ]
        typer.echo(json.dumps(output, indent=2))
    else:
        table = Table(title="Sync Results")
        table.add_column("Repository", style="cyan")
        table.add_column("Action", style="green")
        table.add_column("Ahead", justify="right")
        table.add_column("Behind", justify="right")
        table.add_column("Status")

        for r in results:
            status = "✓" if r.success else "[red]✗[/red]"
            table.add_row(r.name, r.action, str(r.ahead), str(r.behind), status)

        console.print(table)

    failed = sum(1 for r in results if not r.success)
    if failed:
        raise typer.Exit(code=1)
