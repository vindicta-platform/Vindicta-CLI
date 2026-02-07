# Tasks: Developer Commands for Platform Management

**Input**: Design documents from `/specs/001-dev-commands/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: REQUIRED per Constitution Principle III (Test-First Development — NON-NEGOTIABLE). TDD Red-Green-Refactor cycle enforced.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, package scaffolding, and dependency configuration

- [ ] T001 Create source package structure: `src/vindicta_cli/__init__.py`, `src/vindicta_cli/cli/__init__.py`, `src/vindicta_cli/cli/dev/__init__.py`, `src/vindicta_cli/lib/__init__.py`, `src/vindicta_cli/models/__init__.py`
- [ ] T002 Create test directory structure: `tests/__init__.py`, `tests/conftest.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/contract/__init__.py`
- [ ] T003 Update `pyproject.toml` to add new dependencies: `pyyaml>=6.0`, `tenacity>=8.0`; add dev deps: `pytest-mock>=3.12`, `pytest-asyncio>=0.23`
- [ ] T004 [P] Create Typer root app in `src/vindicta_cli/main.py` with `dev` sub-app registration
- [ ] T005 [P] Create `.gitignore` patterns for Python artifacts (`__pycache__/`, `.venv/`, `*.pyc`, `.pytest_cache/`, `.vindicta/`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational

- [ ] T006 [P] Write unit tests for WorkspaceConfig model in `tests/unit/test_workspace_config.py` (serialization, defaults, validation)
- [ ] T007 [P] Write unit tests for RepoEntry model in `tests/unit/test_repo_entry.py` (tier validation, type validation)
- [ ] T008 [P] Write unit tests for RepoInfo model in `tests/unit/test_repo_info.py` (git state properties)
- [ ] T009 [P] Write unit tests for logger in `tests/unit/test_logger.py` (JSON format, rotation, console output)
- [ ] T010 [P] Write unit tests for retry logic in `tests/unit/test_retry.py` (backoff timing, max attempts, logging)
- [ ] T011 [P] Write unit tests for MCP client in `tests/unit/test_mcp_client.py` (availability detection, fallback)
- [ ] T012 [P] Write unit tests for GH client in `tests/unit/test_gh_client.py` (auth check, command construction, JSON parsing)

### Implementation for Foundational

- [ ] T013 [P] Implement WorkspaceConfig dataclass in `src/vindicta_cli/models/workspace_config.py` (schema_version, sync/validation/setup preferences, YAML serialization)
- [ ] T014 [P] Implement RepoEntry dataclass in `src/vindicta_cli/models/repo_info.py` (name, tier, repo_type, github_url, local_path, present flag)
- [ ] T015 [P] Implement RepoInfo dataclass in `src/vindicta_cli/models/repo_info.py` (git state fields, CI status, PR count)
- [ ] T016 [P] Implement ValidationResult and ValidationCheck dataclasses in `src/vindicta_cli/models/validation_result.py` (checks list, compliance_score property)
- [ ] T017 [P] Implement HealthStatus and RepoHealthSummary dataclasses in `src/vindicta_cli/models/health_status.py` (tier_summary, healthy/issue counts)
- [ ] T018 Implement structured JSON logger with rotation in `src/vindicta_cli/lib/logger.py` (JSON formatter, `.vindicta/logs/`, 30d/100MB rotation, Rich console handler)
- [ ] T019 Implement retry decorator config in `src/vindicta_cli/lib/retry.py` (tenacity exponential backoff: 3 attempts, 1s/2s/4s delays, attempt logging via FR-033)
- [ ] T020 Implement MCP filesystem client in `src/vindicta_cli/lib/mcp_client.py` (availability detection, read/write/list/create_directory, fallback to pathlib/shutil)
- [ ] T021 Implement GitHub CLI wrapper in `src/vindicta_cli/lib/gh_client.py` (auth check via `gh auth status`, repo clone, PR list, CI status query, JSON parsing)
- [ ] T022 Implement repository registry in `src/vindicta_cli/lib/registry.py` (hardcoded 26-repo list with tiers, tier filtering, name filtering)
- [ ] T023 Implement workspace service in `src/vindicta_cli/lib/workspace.py` (discover workspace root, load/save `.vindicta-workspace.yml`, merge registry with config)

**Checkpoint**: Foundation ready — all models, logger, retry, MCP client, GH client, registry, and workspace service are operational. User story implementation can now begin.

---

## Phase 3: User Story 1 — New Developer Onboarding (Priority: P1) 🎯 MVP

**Goal**: Allow a new developer to initialize their workspace with all 26 repositories, install dependencies, and configure tooling in under 10 minutes.

**Independent Test**: Run `vindicta dev init` on a clean directory → verify repos cloned, then `vindicta dev setup` → verify deps installed and hooks configured, then `vindicta dev doctor` → verify health is "ready".

### Tests for User Story 1

- [ ] T024 [P] [US1] Write unit tests for init logic in `tests/unit/test_init_workflow.py` (repo cloning, tier filtering, partial failure handling)
- [ ] T025 [P] [US1] Write unit tests for setup logic in `tests/unit/test_setup_service.py` (Python venv, Node deps, pre-commit hooks)
- [ ] T026 [P] [US1] Write unit tests for doctor logic in `tests/unit/test_doctor_service.py` (tool detection, version checks, auto-fix)
- [ ] T027 [US1] Write integration test for full init→setup→doctor workflow in `tests/integration/test_init_workflow.py`

### Implementation for User Story 1

- [ ] T028 [US1] Implement init service logic in `src/vindicta_cli/lib/repository.py` (clone repo via `gh`, detect repo type, report progress)
- [ ] T029 [US1] Implement setup service in `src/vindicta_cli/lib/setup_service.py` (create venv, install Python deps via `uv`, install Node deps via `npm`, install pre-commit hooks)
- [ ] T030 [US1] Implement doctor service in `src/vindicta_cli/lib/doctor_service.py` (check git, gh, python, uv, node versions; workspace config validation; auto-fix recommendations)
- [ ] T031 [US1] Implement `vindicta dev init` CLI command in `src/vindicta_cli/cli/dev/init_cmd.py` (--tier, --repo, --workspace, --skip-setup flags; Rich progress bars; --json output)
- [ ] T032 [US1] Implement `vindicta dev setup` CLI command in `src/vindicta_cli/cli/dev/setup_cmd.py` (--repo, --skip-hooks, --skip-venv, --skip-node flags)
- [ ] T033 [US1] Implement `vindicta dev doctor` CLI command in `src/vindicta_cli/cli/dev/doctor_cmd.py` (--fix flag; Rich table output; exit codes)
- [ ] T034 [US1] Write CLI contract test for init/setup/doctor in `tests/contract/test_cli_contract.py` (exit codes, --json schema, --help output)

**Checkpoint**: User Story 1 fully functional — new developer can init, setup, and doctor their workspace.

---

## Phase 4: User Story 2 — Daily Workspace Synchronization (Priority: P1)

**Goal**: Allow developers to synchronize all local repositories with remote changes, with parallel fetch and configurable auto-pull.

**Independent Test**: Create test commits on remote, run `vindicta dev sync` → verify repos fetched and ahead/behind reported. Test with dirty repo → verify skip with warning.

### Tests for User Story 2

- [ ] T035 [P] [US2] Write unit tests for sync service in `tests/unit/test_sync_service.py` (parallel fetch, dirty skip, auto-pull, timeout, force flag)
- [ ] T036 [US2] Write integration test for sync workflow in `tests/integration/test_sync_workflow.py`

### Implementation for User Story 2

- [ ] T037 [US2] Implement sync service in `src/vindicta_cli/lib/sync_service.py` (asyncio.gather with Semaphore, fetch/pull per repo, dirty detection, ahead/behind counting, timeout handling)
- [ ] T038 [US2] Implement `vindicta dev sync` CLI command in `src/vindicta_cli/cli/dev/sync_cmd.py` (--pull, --parallel, --tier, --force flags; Rich progress; summary table)

**Checkpoint**: User Story 2 functional — daily sync workflow complete.

---

## Phase 5: User Story 3 — Pre-Commit Validation (Priority: P1)

**Goal**: Validate Platform Constitution compliance across all repositories with auto-fix support.

**Independent Test**: Introduce violations (missing constitution, broken links, failing hooks) → run `vindicta dev validate` → verify detection and reporting. Run with `--fix` → verify auto-remediation.

### Tests for User Story 3

- [ ] T039 [P] [US3] Write unit tests for validate service in `tests/unit/test_validate_service.py` (constitution check, context artifacts, link validation, hooks, auto-fix, compliance score)
- [ ] T040 [US3] Write integration test for validation workflow in `tests/integration/test_validate_workflow.py`

### Implementation for User Story 3

- [ ] T041 [US3] Implement validate service in `src/vindicta_cli/lib/validate_service.py` (constitution presence check, .antigravity/ context check, markdown link validation, pre-commit hook execution, auto-fix logic, compliance score calculation)
- [ ] T042 [US3] Implement `vindicta dev validate` CLI command in `src/vindicta_cli/cli/dev/validate_cmd.py` (--repo, --fix, --check flags; per-repo results table; compliance score; exit codes)

**Checkpoint**: User Story 3 functional — pre-commit validation workflow complete.

---

## Phase 6: User Story 4 — Workspace Health Monitoring (Priority: P2)

**Goal**: Display a tier-grouped health dashboard with git status, CI status, and PR counts for all repositories.

**Independent Test**: Create repos in various states → run `vindicta dev status` → verify dashboard accuracy. Test `--failing` filter and `--json` output.

### Tests for User Story 4

- [ ] T043 [P] [US4] Write unit tests for status dashboard in `tests/unit/test_status_dashboard.py` (tier grouping, health indicators, CI status, filtering, JSON output)

### Implementation for User Story 4

- [ ] T044 [US4] Implement status dashboard logic in `src/vindicta_cli/lib/workspace.py` (extend with health assessment, CI query via gh_client, tier grouping, HealthStatus assembly)
- [ ] T045 [US4] Implement `vindicta dev status` CLI command in `src/vindicta_cli/cli/dev/status_cmd.py` (--tier, --failing, --ci, --detailed flags; Rich table/panel dashboard; --json output)

**Checkpoint**: User Story 4 functional — workspace health monitoring complete.

---

## Phase 7: User Story 5 — Environment Troubleshooting (Priority: P2)

**Goal**: Provide a diagnostic command that checks tool versions, workspace configuration, and recommends fixes.

**Independent Test**: Remove required tools or use wrong versions → run `vindicta dev doctor` → verify detection and remediation guidance.

> Note: The `doctor` command was implemented in Phase 3 (US1). This phase extends it with advanced diagnostics.

### Implementation for User Story 5

- [ ] T046 [US5] Extend doctor service in `src/vindicta_cli/lib/doctor_service.py` with advanced diagnostics: workspace config corruption detection, pre-commit hook health check, stale lock file detection, environment variable validation
- [ ] T047 [US5] Write unit tests for advanced doctor diagnostics in `tests/unit/test_doctor_service.py` (append to existing tests: config corruption, hook health, auto-fix scenarios)

**Checkpoint**: User Story 5 functional — advanced diagnostics complement the basic doctor from US1.

---

## Phase 8: User Story 6 — Selective Repository Setup (Priority: P3)

**Goal**: Allow developers to set up only specific repositories or tier subsets instead of the full workspace.

**Independent Test**: Run `vindicta dev init --tier P0 --tier P1` → verify only 7 core repos cloned. Add repos to existing workspace → verify incremental setup.

> Note: Tier/repo filtering was implemented in US1 (T031). This phase ensures incremental addition to existing workspaces.

### Implementation for User Story 6

- [ ] T048 [US6] Extend workspace service in `src/vindicta_cli/lib/workspace.py` with incremental repo addition logic (detect existing workspace, add new repos without re-cloning existing)
- [ ] T049 [US6] Write unit tests for incremental workspace setup in `tests/unit/test_workspace.py` (partial workspace detection, additive cloning, config merge)

**Checkpoint**: User Story 6 functional — selective setup and incremental addition work correctly.

---

## Phase 9: User Story 7 — Build Artifact Cleanup (Priority: P3)

**Goal**: Clean build artifacts across all repositories and report disk space reclaimed.

**Independent Test**: Build projects to generate artifacts → run `vindicta dev clean --dry-run` → verify identification. Run `vindicta dev clean` → verify removal and disk report.

### Tests for User Story 7

- [ ] T050 [P] [US7] Write unit tests for clean service in `tests/unit/test_clean_service.py` (Python artifacts, Node artifacts, dry-run, disk space accounting)

### Implementation for User Story 7

- [ ] T051 [US7] Implement clean service in `src/vindicta_cli/lib/clean_service.py` (scan for __pycache__, .pytest_cache, .venv, node_modules, dist, .next; calculate sizes; delete with safety checks; summary report)
- [ ] T052 [US7] Implement `vindicta dev clean` CLI command in `src/vindicta_cli/cli/dev/clean_cmd.py` (--dry-run, --type, --repo flags; per-repo cleanup table; total reclaimed)

**Checkpoint**: User Story 7 functional — artifact cleanup with disk accounting works.

---

## Phase 10: User Story 8 — Workspace Configuration Management (Priority: P3)

**Goal**: Allow developers to customize workspace behavior via persistent configuration.

**Independent Test**: Set config values → verify persistence across invocations. Run `vindicta dev config list` → verify display. Reset → verify defaults restored.

### Tests for User Story 8

- [ ] T053 [P] [US8] Write unit tests for config service in `tests/unit/test_config_service.py` (get, set, list, reset, validation, persistence)

### Implementation for User Story 8

- [ ] T054 [US8] Implement config service in `src/vindicta_cli/lib/config_service.py` (get/set/list/reset operations, key validation, value type coercion, persistence via workspace.py)
- [ ] T055 [US8] Implement `vindicta dev config` CLI command group in `src/vindicta_cli/cli/dev/config_cmd.py` (get/set/list/reset subcommands; Rich table for list; error handling for invalid keys)

**Checkpoint**: User Story 8 functional — configuration management complete.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories

- [ ] T056 [P] Update `docs/commands.md` with full `dev` command reference
- [ ] T057 [P] Update `README.md` with dev commands quickstart section
- [ ] T058 [P] Update `CHANGELOG.md` with 0.2.0 release notes for dev commands
- [ ] T059 Code-wide review: ensure all Rich console output respects `--json` flag (suppress Rich when JSON mode active)
- [ ] T060 Code-wide review: ensure all commands respect `--verbose` flag (stream subprocess output when verbose)
- [ ] T061 Run `ruff check` and `ruff format` across all source files
- [ ] T062 Run full test suite: `pytest tests/ -v --tb=short` and verify >80% coverage
- [ ] T063 Run quickstart.md validation: execute each workflow example and verify expected output

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3–10)**: All depend on Foundational phase completion
  - US1 (P1): Independent — MVP target
  - US2 (P1): Independent of US1 (uses workspace.py, registry.py from foundation)
  - US3 (P1): Independent of US1/US2
  - US4 (P2): Independent (uses gh_client from foundation)
  - US5 (P2): Extends US1's doctor command (depends on T030)
  - US6 (P3): Extends US1's init logic (depends on T028, T031)
  - US7 (P3): Independent
  - US8 (P3): Independent (uses workspace.py from foundation)
- **Polish (Phase 11)**: Depends on all user stories being complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD Red phase)
- Models before services
- Services before CLI commands
- CLI commands before contract tests

### Parallel Opportunities

- All Setup T004–T005 can run in parallel
- All Foundation test tasks T006–T012 can run in parallel
- All Foundation model tasks T013–T017 can run in parallel
- Foundation service tasks T018–T023 are mostly parallel (T023 depends on T013, T022)
- US1 test tasks T024–T026 can run in parallel
- US1/US2/US3 can run in parallel after Foundation (if team capacity allows)
- US7/US8 are fully independent and can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: T024 "Unit tests for init logic in tests/unit/test_init_workflow.py"
Task: T025 "Unit tests for setup logic in tests/unit/test_setup_service.py"
Task: T026 "Unit tests for doctor logic in tests/unit/test_doctor_service.py"

# Launch all implementations (after tests confirmed failing):
Task: T028 "Init service logic in src/vindicta_cli/lib/repository.py"
Task: T029 "Setup service in src/vindicta_cli/lib/setup_service.py"
Task: T030 "Doctor service in src/vindicta_cli/lib/doctor_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (init + setup + doctor)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (init/setup/doctor) → Test independently → MVP!
3. US2 (sync) → Test independently → Daily workflow enabled
4. US3 (validate) → Test independently → Compliance enforcement
5. US4 (status) → Test independently → Health monitoring
6. US5 (doctor+) → Test independently → Advanced diagnostics
7. US6 (selective init) → Test independently → Power user feature
8. US7 (clean) → Test independently → Maintenance workflow
9. US8 (config) → Test independently → Customization
10. Polish → Final validation → Release 0.2.0

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests MUST fail before implementing (Constitution Principle III)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: 63
