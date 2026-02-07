"""Config service — T054.

Workspace configuration management operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vindicta_cli.lib.logger import get_logger
from vindicta_cli.lib.workspace import load_config, save_config
from vindicta_cli.models.workspace_config import WorkspaceConfig

logger = get_logger("config_service")

# Valid configuration keys with types and descriptions
CONFIG_KEYS = {
    "parallel_count": {
        "type": int,
        "min": 1,
        "max": 16,
        "desc": "Max concurrent operations",
    },
    "auto_pull": {"type": bool, "desc": "Auto-pull on sync"},
    "sync_timeout": {
        "type": int,
        "min": 10,
        "max": 600,
        "desc": "Sync timeout (seconds)",
    },
    "auto_fix": {"type": bool, "desc": "Auto-fix validation issues"},
    "constitution_check": {"type": bool, "desc": "Enable constitution checks"},
    "link_check": {"type": bool, "desc": "Enable markdown link checks"},
    "install_hooks": {"type": bool, "desc": "Install pre-commit hooks on setup"},
    "create_venvs": {"type": bool, "desc": "Create virtual environments on setup"},
    "verbose": {"type": bool, "desc": "Enable verbose output"},
    "json_output": {"type": bool, "desc": "Default to JSON output"},
}


def get_config_value(workspace_root: Path, key: str) -> Any:
    """Get a configuration value.

    Args:
        workspace_root: Workspace root path.
        key: Configuration key.

    Returns:
        Current value.

    Raises:
        ValueError: If key is invalid.
    """
    if key not in CONFIG_KEYS:
        raise ValueError(f"Unknown config key: {key}")

    config = load_config(workspace_root)
    return getattr(config, key)


def set_config_value(workspace_root: Path, key: str, value: str) -> Any:
    """Set a configuration value.

    Args:
        workspace_root: Workspace root path.
        key: Configuration key.
        value: New value as string (will be coerced).

    Returns:
        Coerced value that was set.

    Raises:
        ValueError: If key is invalid or value can't be coerced.
    """
    if key not in CONFIG_KEYS:
        raise ValueError(f"Unknown config key: {key}")

    spec = CONFIG_KEYS[key]
    coerced = _coerce_value(value, spec["type"])

    # Range validation
    if "min" in spec and coerced < spec["min"]:
        raise ValueError(f"{key} must be >= {spec['min']}")
    if "max" in spec and coerced > spec["max"]:
        raise ValueError(f"{key} must be <= {spec['max']}")

    config = load_config(workspace_root)
    setattr(config, key, coerced)
    save_config(config, workspace_root)

    logger.info("Set %s = %s", key, coerced)
    return coerced


def list_config(workspace_root: Path) -> dict[str, Any]:
    """List all configuration values.

    Returns:
        Dict of key -> (value, description) pairs.
    """
    config = load_config(workspace_root)
    return {
        key: {
            "value": getattr(config, key),
            "description": spec["desc"],
            "type": spec["type"].__name__,
        }
        for key, spec in CONFIG_KEYS.items()
    }


def reset_config(workspace_root: Path, key: str | None = None) -> None:
    """Reset configuration to defaults.

    Args:
        workspace_root: Workspace root path.
        key: Specific key to reset. None = reset all.
    """
    if key is None:
        config = WorkspaceConfig()
    else:
        if key not in CONFIG_KEYS:
            raise ValueError(f"Unknown config key: {key}")
        config = load_config(workspace_root)
        default = WorkspaceConfig()
        setattr(config, key, getattr(default, key))

    save_config(config, workspace_root)
    logger.info("Reset config: %s", key or "all")


def _coerce_value(value: str, target_type: type) -> Any:
    """Coerce string value to target type."""
    if target_type is bool:
        if value.lower() in ("true", "1", "yes", "on"):
            return True
        if value.lower() in ("false", "0", "no", "off"):
            return False
        raise ValueError(f"Cannot convert '{value}' to bool")
    if target_type is int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot convert '{value}' to int")
    return value
