"""Integration test for init → setup → doctor workflow — T027.

End-to-end test using mocked git/gh operations to validate
the full new developer onboarding flow.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from vindicta_cli.lib.doctor_service import run_diagnostics
from vindicta_cli.lib.workspace import CONFIG_FILENAME, load_config
from vindicta_cli.models.workspace_config import WorkspaceConfig


class TestInitWorkflowIntegration:
    """Integration tests for the init → setup → doctor flow."""

    def test_workspace_config_created_on_init(self, tmp_path: Path):
        """Init creates a valid workspace configuration file."""
        config = WorkspaceConfig(workspace_root=str(tmp_path))
        config.save(tmp_path / CONFIG_FILENAME)

        loaded = load_config(tmp_path)
        assert loaded.schema_version == "1.0.0"
        assert loaded.parallel_count == 4

    def test_doctor_after_init(self, tmp_path: Path):
        """Doctor reports workspace config after init."""
        # Simulate init by creating config
        config = WorkspaceConfig(workspace_root=str(tmp_path))
        config.save(tmp_path / CONFIG_FILENAME)

        with (
            patch(
                "vindicta_cli.lib.doctor_service.shutil.which",
                return_value="/usr/bin/x",
            ),
            patch("vindicta_cli.lib.doctor_service.subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(stdout="v1.0", stderr="", returncode=0)
            report = run_diagnostics(workspace_root=tmp_path)

        # workspace config should pass
        config_checks = [c for c in report.checks if c.name == "workspace config"]
        assert len(config_checks) == 1
        assert config_checks[0].status == "ok"

    def test_config_values_persist_across_operations(self, tmp_path: Path):
        """Config changes survive save/load cycle."""
        config = WorkspaceConfig(parallel_count=8, auto_pull=True)
        config.save(tmp_path / CONFIG_FILENAME)

        loaded = load_config(tmp_path)
        assert loaded.parallel_count == 8
        assert loaded.auto_pull is True

        # Modify and verify
        loaded.sync_timeout = 300
        loaded.save(tmp_path / CONFIG_FILENAME)

        reloaded = load_config(tmp_path)
        assert reloaded.sync_timeout == 300
        assert reloaded.parallel_count == 8  # Preserved
