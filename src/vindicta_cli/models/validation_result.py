"""Validation result models — T016."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationCheck:
    """Single validation check result."""

    name: str
    passed: bool
    message: str
    file_path: str | None = None
    line_number: int | None = None
    auto_fixable: bool = False
    fixed: bool = False


@dataclass
class ValidationResult:
    """Aggregated validation results for a repository."""

    repo_name: str
    checks: list[ValidationCheck] = field(default_factory=list)

    @property
    def total_passed(self) -> int:
        return sum(1 for c in self.checks if c.passed)

    @property
    def total_failed(self) -> int:
        return sum(1 for c in self.checks if not c.passed)

    @property
    def total_fixed(self) -> int:
        return sum(1 for c in self.checks if c.fixed)

    @property
    def compliance_score(self) -> float:
        total = len(self.checks)
        if total == 0:
            return 100.0
        return (self.total_passed / total) * 100

    @property
    def all_passed(self) -> bool:
        return self.total_failed == 0
