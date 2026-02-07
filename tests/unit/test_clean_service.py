"""Unit tests for clean service — T050.

Tests for artifact scanning, dry-run, disk space accounting.
"""

from pathlib import Path

from vindicta_cli.lib.clean_service import (
    _format_size,
    _get_size,
    clean_repo,
)


class TestCleanRepo:
    """Tests for clean_repo function."""

    def test_finds_pycache(self, tmp_path: Path):
        """Detects __pycache__ directories."""
        cache_dir = tmp_path / "src" / "__pycache__"
        cache_dir.mkdir(parents=True)
        (cache_dir / "module.pyc").write_bytes(b"x" * 1024)

        result = clean_repo(tmp_path, "TestRepo", dry_run=True)
        assert result.items_found >= 1
        assert result.bytes_reclaimed > 0

    def test_finds_node_modules(self, tmp_path: Path):
        """Detects node_modules directories."""
        nm = tmp_path / "node_modules"
        nm.mkdir()
        (nm / "package.json").write_text("{}")

        result = clean_repo(tmp_path, "TestRepo", types=["node"], dry_run=True)
        assert result.items_found >= 1

    def test_finds_venv(self, tmp_path: Path):
        """Detects .venv directories."""
        venv = tmp_path / ".venv"
        venv.mkdir()
        (venv / "pyvenv.cfg").write_text("home = /usr/bin")

        result = clean_repo(tmp_path, "TestRepo", types=["venv"], dry_run=True)
        assert result.items_found >= 1

    def test_dry_run_does_not_delete(self, tmp_path: Path):
        """Dry run reports but doesn't remove."""
        cache = tmp_path / "__pycache__"
        cache.mkdir()
        (cache / "test.pyc").write_bytes(b"data")

        result = clean_repo(tmp_path, "TestRepo", dry_run=True)
        assert cache.exists()  # Still there
        assert result.items_removed == 0  # Nothing removed
        assert result.bytes_reclaimed > 0  # But size reported

    def test_actual_clean_removes(self, tmp_path: Path):
        """Actual clean removes artifacts."""
        cache = tmp_path / "__pycache__"
        cache.mkdir()
        (cache / "test.pyc").write_bytes(b"data")

        result = clean_repo(tmp_path, "TestRepo", types=["python"])
        assert not cache.exists()
        assert result.items_removed >= 1

    def test_type_filter(self, tmp_path: Path):
        """Only cleans specified types."""
        (tmp_path / "__pycache__").mkdir()
        nm = tmp_path / "node_modules"
        nm.mkdir()

        result = clean_repo(tmp_path, "TestRepo", types=["python"], dry_run=True)
        assert any("__pycache__" in d for d in result.details)

    def test_empty_repo(self, tmp_path: Path):
        """No artifacts to clean."""
        result = clean_repo(tmp_path, "TestRepo")
        assert result.items_found == 0
        assert result.bytes_reclaimed == 0

    def test_skips_git_internals(self, tmp_path: Path):
        """Doesn't clean inside .git directory."""
        git_cache = tmp_path / ".git" / "__pycache__"
        git_cache.mkdir(parents=True)

        result = clean_repo(tmp_path, "TestRepo", types=["python"], dry_run=True)
        # __pycache__ inside .git should be skipped
        git_details = [d for d in result.details if ".git" in d]
        assert len(git_details) == 0


class TestFormatSize:
    """Tests for _format_size helper."""

    def test_bytes(self):
        assert "B" in _format_size(500)

    def test_kilobytes(self):
        assert "KB" in _format_size(2048)

    def test_megabytes(self):
        assert "MB" in _format_size(1024 * 1024 * 5)

    def test_gigabytes(self):
        assert "GB" in _format_size(1024 * 1024 * 1024 * 2)


class TestGetSize:
    """Tests for _get_size helper."""

    def test_file_size(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_bytes(b"x" * 100)
        assert _get_size(f) == 100

    def test_dir_size(self, tmp_path: Path):
        (tmp_path / "a.txt").write_bytes(b"x" * 50)
        (tmp_path / "b.txt").write_bytes(b"y" * 30)
        total = _get_size(tmp_path)
        assert total == 80
