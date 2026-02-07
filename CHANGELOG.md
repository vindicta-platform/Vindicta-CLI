# Changelog

## [0.2.0] - 2026-02-07

### Added
- **Developer Commands** (`vindicta dev`): 8 workspace management commands
  - `init`: Clone platform repositories with tier/repo filtering and parallel operations
  - `sync`: Synchronize repos with remote (fetch, pull, dirty detection, force mode)
  - `setup`: Install Python venvs, Node deps, and pre-commit hooks per repo
  - `status`: Tier-grouped health dashboard with branch/dirty/ahead-behind tracking
  - `validate`: Platform Constitution compliance checks with auto-fix support
  - `doctor`: Environment diagnostics for git, gh, python, uv, node, and workspace config
  - `clean`: Artifact/cache removal with dry-run and disk space reporting
  - `config`: Workspace configuration management (get/set/list/reset)
- **Core Services**: 9 service modules (`workspace`, `repository`, `sync_service`, `setup_service`, `validate_service`, `doctor_service`, `clean_service`, `config_service`, `registry`)
- **Models**: `WorkspaceConfig`, `RepoEntry`, `RepoInfo`, `ValidationResult`, `HealthStatus`
- **Infrastructure**: Structured JSON logging, tenacity retry with exponential backoff, MCP filesystem client with pathlib fallback, GitHub CLI wrapper
- **Testing**: 164 tests (unit, integration, contract) with 100% pass rate
- **Dependencies**: Added `pyyaml>=6.0`, `tenacity>=8.0`, `pytest-mock>=3.12`, `pytest-asyncio>=0.23`

## [0.1.0] - 2026-02-01
- Initial repository creation
