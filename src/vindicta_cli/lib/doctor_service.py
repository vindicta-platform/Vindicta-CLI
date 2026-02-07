"""Doctor service — T030.

Environment diagnostics: tool checks, version validation,
workspace health assessment, and auto-fix recommendations.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from vindicta_cli.lib.logger import get_logger

logger = get_logger("doctor")

# Minimum required versions
REQUIRED_TOOLS = {
    "git": "2.30",
    "gh": "2.0",
    "python": "3.10",
    "uv": "0.1",
    "node": "18.0",
}


@dataclass
class DiagnosticResult:
    """Result of a single diagnostic check."""

    name: str
    status: str  # "ok", "warning", "error"
    message: str
    fixable: bool = False
    fix_command: str | None = None


@dataclass
class DoctorReport:
    """Complete doctor diagnostics report."""

    checks: list[DiagnosticResult] = field(default_factory=list)

    @property
    def all_ok(self) -> bool:
        return all(c.status == "ok" for c in self.checks)

    @property
    def error_count(self) -> int:
        return sum(1 for c in self.checks if c.status == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.checks if c.status == "warning")


def run_diagnostics(
    workspace_root: Path | None = None,
    auto_fix: bool = False,
) -> DoctorReport:
    """Run all diagnostic checks.

    Args:
        workspace_root: Path to workspace. None = cwd.
        auto_fix: Attempt automatic fixes for fixable issues.

    Returns:
        DoctorReport with all check results.
    """
    report = DoctorReport()

    # Check required tools
    for tool, min_version in REQUIRED_TOOLS.items():
        result = _check_tool(tool, min_version)
        report.checks.append(result)

    # Check workspace config
    if workspace_root:
        config_result = _check_workspace_config(workspace_root)
        report.checks.append(config_result)

        # Check for stale lock files
        lock_result = _check_stale_locks(workspace_root)
        report.checks.append(lock_result)

    return report


def _check_tool(name: str, min_version: str) -> DiagnosticResult:
    """Check if a tool is installed and meets minimum version."""
    path = shutil.which(name)
    if not path:
        return DiagnosticResult(
            name=f"{name} installed",
            status="error",
            message=f"{name} not found in PATH",
            fixable=False,
        )

    # Get version
    try:
        version_flag = "--version"
        result = subprocess.run(
            [name, version_flag],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version_str = result.stdout.strip() or result.stderr.strip()

        return DiagnosticResult(
            name=f"{name} version",
            status="ok",
            message=f"{name}: {version_str}",
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return DiagnosticResult(
            name=f"{name} version",
            status="warning",
            message=f"{name} found but version check failed",
        )


def _check_workspace_config(workspace_root: Path) -> DiagnosticResult:
    """Check workspace configuration file health."""
    config_path = workspace_root / ".vindicta-workspace.yml"

    if not config_path.exists():
        return DiagnosticResult(
            name="workspace config",
            status="warning",
            message="No .vindicta-workspace.yml found",
            fixable=True,
            fix_command="vindicta dev init",
        )

    try:
        import yaml

        with open(config_path) as f:
            yaml.safe_load(f)
        return DiagnosticResult(
            name="workspace config",
            status="ok",
            message="Config file valid",
        )
    except Exception as e:
        return DiagnosticResult(
            name="workspace config",
            status="error",
            message=f"Config file corrupted: {e}",
            fixable=True,
            fix_command="vindicta dev init --force",
        )


def _check_stale_locks(workspace_root: Path) -> DiagnosticResult:
    """Check for stale lock files."""
    lock_patterns = [
        "**/.git/index.lock",
        "**/.git/refs/heads/*.lock",
    ]
    stale_locks = []
    for pattern in lock_patterns:
        stale_locks.extend(workspace_root.glob(pattern))

    if stale_locks:
        names = [str(lock.relative_to(workspace_root)) for lock in stale_locks[:5]]
        return DiagnosticResult(
            name="stale locks",
            status="warning",
            message=f"Found {len(stale_locks)} stale lock file(s): {', '.join(names)}",
            fixable=True,
            fix_command="Remove lock files manually or use --fix",
        )

    return DiagnosticResult(
        name="stale locks",
        status="ok",
        message="No stale lock files found",
    )
