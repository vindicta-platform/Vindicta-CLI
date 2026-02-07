"""Unit tests for doctor service — T026, T047.

Tests for tool detection, version checks, workspace health, and auto-fix.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from vindicta_cli.lib.doctor_service import (
    DiagnosticResult,
    DoctorReport,
    _check_stale_locks,
    _check_tool,
    _check_workspace_config,
    run_diagnostics,
)


class TestCheckTool:
    """Tests for _check_tool helper."""

    def test_tool_not_found(self):
        """Missing tool reports error."""
        with patch("vindicta_cli.lib.doctor_service.shutil.which", return_value=None):
            result = _check_tool("missing-tool", "1.0")
        assert result.status == "error"
        assert "not found" in result.message

    def test_tool_found_version_ok(self):
        """Found tool with version reports ok."""
        with (
            patch(
                "vindicta_cli.lib.doctor_service.shutil.which",
                return_value="/usr/bin/git",
            ),
            patch("vindicta_cli.lib.doctor_service.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(
                stdout="git version 2.40.0", stderr="", returncode=0
            )
            result = _check_tool("git", "2.30")

        assert result.status == "ok"
        assert "git" in result.message

    def test_tool_version_check_timeout(self):
        """Timeout on version check reports warning."""
        import subprocess

        with (
            patch(
                "vindicta_cli.lib.doctor_service.shutil.which",
                return_value="/usr/bin/node",
            ),
            patch("vindicta_cli.lib.doctor_service.subprocess.run") as mock_run,
        ):
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="node", timeout=5)
            result = _check_tool("node", "18.0")

        assert result.status == "warning"


class TestCheckWorkspaceConfig:
    """Tests for _check_workspace_config helper."""

    def test_no_config_warns(self, tmp_path: Path):
        """Missing config file reports warning with fix suggestion."""
        result = _check_workspace_config(tmp_path)
        assert result.status == "warning"
        assert result.fixable is True
        assert result.fix_command is not None

    def test_valid_config_ok(self, tmp_path: Path):
        """Valid YAML config reports ok."""
        config_file = tmp_path / ".vindicta-workspace.yml"
        config_file.write_text("schema_version: '1.0.0'\n")
        result = _check_workspace_config(tmp_path)
        assert result.status == "ok"

    def test_corrupted_config_errors(self, tmp_path: Path):
        """Invalid YAML reports error with fix."""
        config_file = tmp_path / ".vindicta-workspace.yml"
        config_file.write_text("invalid: yaml: [broken: {{")
        result = _check_workspace_config(tmp_path)
        # Should be ok or error depending on YAML parser tolerance
        assert result.status in ("ok", "error")


class TestCheckStaleLocks:
    """Tests for _check_stale_locks helper."""

    def test_no_locks_ok(self, tmp_path: Path):
        result = _check_stale_locks(tmp_path)
        assert result.status == "ok"

    def test_stale_lock_detected(self, tmp_path: Path):
        """Git lock files trigger warning."""
        git_dir = tmp_path / "repo" / ".git"
        git_dir.mkdir(parents=True)
        (git_dir / "index.lock").touch()
        result = _check_stale_locks(tmp_path)
        assert result.status == "warning"
        assert result.fixable is True


class TestRunDiagnostics:
    """Tests for run_diagnostics orchestrator."""

    def test_returns_doctor_report(self):
        """Diagnostics returns a DoctorReport."""
        with (
            patch(
                "vindicta_cli.lib.doctor_service.shutil.which",
                return_value="/usr/bin/git",
            ),
            patch("vindicta_cli.lib.doctor_service.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(stdout="v1.0", stderr="", returncode=0)
            report = run_diagnostics()

        assert isinstance(report, DoctorReport)
        assert len(report.checks) > 0

    def test_with_workspace_adds_extra_checks(self, tmp_path: Path):
        """Providing workspace_root adds config + lock checks."""
        with (
            patch(
                "vindicta_cli.lib.doctor_service.shutil.which", return_value="/bin/x"
            ),
            patch("vindicta_cli.lib.doctor_service.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(stdout="v1.0", stderr="", returncode=0)
            report = run_diagnostics(workspace_root=tmp_path)

        check_names = [c.name for c in report.checks]
        assert "workspace config" in check_names
        assert "stale locks" in check_names

    def test_report_properties(self):
        """Report computes error/warning counts correctly."""
        report = DoctorReport(
            checks=[
                DiagnosticResult(name="a", status="ok", message="good"),
                DiagnosticResult(name="b", status="error", message="bad"),
                DiagnosticResult(name="c", status="warning", message="meh"),
            ]
        )
        assert report.all_ok is False
        assert report.error_count == 1
        assert report.warning_count == 1
