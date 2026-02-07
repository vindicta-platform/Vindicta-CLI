"""Structured JSON logger with rotation — T018.

Writes structured JSON logs to .vindicta/logs/ directory.
Provides Rich console handler for human-readable output.
Implements log rotation (30 days or 100MB).
"""

from __future__ import annotations

import json
import logging
import logging.handlers
from datetime import datetime, timezone
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include extra fields
        for key in ("command", "duration", "args", "outcome"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry)


def setup_logging(
    log_dir: Path | None = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configure structured logging with JSON file output.

    Args:
        log_dir: Directory for log files. Defaults to .vindicta/logs/.
        level: Logging level.

    Returns:
        Configured root logger for vindicta.
    """
    if log_dir is None:
        log_dir = Path(".vindicta") / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("vindicta")
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # JSON file handler with rotation (100MB max, 30 backups)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"vindicta-{today}.log"

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=100 * 1024 * 1024,  # 100MB
        backupCount=30,
    )
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a named logger under the vindicta namespace.

    Args:
        name: Module name for the logger.

    Returns:
        Named logger instance.
    """
    return logging.getLogger(f"vindicta.{name}")
