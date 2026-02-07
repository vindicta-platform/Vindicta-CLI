# Implementation Plan: Developer Commands for Platform Management

**Branch**: `001-dev-commands` | **Date**: 2026-02-07 | **Spec**: [spec.md](file:///c:/Users/bfoxt/Github/vindicta-platform/Vindicta-CLI/specs/001-dev-commands/spec.md)
**Input**: Feature specification from `/specs/001-dev-commands/spec.md`

## Summary

Implement a `vindicta dev` command group providing workspace lifecycle management for the 26-repository Vindicta Platform. Commands include `init`, `sync`, `setup`, `status`, `validate`, `doctor`, `clean`, and `config`. The implementation follows a Library-First architecture: each command's logic lives in a standalone service library under `src/vindicta_cli/lib/`, exposed through Typer CLI commands under `src/vindicta_cli/cli/dev/`. External operations delegate to `gh` CLI for GitHub and MCP filesystem server for file operations (with direct fallback). All operations emit structured JSON logs to `.vindicta/logs/` and display Rich progress indicators by default.

## Technical Context

**Language/Version**: Python 3.11+ (requires-python >=3.10 per pyproject.toml)
**Primary Dependencies**: Typer >=0.12, Rich >=13.0 (already declared); new: PyYAML (workspace config), tenacity (retry logic)
**Storage**: Local filesystem — `.vindicta-workspace.yml` (workspace config), `.vindicta/logs/` (structured logs)
**Testing**: pytest >=8.0 (already in dev deps), pytest-mock, pytest-tmp-files
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: Single project (CLI tool)
**Performance Goals**: <100ms for simple commands (config get/set), <5s for status, <2min for sync (26 repos, parallel), <10min for init
**Constraints**: MCP-first for file ops, `gh` CLI for GitHub ops, exponential backoff retry (3×: 1s/2s/4s)
**Scale/Scope**: 8 commands in `dev` domain, 34 functional requirements, 26 repositories to manage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                        | Status | Evidence                                                                                                                   |
| -------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------- |
| I. Library-First                 | ✅ PASS | Each command backed by independent service library in `src/vindicta_cli/lib/`                                              |
| II. CLI Interface Contract       | ✅ PASS | All commands follow `vindicta dev [action]` pattern via Typer; support `--json` and `--verbose` flags; text I/O protocol   |
| III. Test-First (NON-NEGOTIABLE) | ✅ PASS | Tests defined in `tests/unit/`, `tests/integration/`, `tests/contract/`; TDD Red-Green-Refactor enforced per task ordering |
| IV. Integration Testing          | ✅ PASS | Integration tests verify git operations, workspace lifecycle, and multi-repo sync                                          |
| V. Observability                 | ✅ PASS | Structured JSON logs to `.vindicta/logs/`, Rich console output, log rotation (30d/100MB)                                   |
| VI. Versioning                   | ✅ PASS | CLI follows semver via pyproject.toml; workspace config includes schema version                                            |
| VII. Simplicity & YAGNI          | ✅ PASS | Minimal dependencies (PyYAML, tenacity); composition-based architecture; no ORM, no DB                                     |

**GATE PASSED** — Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-dev-commands/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contract docs)
│   └── cli-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/vindicta_cli/
├── __init__.py
├── main.py                    # Root Typer app, registers sub-apps
├── cli/
│   ├── __init__.py
│   └── dev/
│       ├── __init__.py        # dev sub-app registration
│       ├── init_cmd.py        # vindicta dev init
│       ├── sync_cmd.py        # vindicta dev sync
│       ├── setup_cmd.py       # vindicta dev setup
│       ├── status_cmd.py      # vindicta dev status
│       ├── validate_cmd.py    # vindicta dev validate
│       ├── doctor_cmd.py      # vindicta dev doctor
│       ├── clean_cmd.py       # vindicta dev clean
│       └── config_cmd.py      # vindicta dev config
├── lib/
│   ├── __init__.py
│   ├── workspace.py           # Workspace discovery, config I/O
│   ├── repository.py          # Repository model, git operations
│   ├── registry.py            # Repository registry (26 repos, tiers)
│   ├── sync_service.py        # Parallel fetch/pull logic
│   ├── setup_service.py       # Dependency installation, hooks
│   ├── validate_service.py    # Constitution & compliance checks
│   ├── doctor_service.py      # Tool detection, diagnostics
│   ├── clean_service.py       # Artifact cleanup, disk accounting
│   ├── config_service.py      # Config get/set/list
│   ├── mcp_client.py          # MCP filesystem server bridge
│   ├── gh_client.py           # GitHub CLI wrapper
│   ├── retry.py               # Exponential backoff (tenacity config)
│   └── logger.py              # Structured JSON logger, rotation
└── models/
    ├── __init__.py
    ├── workspace_config.py    # WorkspaceConfig dataclass
    ├── repo_info.py           # RepoInfo dataclass
    ├── validation_result.py   # ValidationResult dataclass
    └── health_status.py       # HealthStatus dataclass

tests/
├── conftest.py                # Shared fixtures (tmp workspace, mock repos)
├── unit/
│   ├── test_workspace.py
│   ├── test_repository.py
│   ├── test_registry.py
│   ├── test_sync_service.py
│   ├── test_validate_service.py
│   ├── test_doctor_service.py
│   ├── test_clean_service.py
│   ├── test_config_service.py
│   ├── test_retry.py
│   └── test_logger.py
├── integration/
│   ├── test_init_workflow.py
│   ├── test_sync_workflow.py
│   └── test_validate_workflow.py
└── contract/
    └── test_cli_contract.py   # CLI output format contracts
```

**Structure Decision**: Single project layout using `src/vindicta_cli/` with three internal layers: `models/` (data classes), `lib/` (service logic), `cli/` (Typer command wrappers). This follows Library-First Architecture (Principle I) — each service in `lib/` is independently testable without CLI coupling.

## Complexity Tracking

> No Constitution Check violations. No complexity justifications required.

| Aspect         | Decision                                  | Rationale                                                              |
| -------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| MCP Client     | Thin wrapper with fallback                | Constitution mandates MCP-first; fallback keeps CLI usable standalone  |
| Parallel Sync  | `asyncio.gather` with concurrency limiter | Simplest approach for parallel git operations; no thread pool overhead |
| Config Storage | YAML file (no DB)                         | Simplicity principle — flat file sufficient for workspace config       |
