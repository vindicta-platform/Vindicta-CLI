"""Unit tests for config service — T053.

Tests for get, set, list, reset, validation, and persistence.
"""

from pathlib import Path

import pytest

from vindicta_cli.lib.config_service import (
    CONFIG_KEYS,
    _coerce_value,
    get_config_value,
    list_config,
    reset_config,
    set_config_value,
)


class TestGetConfigValue:
    """Tests for get_config_value."""

    def test_get_default_value(self, tmp_path: Path):
        value = get_config_value(tmp_path, "parallel_count")
        assert value == 4

    def test_invalid_key_raises(self, tmp_path: Path):
        with pytest.raises(ValueError, match="Unknown config key"):
            get_config_value(tmp_path, "nonexistent_key")


class TestSetConfigValue:
    """Tests for set_config_value."""

    def test_set_int_value(self, tmp_path: Path):
        result = set_config_value(tmp_path, "parallel_count", "8")
        assert result == 8
        # Verify persistence
        assert get_config_value(tmp_path, "parallel_count") == 8

    def test_set_bool_value(self, tmp_path: Path):
        result = set_config_value(tmp_path, "auto_pull", "true")
        assert result is True

    def test_range_validation_min(self, tmp_path: Path):
        with pytest.raises(ValueError):
            set_config_value(tmp_path, "parallel_count", "0")

    def test_range_validation_max(self, tmp_path: Path):
        with pytest.raises(ValueError):
            set_config_value(tmp_path, "parallel_count", "20")

    def test_invalid_key_raises(self, tmp_path: Path):
        with pytest.raises(ValueError, match="Unknown config key"):
            set_config_value(tmp_path, "bad_key", "value")


class TestListConfig:
    """Tests for list_config."""

    def test_lists_all_keys(self, tmp_path: Path):
        config_data = list_config(tmp_path)
        assert len(config_data) == len(CONFIG_KEYS)
        for key in CONFIG_KEYS:
            assert key in config_data
            assert "value" in config_data[key]
            assert "description" in config_data[key]
            assert "type" in config_data[key]


class TestResetConfig:
    """Tests for reset_config."""

    def test_reset_single_key(self, tmp_path: Path):
        # Change a value
        set_config_value(tmp_path, "parallel_count", "8")
        assert get_config_value(tmp_path, "parallel_count") == 8

        # Reset it
        reset_config(tmp_path, "parallel_count")
        assert get_config_value(tmp_path, "parallel_count") == 4

    def test_reset_all(self, tmp_path: Path):
        set_config_value(tmp_path, "parallel_count", "8")
        set_config_value(tmp_path, "auto_pull", "true")

        reset_config(tmp_path)
        assert get_config_value(tmp_path, "parallel_count") == 4
        assert get_config_value(tmp_path, "auto_pull") is False

    def test_reset_invalid_key_raises(self, tmp_path: Path):
        with pytest.raises(ValueError):
            reset_config(tmp_path, "bad_key")


class TestCoerceValue:
    """Tests for _coerce_value helper."""

    def test_bool_true_variants(self):
        for val in ("true", "True", "1", "yes", "on"):
            assert _coerce_value(val, bool) is True

    def test_bool_false_variants(self):
        for val in ("false", "False", "0", "no", "off"):
            assert _coerce_value(val, bool) is False

    def test_bool_invalid(self):
        with pytest.raises(ValueError):
            _coerce_value("maybe", bool)

    def test_int_valid(self):
        assert _coerce_value("42", int) == 42

    def test_int_invalid(self):
        with pytest.raises(ValueError):
            _coerce_value("not-a-number", int)
