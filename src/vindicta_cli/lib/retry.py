"""Retry logic with exponential backoff — T019.

Configures tenacity for network operation retries.
3 attempts with delays: 1s, 2s, 4s (total ~7s max wait).
Only retries on network-related exceptions.
"""

from __future__ import annotations

import logging

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger("vindicta.retry")

# Network-related exceptions that should trigger retries
RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    OSError,
)


def with_retry(func):
    """Decorator for exponential backoff retry on network failures.

    Retries up to 3 times with exponential backoff (1s, 2s, 4s).
    Only retries on network-related exceptions (ConnectionError,
    TimeoutError, OSError). Other exceptions propagate immediately.
    """
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )(func)
