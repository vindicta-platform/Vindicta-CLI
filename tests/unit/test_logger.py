"""Unit tests for logger module — T009.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations

import json
from pathlib import Path


class TestJsonLogger:
    """Test structured JSON logging."""

    def test_creates_log_directory(self, tmp_path: Path):
        from vindicta_cli.lib.logger import setup_logging

        log_dir = tmp_path / ".vindicta" / "logs"
        setup_logging(log_dir=log_dir)
        assert log_dir.exists()

    def test_writes_json_log_entries(self, tmp_path: Path):
        from vindicta_cli.lib.logger import setup_logging

        log_dir = tmp_path / ".vindicta" / "logs"
        logger = setup_logging(log_dir=log_dir)
        logger.info("test message", extra={"command": "dev init"})

        log_files = list(log_dir.glob("vindicta-*.log"))
        assert len(log_files) >= 1

        content = log_files[0].read_text()
        lines = [line for line in content.strip().split("\n") if line]
        assert len(lines) >= 1

        entry = json.loads(lines[0])
        assert "timestamp" in entry
        assert "message" in entry
        assert entry["message"] == "test message"

    def test_log_entry_contains_required_fields(self, tmp_path: Path):
        from vindicta_cli.lib.logger import setup_logging

        log_dir = tmp_path / ".vindicta" / "logs"
        logger = setup_logging(log_dir=log_dir)
        logger.info("test", extra={"command": "dev sync", "duration": 1.5})

        log_files = list(log_dir.glob("vindicta-*.log"))
        content = log_files[0].read_text()
        entry = json.loads(content.strip().split("\n")[0])

        assert "timestamp" in entry
        assert "level" in entry
        assert "message" in entry

    def test_get_logger_returns_named_logger(self):
        from vindicta_cli.lib.logger import get_logger

        logger = get_logger("test_module")
        assert logger.name == "vindicta.test_module"
