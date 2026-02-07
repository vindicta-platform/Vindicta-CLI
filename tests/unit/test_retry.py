"""Unit tests for retry logic — T010.

TDD Red Phase: These tests MUST fail before implementation.
"""

from __future__ import annotations

import pytest


class TestRetryConfig:
    """Test exponential backoff retry configuration."""

    def test_retry_decorator_exists(self):
        from vindicta_cli.lib.retry import with_retry

        assert callable(with_retry)

    def test_retries_on_exception(self):
        from vindicta_cli.lib.retry import with_retry

        call_count = 0

        @with_retry
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("network down")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 3

    def test_gives_up_after_max_attempts(self):
        from vindicta_cli.lib.retry import with_retry

        call_count = 0

        @with_retry
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise ConnectionError("permanent failure")

        with pytest.raises(ConnectionError):
            always_fails()

        assert call_count == 3  # 3 attempts per FR-025

    def test_does_not_retry_on_value_error(self):
        from vindicta_cli.lib.retry import with_retry

        call_count = 0

        @with_retry
        def bad_input():
            nonlocal call_count
            call_count += 1
            raise ValueError("bad input")

        with pytest.raises(ValueError):
            bad_input()

        assert call_count == 1  # No retry on ValueError
