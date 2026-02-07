<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles:
  - Technical Context: Python 3.11+ → Python 3.10+ (aligns with pyproject.toml)
- Added sections:
  - Principle VIII: Commit Discipline (atomic commits after Red/Green cycles)
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md - No changes needed (Constitution Check still valid)
  ✅ spec-template.md - No changes needed
  ✅ tasks-template.md - "Commit after each task" note already present (line 477)
- Follow-up TODOs: None
-->

# Vindicta-CLI Constitution

## Core Principles

### I. Library-First Architecture

Every feature MUST start as a standalone library before CLI integration. Libraries MUST be:
- Self-contained with clear boundaries
- Independently testable without CLI dependencies
- Fully documented with API contracts
- Purpose-driven (no organizational-only libraries)

**Rationale**: Library-first design ensures reusability across the platform, enables independent testing, and prevents tight coupling between CLI commands and business logic.

### II. CLI Interface Contract

Every library MUST expose functionality via a Typer-based CLI command. CLI commands MUST follow:
- Text I/O protocol: stdin/args → stdout, errors → stderr
- Support both JSON and human-readable output formats
- Provide `--help` documentation for all commands
- Follow the `vindicta [domain] [action]` naming convention

**Rationale**: Consistent CLI interfaces ensure predictable behavior, enable scripting and automation, and maintain compatibility with platform workflows.

### III. Test-First Development (NON-NEGOTIABLE)

Test-Driven Development (TDD) is MANDATORY for all implementations:
- Tests MUST be written before implementation
- Tests MUST be reviewed and approved by user before implementation begins
- Tests MUST fail initially (Red phase)
- Implementation proceeds only after failing tests are confirmed (Green phase)
- Refactoring follows successful implementation (Refactor phase)

**Rationale**: TDD ensures code correctness, prevents regression, and serves as living documentation. The Red-Green-Refactor cycle is non-negotiable to maintain code quality and reliability.

### IV. Integration Testing

Integration tests are REQUIRED for the following scenarios:
- New library contract tests (verify library API contracts)
- Contract changes (ensure backward compatibility or explicit breaking changes)
- Inter-service communication (validate service boundaries)
- Shared schema validation (ensure data contract integrity)

**Rationale**: Integration tests verify that components work together correctly and prevent breaking changes from propagating across the platform.

### V. Observability

All CLI commands and libraries MUST implement structured observability:
- Text I/O ensures debuggability (human-readable logs)
- Structured logging REQUIRED for all operations (JSON format for machine parsing)
- Error messages MUST include actionable context
- Performance metrics MUST be logged for long-running operations

**Rationale**: Observability enables rapid debugging, performance monitoring, and operational insights without requiring code changes.

### VI. Versioning &amp; Breaking Changes

All libraries and CLI commands MUST follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes (incompatible API changes)
- MINOR: New features (backward-compatible additions)
- PATCH: Bug fixes (backward-compatible fixes)

Breaking changes MUST include:
- Migration guide in CHANGELOG.md
- Deprecation warnings in prior MINOR version
- User notification before MAJOR version release

**Rationale**: Semantic versioning provides clear expectations for users and enables safe upgrades without unexpected breakage.

### VII. Simplicity &amp; YAGNI

Start simple and add complexity only when justified:
- Implement the simplest solution that meets requirements
- YAGNI (You Aren't Gonna Need It) principles apply
- Complexity MUST be justified in implementation plan
- Prefer composition over inheritance
- Avoid premature optimization

**Rationale**: Simple code is easier to understand, test, and maintain. Complexity should be added incrementally based on actual needs, not anticipated future requirements.


### VIII. Commit Discipline

All development MUST follow atomic commit practices:
- Commit after each Red/Green cycle (failing test → passing implementation)
- Commit after each Refactor phase
- Each commit MUST be self-contained and independently revertible
- Commit messages MUST follow Conventional Commits format (`type(scope): description`)
- Never bundle unrelated changes in a single commit

**Rationale**: Atomic commits create a clear, auditable history that supports bisecting, code review, and safe rollbacks. Coupling commits to TDD cycles ensures every commit represents a verified state.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Framework**: Typer (CLI), uv (package management), ruff (linting)
**Testing**: pytest with contract and integration test support
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: Single project (CLI tool)
**Performance Goals**: &lt;100ms response time for simple commands, &lt;5s for complex operations
**Constraints**: Must integrate with existing Vindicta Platform services and respect MCP-First Mandate
**Scale/Scope**: 20+ domain commands, 100+ total CLI commands across all domains

## Development Workflow

The Vindicta-CLI follows the Spec-Driven Development (SDD) lifecycle:

1. **Specify**: Create tech-agnostic user stories and acceptance criteria in `spec.md`
2. **Clarify**: Three-cycle clarification (Ambiguity, Component Impact, Failure Mode)
3. **Plan**: Document technical architecture, file changes, and risk assessment in `plan.md`
4. **Tasks**: Generate dependency-ordered task list (MODELS → SERVICES → ENDPOINTS) in `tasks.md`
5. **Implement**: Execute atomic TDD commits following Red-Green-Refactor cycle
6. **Verify**: Complete verification checklist with evidence and testing results

All SDD bundles MUST reside in `.specify/specs/[ID]-[name]/` and be approved before implementation.

## Quality Gates

All code MUST pass the following quality gates before merge:

1. **Linting &amp; Formatting**: All commits MUST pass `ruff check` and `ruff format` pre-commit hooks
2. **Test Coverage**: Critical paths MUST have unit or integration tests (&gt;80% coverage)
3. **Link Integrity**: Documentation MUST pass markdown link validation
4. **Constitution Compliance**: All implementations MUST align with these principles

## Governance

This constitution supersedes all other development practices for Vindicta-CLI.

**Amendment Process**:
- Amendments REQUIRE documentation of rationale and impact analysis
- Amendments REQUIRE user approval before adoption
- Amendments REQUIRE migration plan for existing code
- Version MUST be incremented according to semantic versioning rules

**Compliance Review**:
- All PRs MUST verify constitution compliance
- Complexity MUST be justified in implementation plan
- Violations MUST be documented with rationale for exception

**Runtime Guidance**: Developers should reference `.specify/templates/` for SDD workflow execution and `.antigravity/` for agent-specific development guidance

**Version**: 1.1.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
