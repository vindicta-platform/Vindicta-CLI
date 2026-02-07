"""vindicta dev clean — T052.

Clean build artifacts and report disk space reclaimed.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.clean_service import _format_size, clean_repo
from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.workspace import discover_workspace_root, scan_repos

console = Console()


def clean_cmd(
    dry_run: bool = typer.Option(False, "--dry-run", help="Report but don't delete"),
    type_filter: list[str] = typer.Option(
        None, "--type", help="Artifact types: python, venv, node, build, coverage"
    ),
    repo: list[str] = typer.Option(["all"], "-r", "--repo", help="Repos to clean"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Clean build artifacts across workspace repositories."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red] Run `vindicta dev init` first.")
        raise typer.Exit(code=1)

    repos = scan_repos(workspace_root, names=repo if "all" not in repo else None)
    present = [r for r in repos if r.present and r.local_path]

    all_results = []
    total_reclaimed = 0

    for entry in present:
        result = clean_repo(
            entry.local_path,
            entry.name,
            types=type_filter,
            dry_run=dry_run,
        )
        all_results.append(result)
        total_reclaimed += result.bytes_reclaimed

    if json_output:
        output = {
            "dry_run": dry_run,
            "total_reclaimed": total_reclaimed,
            "total_reclaimed_human": _format_size(total_reclaimed),
            "repos": [
                {
                    "name": r.name,
                    "items_found": r.items_found,
                    "items_removed": r.items_removed,
                    "bytes_reclaimed": r.bytes_reclaimed,
                }
                for r in all_results
            ],
        }
        typer.echo(json.dumps(output, indent=2))
    else:
        prefix = "[DRY RUN] " if dry_run else ""
        table = Table(title=f"{prefix}Cleanup Results")
        table.add_column("Repository", style="cyan")
        table.add_column("Items Found", justify="right")
        table.add_column("Removed", justify="right")
        table.add_column("Space", justify="right")

        for r in all_results:
            if r.items_found > 0:
                table.add_row(
                    r.name,
                    str(r.items_found),
                    str(r.items_removed),
                    _format_size(r.bytes_reclaimed),
                )

        console.print(table)
        console.print(
            f"\n[bold]Total reclaimed:[/bold] {_format_size(total_reclaimed)}"
        )
