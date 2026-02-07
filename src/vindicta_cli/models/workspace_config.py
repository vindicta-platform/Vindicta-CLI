"""Workspace configuration model — T013.

Persistent workspace settings stored in .vindicta-workspace.yml.
Supports YAML serialization/deserialization with validation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class WorkspaceConfig:
    """Workspace configuration persisted to .vindicta-workspace.yml."""

    # Identity
    schema_version: str = "1.0.0"
    workspace_root: str = "."

    # Repository Registry
    repositories: list[dict[str, Any]] = field(default_factory=list)

    # Sync Preferences
    parallel_count: int = 4
    auto_pull: bool = False
    sync_timeout: int = 120

    # Validation Preferences
    auto_fix: bool = False
    constitution_check: bool = True
    link_check: bool = True

    # Setup Preferences
    install_hooks: bool = True
    create_venvs: bool = True

    # Global
    default_tier: str | None = None
    verbose: bool = False
    json_output: bool = False

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not (1 <= self.parallel_count <= 16):
            raise ValueError(f"parallel_count must be 1-16, got {self.parallel_count}")
        if not (10 <= self.sync_timeout <= 600):
            raise ValueError(f"sync_timeout must be 10-600, got {self.sync_timeout}")

    def to_yaml(self) -> str:
        """Serialize configuration to YAML string."""
        data = asdict(self)
        return yaml.dump(data, default_flow_style=False, sort_keys=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> WorkspaceConfig:
        """Deserialize configuration from YAML string."""
        data = yaml.safe_load(yaml_str) or {}
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def save(self, path: Path) -> None:
        """Save configuration to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_yaml())

    @classmethod
    def load(cls, path: Path) -> WorkspaceConfig:
        """Load configuration from file."""
        if not path.exists():
            return cls()
        return cls.from_yaml(path.read_text())
