"""Unit tests for setup service — T025.

Tests for venv creation, Python deps, Node deps, and hook installation.
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from vindicta_cli.lib.setup_service import (
    _create_venv,
    _install_hooks,
    _install_node_deps,
    _install_python_deps,
    setup_repo,
)


class TestSetupRepo:
    """Tests for setup_repo orchestrator."""

    def test_python_repo_creates_venv_and_deps(self, tmp_path: Path):
        """Python repo runs venv + deps + hooks."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            results = setup_repo(tmp_path, repo_type="python")

        assert "venv" in results
        assert "python_deps" in results

    def test_nodejs_repo_installs_node_deps(self, tmp_path: Path):
        """Node.js repo runs npm install + hooks."""
        (tmp_path / "package.json").write_text("{}")

        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            results = setup_repo(tmp_path, repo_type="nodejs")

        assert "node_deps" in results

    def test_skip_flags_honored(self, tmp_path: Path):
        """Skip flags prevent corresponding setup steps."""
        results = setup_repo(
            tmp_path,
            repo_type="python",
            skip_venv=True,
            skip_hooks=True,
        )

        assert "venv" not in results
        assert "hooks" not in results

    def test_mixed_repo_runs_both(self, tmp_path: Path):
        """Mixed repo runs Python + Node deps."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")
        (tmp_path / "package.json").write_text("{}")

        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            results = setup_repo(tmp_path, repo_type="mixed")

        assert "venv" in results
        assert "python_deps" in results
        assert "node_deps" in results


class TestCreateVenv:
    """Tests for _create_venv helper."""

    def test_success_returns_true(self, tmp_path: Path):
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert _create_venv(tmp_path) is True

    def test_failure_returns_false(self, tmp_path: Path):
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="error")
            assert _create_venv(tmp_path) is False

    def test_timeout_returns_false(self, tmp_path: Path):
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="uv", timeout=30)
            assert _create_venv(tmp_path) is False


class TestInstallPythonDeps:
    """Tests for _install_python_deps helper."""

    def test_no_deps_files_returns_true(self, tmp_path: Path):
        """No pyproject.toml or requirements.txt → success."""
        assert _install_python_deps(tmp_path) is True

    def test_pyproject_triggers_editable_install(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = _install_python_deps(tmp_path)

        assert result is True
        args = mock_run.call_args[0][0]
        assert "-e" in args and "." in args


class TestInstallNodeDeps:
    """Tests for _install_node_deps helper."""

    def test_no_package_json_returns_true(self, tmp_path: Path):
        assert _install_node_deps(tmp_path) is True

    def test_with_package_json_runs_npm(self, tmp_path: Path):
        (tmp_path / "package.json").write_text("{}")
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = _install_node_deps(tmp_path)

        assert result is True
        args = mock_run.call_args[0][0]
        assert "npm" in args


class TestInstallHooks:
    """Tests for _install_hooks helper."""

    def test_no_config_returns_true(self, tmp_path: Path):
        assert _install_hooks(tmp_path) is True

    def test_with_config_runs_precommit(self, tmp_path: Path):
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []")
        with patch("vindicta_cli.lib.setup_service.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = _install_hooks(tmp_path)

        assert result is True
