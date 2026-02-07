# Feature Specification: Developer Commands for Platform Management

**Feature Branch**: `001-dev-commands`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "Developer commands for Vindicta Platform workspace management including init, sync, setup, status, validate, doctor, clean, and config operations"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New Developer Onboarding (Priority: P1)

A new developer joins the Vindicta Platform team and needs to set up their local development environment with all 26 repositories, dependencies, and tooling configured correctly.

**Why this priority**: This is the most critical workflow as it directly impacts developer productivity and time-to-first-contribution. Without this, developers spend hours manually cloning repos and configuring environments.

**Independent Test**: Can be fully tested by running initialization commands on a clean machine and verifying all repositories are cloned, dependencies installed, and pre-commit hooks configured. Delivers immediate value by reducing onboarding time from hours to minutes.

**Acceptance Scenarios**:

1. **Given** a developer has a clean machine with Git and Python installed, **When** they run the initialization command with default settings, **Then** all 26 repositories are cloned to the workspace directory with correct folder structure
2. **Given** repositories are cloned, **When** the setup command completes, **Then** all Python virtual environments are created, Node.js dependencies are installed, and pre-commit hooks are configured
3. **Given** setup is complete, **When** the developer runs the diagnostic command, **Then** all required tools are detected with correct versions and workspace health is reported as "ready"
4. **Given** a developer wants only core repositories, **When** they initialize with tier filtering (P0 and P1 only), **Then** only the 7 core repositories are cloned and configured

---

### User Story 2 - Daily Workspace Synchronization (Priority: P1)

A developer starts their workday and needs to synchronize all local repositories with the latest remote changes across the entire platform.

**Why this priority**: Daily sync is essential for maintaining workspace health and preventing merge conflicts. This is a daily workflow that impacts all developers.

**Independent Test**: Can be tested by creating test commits on remote branches, running sync commands, and verifying local repositories are updated. Delivers value by keeping workspace current with minimal manual effort.

**Acceptance Scenarios**:

1. **Given** multiple repositories have remote updates, **When** the developer runs the sync command, **Then** all repositories fetch latest changes and display ahead/behind status for each repo
2. **Given** a repository has uncommitted local changes, **When** sync runs, **Then** the repository is skipped with a warning message and the developer is notified of dirty state
3. **Given** all repositories are clean, **When** sync runs with auto-pull enabled, **Then** all repositories are updated to latest remote state and summary shows successful sync count
4. **Given** sync completes, **When** the developer views status, **Then** workspace health dashboard shows current branch, commit status, and any issues requiring attention

---

### User Story 3 - Pre-Commit Validation (Priority: P1)

A developer has made changes across multiple repositories and needs to validate that all changes comply with Platform Constitution requirements before creating pull requests.

**Why this priority**: Constitutional compliance is mandatory per Platform Constitution v1.0.0. This prevents CI failures and ensures quality gates are met before code review.

**Independent Test**: Can be tested by introducing violations (missing constitution files, broken markdown links, failing pre-commit hooks) and verifying validation detects and reports them. Delivers value by catching issues locally before PR creation.

**Acceptance Scenarios**:

1. **Given** a repository is missing Platform Constitution file, **When** validation runs, **Then** the issue is detected and reported with specific file path and remediation steps
2. **Given** markdown files contain broken links, **When** link validation runs, **Then** all broken links are identified with file locations and line numbers
3. **Given** pre-commit hooks would fail, **When** validation runs with auto-fix enabled, **Then** fixable issues are automatically corrected and remaining issues are reported
4. **Given** all validation checks pass, **When** validation completes, **Then** compliance score is reported as 100% and developer receives confirmation to proceed with PR creation

---

### User Story 4 - Workspace Health Monitoring (Priority: P2)

A developer needs to quickly assess the health of their entire workspace to identify repositories with issues, pending PRs, or failing CI checks.

**Why this priority**: Proactive health monitoring prevents issues from accumulating and helps developers maintain workspace hygiene. This is a periodic workflow (weekly/bi-weekly) rather than daily.

**Independent Test**: Can be tested by creating various repository states (dirty, ahead/behind, failing CI) and verifying status dashboard accurately reports all conditions. Delivers value by providing at-a-glance workspace overview.

**Acceptance Scenarios**:

1. **Given** workspace contains 26 repositories in various states, **When** status command runs, **Then** dashboard displays tier-grouped summary with health indicators for each repository
2. **Given** some repositories have failing CI checks, **When** status runs with detailed mode, **Then** CI status is queried and failures are highlighted with links to build logs
3. **Given** developer wants to focus on issues, **When** status runs with failing-only filter, **Then** only repositories with problems are displayed with specific issue details
4. **Given** status data is needed for reporting, **When** status runs with JSON output, **Then** structured data is exported with all repository metrics for external processing

---

