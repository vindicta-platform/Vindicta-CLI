"""Contract tests for CLI commands — T034.

Verifies CLI exit codes, --help output, and --json schema compliance.
"""

import json
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from vindicta_cli.main import app

runner = CliRunner()


class TestCliHelpContract:
    """Tests that all commands produce valid --help output."""

    def test_root_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "vindicta" in result.output.lower() or "Vindicta" in result.output

    def test_dev_help(self):
        result = runner.invoke(app, ["dev", "--help"])
        assert result.exit_code == 0
        assert "dev" in result.output.lower()

    def test_dev_init_help(self):
        result = runner.invoke(app, ["dev", "init", "--help"])
        assert result.exit_code == 0
        assert "--tier" in result.output
        assert "--workspace" in result.output

    def test_dev_sync_help(self):
        result = runner.invoke(app, ["dev", "sync", "--help"])
        assert result.exit_code == 0
        assert "--pull" in result.output

    def test_dev_setup_help(self):
        result = runner.invoke(app, ["dev", "setup", "--help"])
        assert result.exit_code == 0
        assert "--skip-hooks" in result.output

    def test_dev_status_help(self):
        result = runner.invoke(app, ["dev", "status", "--help"])
        assert result.exit_code == 0
        assert "--tier" in result.output

    def test_dev_validate_help(self):
        result = runner.invoke(app, ["dev", "validate", "--help"])
        assert result.exit_code == 0
        assert "--fix" in result.output

    def test_dev_doctor_help(self):
        result = runner.invoke(app, ["dev", "doctor", "--help"])
        assert result.exit_code == 0
        assert "--fix" in result.output

    def test_dev_clean_help(self):
        result = runner.invoke(app, ["dev", "clean", "--help"])
        assert result.exit_code == 0
        assert "--dry-run" in result.output

    def test_dev_config_help(self):
        result = runner.invoke(app, ["dev", "config", "--help"])
        assert result.exit_code == 0
        assert "get" in result.output
        assert "set" in result.output
        assert "list" in result.output
        assert "reset" in result.output


class TestCliExitCodes:
    """Tests that commands use correct exit codes."""

    def test_doctor_exits_0_when_healthy(self):
        """Doctor returns 0 when all checks pass."""
        with (
            patch(
                "vindicta_cli.cli.dev.doctor_cmd.discover_workspace_root",
                return_value=None,
            ),
            patch("vindicta_cli.cli.dev.doctor_cmd.run_diagnostics") as mock_diag,
        ):
            from vindicta_cli.lib.doctor_service import DiagnosticResult, DoctorReport

            mock_diag.return_value = DoctorReport(
                checks=[
                    DiagnosticResult(name="git", status="ok", message="ok"),
                ]
            )
            result = runner.invoke(app, ["dev", "doctor"])
        assert result.exit_code == 0

    def test_doctor_exits_1_on_errors(self):
        """Doctor returns 1 when errors found."""
        with (
            patch(
                "vindicta_cli.cli.dev.doctor_cmd.discover_workspace_root",
                return_value=None,
            ),
            patch("vindicta_cli.cli.dev.doctor_cmd.run_diagnostics") as mock_diag,
        ):
            from vindicta_cli.lib.doctor_service import DiagnosticResult, DoctorReport

            mock_diag.return_value = DoctorReport(
                checks=[
                    DiagnosticResult(name="git", status="error", message="missing"),
                ]
            )
            result = runner.invoke(app, ["dev", "doctor"])
        assert result.exit_code == 1


class TestCliJsonOutput:
    """Tests that --json flag produces valid JSON."""

    def test_doctor_json_output(self):
        """Doctor --json produces valid JSON with expected fields."""
        with (
            patch(
                "vindicta_cli.cli.dev.doctor_cmd.discover_workspace_root",
                return_value=None,
            ),
            patch("vindicta_cli.cli.dev.doctor_cmd.run_diagnostics") as mock_diag,
        ):
            from vindicta_cli.lib.doctor_service import DiagnosticResult, DoctorReport

            mock_diag.return_value = DoctorReport(
                checks=[
                    DiagnosticResult(name="git", status="ok", message="v2.40"),
                ]
            )
            result = runner.invoke(app, ["dev", "doctor", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "all_ok" in data
        assert "checks" in data
        assert isinstance(data["checks"], list)

    def test_config_list_json_output(self):
        """Config list --json produces valid JSON with all keys."""
        with patch(
            "vindicta_cli.cli.dev.config_cmd.discover_workspace_root",
            return_value=Path("."),
        ):
            result = runner.invoke(app, ["dev", "config", "list", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "parallel_count" in data
        assert "auto_pull" in data
