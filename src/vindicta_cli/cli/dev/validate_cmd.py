"""vindicta dev validate — T042.

Validate Platform Constitution compliance.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.validate_service import validate_repo
from vindicta_cli.lib.workspace import discover_workspace_root, scan_repos

console = Console()


def validate_cmd(
    repo: list[str] = typer.Option(["all"], "-r", "--repo", help="Repos to validate"),
    fix: bool = typer.Option(False, "--fix", help="Auto-fix issues"),
    check: list[str] = typer.Option(
        None, "--check", help="Specific checks (constitution, context, links, hooks)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Validate Platform Constitution compliance across repos."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red] Run `vindicta dev init` first.")
        raise typer.Exit(code=1)

    repos = scan_repos(workspace_root, names=repo if "all" not in repo else None)
    present = [r for r in repos if r.present and r.local_path]

    all_results = []
    for entry in present:
        result = validate_repo(
            entry.local_path,
            entry.name,
            auto_fix=fix,
            checks=check,
        )
        all_results.append(result)

    if json_output:
        output = [
            {
                "repo": r.repo_name,
                "compliance_score": round(r.compliance_score, 1),
                "passed": r.total_passed,
                "failed": r.total_failed,
                "fixed": r.total_fixed,
                "checks": [
                    {"name": c.name, "passed": c.passed, "message": c.message}
                    for c in r.checks
                ],
            }
            for r in all_results
        ]
        typer.echo(json.dumps(output, indent=2))
    else:
        for result in all_results:
            table = Table(title=f"{result.repo_name} ({result.compliance_score:.0f}%)")
            table.add_column("Check", style="cyan")
            table.add_column("Status")
            table.add_column("Message")

            for check_result in result.checks:
                status = "[green]✓[/green]" if check_result.passed else "[red]✗[/red]"
                table.add_row(check_result.name, status, check_result.message)

            console.print(table)
            console.print()

        # Summary
        total_score = sum(r.compliance_score for r in all_results)
        avg_score = total_score / len(all_results) if all_results else 0
        console.print(f"[bold]Average compliance:[/bold] {avg_score:.0f}%")

    has_failures = any(r.total_failed > 0 for r in all_results)
    if has_failures:
        raise typer.Exit(code=1)
