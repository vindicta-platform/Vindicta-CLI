"""vindicta dev setup — T032.

Run setup for workspace repositories (deps, venvs, hooks).
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.setup_service import setup_repo
from vindicta_cli.lib.workspace import discover_workspace_root, scan_repos

console = Console()


def setup_cmd(
    repo: list[str] = typer.Option(
        ["all"], "-r", "--repo", help="Specific repos to setup"
    ),
    skip_hooks: bool = typer.Option(False, "--skip-hooks", help="Skip hook install"),
    skip_venv: bool = typer.Option(False, "--skip-venv", help="Skip venv creation"),
    skip_node: bool = typer.Option(False, "--skip-node", help="Skip npm install"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Set up dependencies and tooling for repositories."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red] Run `vindicta dev init` first.")
        raise typer.Exit(code=1)

    repos = scan_repos(workspace_root, names=repo if "all" not in repo else None)
    present = [r for r in repos if r.present and r.local_path]

    all_results = {}
    for entry in present:
        results = setup_repo(
            entry.local_path,
            entry.repo_type,
            skip_venv=skip_venv,
            skip_hooks=skip_hooks,
            skip_node=skip_node,
        )
        all_results[entry.name] = results

    if json_output:
        typer.echo(json.dumps(all_results, indent=2))
    else:
        table = Table(title="Setup Results")
        table.add_column("Repository", style="cyan")
        table.add_column("Steps", style="green")
        table.add_column("Status")

        for name, results in all_results.items():
            steps = ", ".join(f"{k}={'✓' if v else '✗'}" for k, v in results.items())
            all_ok = all(results.values())
            table.add_row(name, steps, "✓" if all_ok else "[red]✗[/red]")

        console.print(table)
