"""vindicta dev doctor — T033.

Environment diagnostics and health checks.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.doctor_service import run_diagnostics
from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.workspace import discover_workspace_root

console = Console()


def doctor_cmd(
    fix: bool = typer.Option(False, "--fix", help="Attempt auto-fixes"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Run environment diagnostics and health checks."""
    setup_logging()
    workspace_root = discover_workspace_root()

    report = run_diagnostics(
        workspace_root=workspace_root,
        auto_fix=fix,
    )

    if json_output:
        output = {
            "all_ok": report.all_ok,
            "errors": report.error_count,
            "warnings": report.warning_count,
            "checks": [
                {
                    "name": c.name,
                    "status": c.status,
                    "message": c.message,
                    "fixable": c.fixable,
                    "fix_command": c.fix_command,
                }
                for c in report.checks
            ],
        }
        typer.echo(json.dumps(output, indent=2))
    else:
        table = Table(title="Environment Diagnostics")
        table.add_column("Check", style="cyan")
        table.add_column("Status")
        table.add_column("Details")
        table.add_column("Fix")

        for check in report.checks:
            if check.status == "ok":
                status = "[green]✓[/green]"
            elif check.status == "warning":
                status = "[yellow]⚠[/yellow]"
            else:
                status = "[red]✗[/red]"

            fix_hint = check.fix_command or "" if check.fixable else ""
            table.add_row(check.name, status, check.message, fix_hint)

        console.print(table)

        if report.all_ok:
            console.print("\n[bold green]All checks passed![/bold green] ✓")
        else:
            console.print(
                f"\n[bold red]{report.error_count} errors[/bold red], "
                f"[bold yellow]{report.warning_count} warnings[/bold yellow]"
            )

    if report.error_count > 0:
        raise typer.Exit(code=1)
