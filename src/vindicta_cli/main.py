"""Vindicta CLI - Root application entry point.

Registers all domain sub-applications (dev, dice, match, etc.)
following the `vindicta [domain] [action]` naming convention.
"""

from __future__ import annotations

import typer

from vindicta_cli.cli.dev.clean_cmd import clean_cmd
from vindicta_cli.cli.dev.config_cmd import config_app
from vindicta_cli.cli.dev.doctor_cmd import doctor_cmd
from vindicta_cli.cli.dev.init_cmd import init_cmd
from vindicta_cli.cli.dev.setup_cmd import setup_cmd
from vindicta_cli.cli.dev.status_cmd import status_cmd
from vindicta_cli.cli.dev.sync_cmd import sync_cmd
from vindicta_cli.cli.dev.validate_cmd import validate_cmd

# Root application
app = typer.Typer(
    name="vindicta",
    help="Unified command-line interface for the Vindicta Platform.",
    no_args_is_help=True,
)

# Dev sub-application
dev_app = typer.Typer(
    name="dev",
    help="Developer commands for platform workspace management.",
    no_args_is_help=True,
)

# Register dev commands
dev_app.command("init")(init_cmd)
dev_app.command("sync")(sync_cmd)
dev_app.command("setup")(setup_cmd)
dev_app.command("status")(status_cmd)
dev_app.command("validate")(validate_cmd)
dev_app.command("doctor")(doctor_cmd)
dev_app.command("clean")(clean_cmd)
dev_app.add_typer(config_app, name="config")

# Register dev sub-app on root
app.add_typer(dev_app, name="dev")


if __name__ == "__main__":
    app()
