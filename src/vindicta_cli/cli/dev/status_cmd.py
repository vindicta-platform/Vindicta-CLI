"""vindicta dev status — T045.

Display workspace health dashboard.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.workspace import (
    discover_workspace_root,
    get_repo_info,
    scan_repos,
)

console = Console()


def status_cmd(
    tier: list[str] = typer.Option(["all"], "-t", "--tier", help="Filter by tier"),
    failing: bool = typer.Option(
        False, "--failing", help="Show only repos with issues"
    ),
    ci: bool = typer.Option(False, "--ci", help="Include CI status (slower)"),
    detailed: bool = typer.Option(False, "--detailed", help="Show full details"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Show workspace repository status dashboard."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red] Run `vindicta dev init` first.")
        raise typer.Exit(code=1)

    repos = scan_repos(workspace_root, tiers=tier)
    present = [r for r in repos if r.present and r.local_path]

    # Gather repo info
    infos = [get_repo_info(r.local_path, r) for r in present]

    # Filter failing
    if failing:
        infos = [i for i in infos if i.is_dirty or not i.is_on_default]

    if json_output:
        output = [
            {
                "name": i.name,
                "tier": i.tier,
                "branch": i.current_branch,
                "dirty": i.is_dirty,
                "ahead": i.ahead,
                "behind": i.behind,
                "on_default": i.is_on_default,
            }
            for i in infos
        ]
        typer.echo(json.dumps(output, indent=2))
    else:
        # Group by tier
        tiers_found: dict[str, list] = {}
        for info in infos:
            tiers_found.setdefault(info.tier, []).append(info)

        for tier_name in sorted(tiers_found.keys()):
            tier_infos = tiers_found[tier_name]
            table = Table(title=f"Tier {tier_name}")
            table.add_column("Repository", style="cyan")
            table.add_column("Branch", style="green")
            table.add_column("Status")
            table.add_column("Ahead", justify="right")
            table.add_column("Behind", justify="right")

            for info in tier_infos:
                status_parts = []
                if info.is_dirty:
                    status_parts.append("[red]dirty[/red]")
                if not info.is_on_default:
                    status_parts.append("[yellow]off-default[/yellow]")
                if not status_parts:
                    status_parts.append("[green]clean[/green]")

                table.add_row(
                    info.name,
                    info.current_branch,
                    " ".join(status_parts),
                    str(info.ahead),
                    str(info.behind),
                )

            console.print(table)
            console.print()

        # Summary
        total = len(infos)
        dirty = sum(1 for i in infos if i.is_dirty)
        off_default = sum(1 for i in infos if not i.is_on_default)
        console.print(
            Panel(
                f"[bold]Total:[/bold] {total} repos | "
                f"[bold green]Clean:[/bold green] {total - dirty} | "
                f"[bold red]Dirty:[/bold red] {dirty} | "
                f"[bold yellow]Off-default:[/bold yellow] {off_default}",
                title="Summary",
            )
        )
