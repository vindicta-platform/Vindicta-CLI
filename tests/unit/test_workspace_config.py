"""Unit tests for WorkspaceConfig model — T006.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations

from pathlib import Path

import pytest


class TestWorkspaceConfigDefaults:
    """Test that WorkspaceConfig has sensible defaults."""

    def test_default_schema_version(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.schema_version == "1.0.0"

    def test_default_parallel_count(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.parallel_count == 4

    def test_default_auto_pull_is_false(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.auto_pull is False

    def test_default_auto_fix_is_false(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.auto_fix is False

    def test_default_verbose_is_false(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.verbose is False

    def test_default_json_output_is_false(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.json_output is False

    def test_default_repositories_is_empty(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        assert config.repositories == []


class TestWorkspaceConfigSerialization:
    """Test YAML serialization/deserialization."""

    def test_to_yaml_string(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config = WorkspaceConfig()
        yaml_str = config.to_yaml()
        assert "schema_version" in yaml_str
        assert "1.0.0" in yaml_str

    def test_from_yaml_string(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        yaml_str = "schema_version: '1.0.0'\nparallel_count: 8\nauto_pull: true\n"
        config = WorkspaceConfig.from_yaml(yaml_str)
        assert config.parallel_count == 8
        assert config.auto_pull is True

    def test_roundtrip_serialization(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        original = WorkspaceConfig(parallel_count=8, auto_pull=True)
        yaml_str = original.to_yaml()
        restored = WorkspaceConfig.from_yaml(yaml_str)
        assert restored.parallel_count == original.parallel_count
        assert restored.auto_pull == original.auto_pull

    def test_save_and_load_file(self, tmp_path: Path):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        config_path = tmp_path / ".vindicta-workspace.yml"
        original = WorkspaceConfig(parallel_count=6)
        original.save(config_path)
        assert config_path.exists()

        loaded = WorkspaceConfig.load(config_path)
        assert loaded.parallel_count == 6


class TestWorkspaceConfigValidation:
    """Test validation rules."""

    def test_parallel_count_must_be_positive(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        with pytest.raises(ValueError):
            WorkspaceConfig(parallel_count=0)

    def test_parallel_count_max_16(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        with pytest.raises(ValueError):
            WorkspaceConfig(parallel_count=17)

    def test_sync_timeout_min_10(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        with pytest.raises(ValueError):
            WorkspaceConfig(sync_timeout=5)

    def test_sync_timeout_max_600(self):
        from vindicta_cli.models.workspace_config import WorkspaceConfig

        with pytest.raises(ValueError):
            WorkspaceConfig(sync_timeout=700)
