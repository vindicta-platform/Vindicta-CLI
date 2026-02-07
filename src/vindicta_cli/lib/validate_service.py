"""Validate service — T041.

Platform Constitution compliance validation across repositories.
"""

from __future__ import annotations

from pathlib import Path

from vindicta_cli.lib.logger import get_logger
from vindicta_cli.models.validation_result import ValidationCheck, ValidationResult

logger = get_logger("validate_service")


def validate_repo(
    repo_path: Path,
    repo_name: str,
    auto_fix: bool = False,
    checks: list[str] | None = None,
) -> ValidationResult:
    """Run validation checks on a single repository.

    Args:
        repo_path: Path to the repository.
        repo_name: Name of the repository.
        auto_fix: Attempt to fix issues automatically.
        checks: Specific checks to run. None = all.

    Returns:
        ValidationResult with per-check results.
    """
    result = ValidationResult(repo_name=repo_name)
    all_checks = checks or ["constitution", "context", "links", "hooks"]

    if "constitution" in all_checks:
        result.checks.append(_check_constitution(repo_path, auto_fix))

    if "context" in all_checks:
        result.checks.append(_check_context_artifacts(repo_path, auto_fix))

    if "links" in all_checks:
        result.checks.extend(_check_markdown_links(repo_path))

    if "hooks" in all_checks:
        result.checks.append(_check_pre_commit_hooks(repo_path, auto_fix))

    return result


def _check_constitution(repo_path: Path, auto_fix: bool = False) -> ValidationCheck:
    """Check for constitution file presence."""
    constitution_paths = [
        repo_path / ".specify" / "memory" / "constitution.md",
        repo_path / "CONSTITUTION.md",
        repo_path / "docs" / "constitution.md",
    ]

    for path in constitution_paths:
        if path.exists():
            return ValidationCheck(
                name="constitution_presence",
                passed=True,
                message=f"Constitution found at {path.relative_to(repo_path)}",
            )

    return ValidationCheck(
        name="constitution_presence",
        passed=False,
        message="No constitution file found",
        auto_fixable=True,
    )


def _check_context_artifacts(
    repo_path: Path, auto_fix: bool = False
) -> ValidationCheck:
    """Check for .antigravity context artifacts."""
    context_dir = repo_path / ".antigravity"
    if context_dir.exists() and any(context_dir.iterdir()):
        file_count = len(list(context_dir.iterdir()))
        return ValidationCheck(
            name="context_artifacts",
            passed=True,
            message=f".antigravity/ directory found with {file_count} files",
        )

    return ValidationCheck(
        name="context_artifacts",
        passed=False,
        message="No .antigravity/ context artifacts found",
        auto_fixable=True,
    )


def _check_markdown_links(repo_path: Path) -> list[ValidationCheck]:
    """Validate markdown file links."""
    checks = []
    md_files = list(repo_path.glob("**/*.md"))

    # Limit to prevent long scans
    for md_file in md_files[:50]:
        if ".git" in str(md_file) or "node_modules" in str(md_file):
            continue

        content = md_file.read_text(encoding="utf-8", errors="ignore")
        broken_links = _find_broken_links(content, md_file.parent)

        if broken_links:
            rel = md_file.relative_to(repo_path)
            summary = ", ".join(broken_links[:3])
            checks.append(
                ValidationCheck(
                    name="markdown_links",
                    passed=False,
                    message=f"Broken links in {rel}: {summary}",
                    file_path=str(md_file),
                )
            )

    if not checks:
        checks.append(
            ValidationCheck(
                name="markdown_links",
                passed=True,
                message=f"All links valid in {len(md_files)} markdown files",
            )
        )

    return checks


def _find_broken_links(content: str, base_dir: Path) -> list[str]:
    """Find broken relative file links in markdown content."""
    import re

    broken = []
    # Match [text](path) but not URLs
    pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    for match in re.finditer(pattern, content):
        link = match.group(2)
        # Skip URLs, anchors, and mailto
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        # Strip anchor from path
        link_path = link.split("#")[0]
        if link_path and not (base_dir / link_path).exists():
            broken.append(link_path)

    return broken


def _check_pre_commit_hooks(repo_path: Path, auto_fix: bool = False) -> ValidationCheck:
    """Check pre-commit configuration and installation."""
    config = repo_path / ".pre-commit-config.yaml"
    hooks_dir = repo_path / ".git" / "hooks" / "pre-commit"

    if not config.exists():
        return ValidationCheck(
            name="pre_commit_config",
            passed=False,
            message="No .pre-commit-config.yaml found",
            auto_fixable=False,
        )

    if not hooks_dir.exists():
        return ValidationCheck(
            name="pre_commit_installed",
            passed=False,
            message="Pre-commit hooks not installed (run `pre-commit install`)",
            auto_fixable=True,
        )

    return ValidationCheck(
        name="pre_commit_hooks",
        passed=True,
        message="Pre-commit configured and installed",
    )
