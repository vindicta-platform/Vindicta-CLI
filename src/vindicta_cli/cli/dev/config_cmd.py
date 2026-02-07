"""vindicta dev config — T055.

Workspace configuration management subcommands.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from vindicta_cli.lib.config_service import (
    get_config_value,
    list_config,
    reset_config,
    set_config_value,
)
from vindicta_cli.lib.logger import setup_logging
from vindicta_cli.lib.workspace import discover_workspace_root

console = Console()
config_app = typer.Typer(help="Manage workspace configuration.")


@config_app.command("get")
def config_get(
    key: str = typer.Argument(help="Configuration key"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Get a configuration value."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red]")
        raise typer.Exit(code=1)

    try:
        value = get_config_value(workspace_root, key)
        if json_output:
            typer.echo(json.dumps({"key": key, "value": value}))
        else:
            console.print(f"[cyan]{key}[/cyan] = {value}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


@config_app.command("set")
def config_set(
    key: str = typer.Argument(help="Configuration key"),
    value: str = typer.Argument(help="New value"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Set a configuration value."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red]")
        raise typer.Exit(code=1)

    try:
        coerced = set_config_value(workspace_root, key, value)
        if json_output:
            typer.echo(json.dumps({"key": key, "value": coerced}))
        else:
            console.print(f"[green]✓[/green] {key} = {coerced}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


@config_app.command("list")
def config_list(
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """List all configuration values."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red]")
        raise typer.Exit(code=1)

    config_data = list_config(workspace_root)

    if json_output:
        typer.echo(json.dumps(config_data, indent=2))
    else:
        table = Table(title="Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Type")
        table.add_column("Description")

        for key, info in config_data.items():
            table.add_row(key, str(info["value"]), info["type"], info["description"])

        console.print(table)


@config_app.command("reset")
def config_reset(
    key: str = typer.Argument(None, help="Specific key to reset (or all)"),
    json_output: bool = typer.Option(False, "--json", help="JSON output"),
) -> None:
    """Reset configuration to defaults."""
    setup_logging()
    workspace_root = discover_workspace_root()
    if not workspace_root:
        console.print("[red]No workspace found.[/red]")
        raise typer.Exit(code=1)

    try:
        reset_config(workspace_root, key)
        target = key or "all settings"
        if json_output:
            typer.echo(json.dumps({"reset": target}))
        else:
            console.print(f"[green]✓[/green] Reset {target} to defaults")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
