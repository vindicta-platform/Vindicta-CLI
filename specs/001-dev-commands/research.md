# Research: Developer Commands for Platform Management

**Feature**: 001-dev-commands
**Date**: 2026-02-07

## Research Tasks & Findings

### 1. Typer CLI Architecture for Multi-Command Apps

**Decision**: Use Typer sub-applications to organize the `dev` command group.

**Rationale**: Typer natively supports `app.add_typer()` for composing sub-applications. This keeps each command in its own module while presenting a unified `vindicta dev [command]` experience. The existing `pyproject.toml` already declares `vindicta_cli.main:app` as the entry point.

**Alternatives considered**:
- Click groups: More verbose, less type-safe. Typer is already the project standard.
- Flat command registration: Would violate Library-First by mixing all commands in one module.

---

### 2. Parallel Git Operations with asyncio

**Decision**: Use `asyncio.gather()` with `asyncio.Semaphore` for parallel repository operations.

**Rationale**: Python's asyncio provides lightweight concurrency for I/O-bound git operations. `asyncio.subprocess` allows running `git` and `gh` CLI commands in parallel without threads. A semaphore limits concurrency to the configured level (default: 4).

**Alternatives considered**:
- `concurrent.futures.ThreadPoolExecutor`: Heavier, GIL contention for subprocess management. asyncio is cleaner for subprocess I/O.
- `multiprocessing`: Overkill for subprocess orchestration; complicates shared state.

---

### 3. MCP Filesystem Server Integration

**Decision**: Implement a thin `McpClient` wrapper that detects MCP filesystem server availability and delegates file operations, with synchronous fallback to standard Python `pathlib`/`shutil`.

**Rationale**: The MCP-first mandate (clarification Q3) requires using MCP filesystem server when available. The wrapper provides a unified interface: `read_file()`, `write_file()`, `list_directory()`, `create_directory()`. At startup, the CLI checks if the MCP server is running (via process/socket detection). If unavailable, operations fall back to direct Python file I/O.

**Alternatives considered**:
- Always use MCP: Would break standalone CLI usage.
- Always use direct I/O: Violates MCP-first mandate.

---

### 4. Workspace Configuration Format

**Decision**: Use YAML (`.vindicta-workspace.yml`) with PyYAML for workspace configuration.

**Rationale**: YAML is human-readable, supports comments, and is already familiar in the Python ecosystem (pre-commit, GitHub Actions). PyYAML is a lightweight, well-maintained dependency. The config file stores repository registry, sync preferences, validation settings, and setup preferences.

**Alternatives considered**:
- TOML: Good for Python but less readable for nested structures (repository registry).
- JSON: No comment support; less human-friendly for manual editing.
- INI: Too flat for nested config structure.

---

### 5. Structured Logging Implementation

**Decision**: Use Python's built-in `logging` module with a custom JSON formatter writing to `.vindicta/logs/vindicta-YYYY-MM-DD.log`, plus Rich console handler for human output.

**Rationale**: Python's `logging` module supports multiple handlers, formatters, and log rotation (`RotatingFileHandler`). The JSON formatter outputs structured records with timestamp, command, args, duration, and outcome. Rich's `Console` provides spinners, progress bars, and colored output. No additional dependencies needed beyond Rich (already declared).

**Alternatives considered**:
- structlog: More powerful but adds a dependency; built-in logging is sufficient for this scope.
- loguru: Popular but non-standard; adds unnecessary dependency.

---

### 6. Retry Logic with tenacity

**Decision**: Use the `tenacity` library for exponential backoff retry on network operations.

**Rationale**: `tenacity` provides declarative retry configuration (`@retry` decorator) with exponential backoff, configurable stop/wait strategies, and callback hooks for logging attempts. It's the de facto Python standard for retry logic.

**Alternatives considered**:
- Manual retry loop: Error-prone, no standardized backoff.
- `backoff` library: Less actively maintained than tenacity.
- `urllib3.Retry`: Only for HTTP; we need retries around subprocess calls (git, gh).

---

### 7. Repository Registry Design

**Decision**: Embed a hardcoded registry of 26 repositories with tier assignments in `src/vindicta_cli/lib/registry.py`. Override with workspace config at runtime.

**Rationale**: The repository list and tiers are stable (platform governance defines them). A code-embedded registry provides a reliable default. The workspace config can override or extend this for future additions. This avoids external API calls during init discovery.

**Alternatives considered**:
- GitHub API discovery (`gh repo list`): Slow, requires auth, may include non-platform repos.
- External registry file: Adds a deployment artifact; code-embedded is simpler.

---

### 8. GitHub CLI (`gh`) Wrapper

**Decision**: Use `asyncio.subprocess` to invoke `gh` CLI commands, wrapping output parsing in `GhClient` class.

**Rationale**: The `gh` CLI handles authentication, rate limiting, and API pagination. Wrapping it preserves the MCP-First Mandate (don't duplicate GitHub MCP functionality) while ensuring the CLI works in environments without MCP. The wrapper parses JSON output (`--json` flag) for structured data.

**Alternatives considered**:
- PyGithub / github3.py: Would require separate auth management; violates decision to delegate to `gh`.
- Direct REST API: Would duplicate `gh` functionality; requires token management.

---

## Summary of New Dependencies

| Dependency | Purpose                        | Size Impact |
| ---------- | ------------------------------ | ----------- |
| PyYAML     | Workspace config I/O           | ~200KB      |
| tenacity   | Retry with exponential backoff | ~50KB       |

Both dependencies are widely used, well-maintained, and minimal in size. Total addition is ~250KB.