### User Story 5 - Environment Troubleshooting (Priority: P2)

A developer encounters issues with their local environment (missing tools, version mismatches, configuration problems) and needs diagnostic assistance.

**Why this priority**: Environment issues are common but not daily occurrences. Quick diagnosis reduces debugging time and helps developers self-service common problems.

**Independent Test**: Can be tested by removing required tools or using incorrect versions, then verifying diagnostics detect issues and provide remediation guidance. Delivers value by reducing support escalations.

**Acceptance Scenarios**:

1. **Given** required tools are missing or outdated, **When** diagnostic command runs, **Then** all tool versions are checked against requirements and missing/outdated tools are reported
2. **Given** workspace configuration is corrupted, **When** diagnostics run, **Then** configuration issues are identified and repair recommendations are provided
3. **Given** common issues are detected, **When** diagnostics run with auto-fix enabled, **Then** fixable problems are automatically resolved and summary of actions is displayed
4. **Given** diagnostics complete, **When** results are displayed, **Then** developer receives prioritized recommendations with specific commands to resolve each issue

---

### User Story 6 - Selective Repository Setup (Priority: P3)

A developer working on a specific feature needs to set up only relevant repositories rather than the entire 26-repository workspace.

**Why this priority**: Useful for focused work but not essential for general development. Most developers work across multiple repositories so full workspace is preferred.

**Independent Test**: Can be tested by initializing workspace with specific repository list and verifying only those repositories are cloned and configured. Delivers value for specialized workflows.

**Acceptance Scenarios**:

1. **Given** developer specifies repository names, **When** initialization runs, **Then** only specified repositories are cloned and configured
2. **Given** developer specifies tier level, **When** initialization runs, **Then** all repositories in specified tier are set up with correct dependencies
3. **Given** partial workspace exists, **When** setup runs for additional repositories, **Then** new repositories are added to existing workspace configuration
4. **Given** selective setup completes, **When** status runs, **Then** workspace configuration reflects partial setup and indicates which repositories are present

---

### User Story 7 - Build Artifact Cleanup (Priority: P3)

A developer needs to reclaim disk space by cleaning build artifacts, caches, and temporary files across all repositories.

**Why this priority**: Disk space management is periodic maintenance, not a daily workflow. Useful but not critical for core development tasks.

**Independent Test**: Can be tested by building projects to generate artifacts, running cleanup, and verifying artifacts are removed while source code remains intact. Delivers value by freeing disk space.

**Acceptance Scenarios**:

1. **Given** repositories contain build artifacts, **When** cleanup runs with dry-run mode, **Then** all cleanable files are identified and total disk space to be reclaimed is reported
2. **Given** cleanup targets Python artifacts, **When** cleanup runs, **Then** `__pycache__`, `.pytest_cache`, and `.venv` directories are removed from all Python repositories
3. **Given** cleanup targets Node.js artifacts, **When** cleanup runs, **Then** `node_modules`, `dist`, and `.next` directories are removed from all JavaScript repositories
4. **Given** cleanup completes, **When** summary is displayed, **Then** total disk space reclaimed is reported with breakdown by repository and artifact type

---

### User Story 8 - Workspace Configuration Management (Priority: P3)

A developer needs to customize workspace behavior (parallel sync operations, auto-fix preferences, default tiers) to match their workflow preferences.

**Why this priority**: Configuration customization improves developer experience but has reasonable defaults. Most developers use default settings.

**Independent Test**: Can be tested by setting various configuration values and verifying they persist across command invocations. Delivers value by enabling workflow optimization.

**Acceptance Scenarios**:

1. **Given** developer wants faster sync, **When** they increase parallel sync setting to 8, **Then** subsequent sync operations process 8 repositories concurrently
2. **Given** developer prefers auto-fix for validation, **When** they enable auto-fix in configuration, **Then** validation commands automatically fix issues without requiring explicit flag
3. **Given** developer works primarily with P0/P1 tiers, **When** they set default tier preference, **Then** initialization commands default to those tiers unless overridden
4. **Given** configuration changes are made, **When** developer views configuration, **Then** all current settings are displayed with descriptions and current values

---

### Edge Cases

- What happens when a repository clone fails due to network issues during initialization?
  - System should continue with remaining repositories, report failures at end, and provide retry command for failed repos
  
- How does system handle repositories with uncommitted changes during sync?
  - System skips pulling for dirty repositories, displays warning, and provides status of uncommitted files
  
- What happens when workspace configuration file is missing or corrupted?
  - System attempts to reconstruct configuration from discovered repositories, warns user, and offers to regenerate configuration
  
- How does system behave when GitHub CLI is not installed or not authenticated?
  - System detects missing `gh` command, reports error with installation instructions, and falls back to git-only operations where possible
  
