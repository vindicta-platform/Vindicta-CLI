"""Setup service — T029.

Handles dependency installation, virtual environment creation,
and pre-commit hook setup for workspace repositories.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from vindicta_cli.lib.logger import get_logger

logger = get_logger("setup_service")


def setup_repo(
    repo_path: Path,
    repo_type: str = "python",
    skip_venv: bool = False,
    skip_hooks: bool = False,
    skip_node: bool = False,
) -> dict[str, bool]:
    """Set up a single repository.

    Args:
        repo_path: Path to the repository.
        repo_type: One of "python", "nodejs", "mixed".
        skip_venv: Skip virtual environment creation.
        skip_hooks: Skip pre-commit hook installation.
        skip_node: Skip Node.js dependency installation.

    Returns:
        Dict with setup step results.
    """
    results: dict[str, bool] = {}

    if repo_type in ("python", "mixed") and not skip_venv:
        results["venv"] = _create_venv(repo_path)
        results["python_deps"] = _install_python_deps(repo_path)

    if repo_type in ("nodejs", "mixed") and not skip_node:
        results["node_deps"] = _install_node_deps(repo_path)

    if not skip_hooks:
        results["hooks"] = _install_hooks(repo_path)

    return results


def _create_venv(repo_path: Path) -> bool:
    """Create a virtual environment using uv."""
    try:
        result = subprocess.run(
            ["uv", "venv"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            logger.info("Created venv for %s", repo_path.name)
            return True
        logger.warning("venv creation failed for %s: %s", repo_path.name, result.stderr)
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.error("venv error for %s: %s", repo_path.name, e)
        return False


def _install_python_deps(repo_path: Path) -> bool:
    """Install Python dependencies using uv."""
    pyproject = repo_path / "pyproject.toml"
    requirements = repo_path / "requirements.txt"

    if not pyproject.exists() and not requirements.exists():
        return True  # No deps to install

    try:
        cmd = ["uv", "pip", "install"]
        if pyproject.exists():
            cmd.extend(["-e", "."])
        elif requirements.exists():
            cmd.extend(["-r", "requirements.txt"])

        result = subprocess.run(
            cmd,
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            logger.info("Installed Python deps for %s", repo_path.name)
            return True
        logger.warning("Python deps failed for %s: %s", repo_path.name, result.stderr)
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.error("Python deps error for %s: %s", repo_path.name, e)
        return False


def _install_node_deps(repo_path: Path) -> bool:
    """Install Node.js dependencies using npm."""
    package_json = repo_path / "package.json"
    if not package_json.exists():
        return True  # No package.json

    try:
        result = subprocess.run(
            ["npm", "install"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            logger.info("Installed Node deps for %s", repo_path.name)
            return True
        logger.warning("Node deps failed for %s: %s", repo_path.name, result.stderr)
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.error("Node deps error for %s: %s", repo_path.name, e)
        return False


def _install_hooks(repo_path: Path) -> bool:
    """Install pre-commit hooks."""
    pre_commit_config = repo_path / ".pre-commit-config.yaml"
    if not pre_commit_config.exists():
        return True  # No hooks to install

    try:
        result = subprocess.run(
            ["pre-commit", "install"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            logger.info("Installed hooks for %s", repo_path.name)
            return True
        logger.warning("Hook install failed for %s: %s", repo_path.name, result.stderr)
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.error("Hook install error for %s: %s", repo_path.name, e)
        return False