- What happens when pre-commit hooks fail during validation?
  - System reports specific hook failures with error messages, provides remediation guidance, and exits with non-zero code
  
- How does system handle repositories on non-default branches during sync?
  - System reports current branch for each repository, warns if not on default branch, and skips auto-pull unless explicitly forced
  
- What happens when tier filtering produces empty repository list?
  - System reports no repositories match criteria, displays available tiers, and exits without making changes
  
- How does system handle parallel operations when one repository hangs?
  - System implements timeout for parallel operations, reports hung repositories, and continues with remaining repos

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide initialization command that clones specified repositories from GitHub organization
- **FR-002**: System MUST support tier-based filtering (P0, P1, P2, P3) for repository selection during initialization
- **FR-003**: System MUST create workspace configuration file (`.vindicta-workspace.yml`) containing repository registry and settings
- **FR-004**: System MUST detect repository type (Python, Node.js, or mixed) and install appropriate dependencies
- **FR-005**: System MUST install pre-commit hooks across all repositories during setup
- **FR-006**: System MUST synchronize all repositories with remote state, fetching latest changes and reporting ahead/behind status
- **FR-007**: System MUST skip pulling for repositories with uncommitted changes and report dirty state
- **FR-008**: System MUST support parallel synchronization with configurable concurrency level
- **FR-009**: System MUST display workspace health dashboard showing git status, CI status, and PR counts for each repository
- **FR-010**: System MUST validate Platform Constitution v1.0.0 presence in all repositories
- **FR-011**: System MUST validate `.antigravity/` context artifacts (ARCHITECTURE.md, CONSTRAINTS.md) exist in repositories
- **FR-012**: System MUST validate markdown link integrity across all documentation files
- **FR-013**: System MUST execute pre-commit hooks and report validation failures with specific error messages
- **FR-014**: System MUST support auto-fix mode for validation issues where automated remediation is possible
- **FR-015**: System MUST detect and report versions of required tools (git, gh, python, uv, node)
- **FR-016**: System MUST identify workspace configuration issues and provide remediation recommendations
- **FR-017**: System MUST clean build artifacts (Python: `__pycache__`, `.pytest_cache`, `.venv`; Node.js: `node_modules`, `dist`, `.next`)
- **FR-018**: System MUST report disk space reclaimed during cleanup operations
- **FR-019**: System MUST persist configuration settings in workspace configuration file
- **FR-020**: System MUST support both workspace-local and global configuration scopes
- **FR-021**: System MUST use GitHub CLI (`gh`) internally for repository cloning and PR/CI status queries
- **FR-022**: System MUST NOT duplicate MCP server functionality (file system operations, GitHub API calls)
- **FR-023**: System MUST exit with non-zero code when validation failures or critical errors occur
- **FR-024**: System MUST support JSON output format for programmatic consumption of status and diagnostic data
- **FR-025**: System MUST handle network failures gracefully and provide retry mechanisms for failed operations

### Key Entities

- **Workspace**: Represents the root directory containing all Vindicta Platform repositories. Contains workspace configuration file, repository registry, and settings for sync/validation behavior.

- **Repository**: Individual Git repository within the workspace. Has attributes: name, tier (P0/P1/P2/P3), type (Python/Node.js/mixed), path, git status (branch, ahead/behind, dirty), CI status, and PR count.

- **Workspace Configuration**: Persistent settings stored in `.vindicta-workspace.yml`. Contains repository registry, sync preferences (parallel count, auto-pull), validation preferences (auto-fix, constitution check), and setup preferences (install hooks, create env files).

- **Validation Result**: Outcome of compliance checks. Contains pass/fail status for constitution presence, context artifacts, link integrity, and pre-commit hooks. Includes specific error messages and remediation guidance.

- **Health Status**: Snapshot of workspace health. Contains per-repository metrics (git status, CI status, PR count), aggregate statistics (total repos, healthy count, issue count), and tier-grouped summaries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New developers can initialize complete workspace (all 26 repositories) in under 10 minutes on standard development machine
- **SC-002**: Workspace synchronization completes for all repositories in under 2 minutes with default parallel settings
- **SC-003**: Validation checks identify 100% of Platform Constitution compliance violations with zero false positives
- **SC-004**: Developers can diagnose and resolve 80% of common environment issues using diagnostic command without external support
- **SC-005**: Workspace health status displays current state for all repositories in under 5 seconds
- **SC-006**: Cleanup operations reclaim disk space without removing any source code or configuration files (100% accuracy)
- **SC-007**: 90% of developers successfully complete onboarding workflow on first attempt without manual intervention
- **SC-008**: Validation auto-fix resolves 70% of common compliance issues without manual correction
- **SC-009**: System handles network failures gracefully with automatic retry for at least 3 attempts before reporting failure
- **SC-010**: Configuration changes persist correctly across command invocations with 100% reliability
