# Vindicta-CLI

> Unified command-line interface for the Vindicta Platform.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Version 0.2.0](https://img.shields.io/badge/version-0.2.0-orange)

## Overview
Vindicta-CLI is a [Typer](https://typer.tiangolo.com/)-based CLI that provides developer workspace management for the 26-repo Vindicta Platform. It handles repository cloning, synchronisation, health checks, validation, and configuration — all with [Rich](https://rich.readthedocs.io/) terminal output and optional `--json` machine-readable output.

## Installation
```bash
# From source (recommended during WIP)
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI
uv venv
uv pip install -e ".[dev]"
```

```bash
# From Git directly
uv pip install git+https://github.com/vindicta-platform/Vindicta-CLI.git
```

## Quick Start
```bash
# Initialize a workspace with all platform repos
vindicta dev init -w ~/vindicta-workspace

# Check workspace health
vindicta dev status

# Synchronize repos with remote
vindicta dev sync --pull

# Diagnose environment issues
vindicta dev doctor
```

## Commands
All commands live under the `vindicta dev` namespace.

| Command                     | Description                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------- |
| `vindicta dev init`         | Initialize workspace by cloning platform repositories (with tier/repo filtering)       |
| `vindicta dev sync`         | Synchronize all workspace repositories with remote (fetch, optional pull, parallelism) |
| `vindicta dev setup`        | Install dependencies for workspace repositories (venvs, npm, hooks)                    |
| `vindicta dev status`       | Display workspace health — branch, dirty state, ahead/behind counts                    |
| `vindicta dev validate`     | Run constitution-compliance validation across repositories                             |
| `vindicta dev doctor`       | Diagnose the development environment (Python, uv, Git, pre-commit, etc.)               |
| `vindicta dev clean`        | Remove build artifacts, caches, and temporary files from workspace repos               |
| `vindicta dev config get`   | Get a workspace configuration value                                                    |
| `vindicta dev config set`   | Set a workspace configuration value                                                    |
| `vindicta dev config list`  | List all configuration values                                                          |
| `vindicta dev config reset` | Reset configuration to defaults                                                        |

> Every command supports `--json` for machine-readable output and `--verbose` / `-v` for detailed logging.

## Project Structure
```
Vindicta-CLI/
├── src/vindicta_cli/
│   ├── main.py                 # Root Typer app — registers all sub-apps
│   ├── cli/
│   │   └── dev/                # Developer workspace commands
│   │       ├── init_cmd.py     # vindicta dev init
│   │       ├── sync_cmd.py     # vindicta dev sync
│   │       ├── setup_cmd.py    # vindicta dev setup
│   │       ├── status_cmd.py   # vindicta dev status
│   │       ├── validate_cmd.py # vindicta dev validate
│   │       ├── doctor_cmd.py   # vindicta dev doctor
│   │       ├── clean_cmd.py    # vindicta dev clean
│   │       └── config_cmd.py   # vindicta dev config (sub-app)
│   ├── lib/                    # Shared services & utilities
│   │   ├── clean_service.py    # Artifact/cache removal logic
│   │   ├── config_service.py   # Configuration read/write/reset
│   │   ├── doctor_service.py   # Environment diagnostic checks
│   │   ├── gh_client.py        # GitHub API wrapper
│   │   ├── logger.py           # Structured logging setup
│   │   ├── mcp_client.py       # MCP server integration
│   │   ├── registry.py         # Platform repository registry (26 repos)
│   │   ├── repository.py       # Git clone/pull operations
│   │   ├── retry.py            # Tenacity retry helpers
│   │   ├── setup_service.py    # Dependency installation logic
│   │   ├── sync_service.py     # Fetch/pull synchronization
│   │   ├── validate_service.py # Constitution compliance checks
│   │   └── workspace.py        # Workspace discovery & config I/O
│   └── models/                 # Data models
│       ├── health_status.py    # Health check result model
│       ├── repo_info.py        # Repository metadata model
│       ├── validation_result.py# Validation outcome model
│       └── workspace_config.py # Workspace config schema
├── tests/
│   ├── unit/                   # Unit tests (pytest)
│   ├── integration/            # Integration tests
│   └── contract/               # Contract tests
├── docs/                       # MkDocs documentation site
│   ├── SETUP.md
│   ├── commands.md
│   ├── contributing.md
│   ├── adr/                    # Architecture Decision Records
│   └── proposals/
├── pyproject.toml              # Build config (hatchling), deps, tool settings
├── mkdocs.yml                  # Documentation site configuration
├── .pre-commit-config.yaml     # Pre-commit hook definitions
├── CONTRIBUTING.md             # Contribution guide & quality gates
├── CHANGELOG.md                # Release history
├── ROADMAP.md                  # Feature roadmap
└── LICENSE                     # MIT
```

## Development
```bash
# Clone & install
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI
uv venv
uv pip install -e ".[dev]"

# ⚠️ Required — install pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push

# Run the test suite
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/vindicta_cli

# Lint & format
ruff check src/ tests/
ruff format src/ tests/
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full development workflow, SDD lifecycle, and quality gates.
See [docs/SETUP.md](./docs/SETUP.md) for detailed setup and shell completion instructions.

## Tech Stack
| Component        | Choice        | Notes                             |
| ---------------- | ------------- | --------------------------------- |
| CLI framework    | Typer ≥0.12   | Declarative, type-hinted CLI      |
| Terminal output  | Rich ≥13.0    | Tables, spinners, colour output   |
| Config format    | PyYAML ≥6.0   | Workspace config persistence      |
| Retry logic      | Tenacity ≥8.0 | Retry on transient network errors |
| Build system     | Hatchling     | PEP 517 build backend             |
| Linter/Formatter | Ruff ≥0.4     | Fast lint + format (E, F, I, W)   |
| Type checker     | mypy ≥1.10    | Static type analysis              |
| Testing          | pytest ≥8.0   | Unit, integration, contract       |

## Platform Documentation

> **📌 Important:** All cross-cutting decisions, feature proposals, and platform-wide architecture documentation live in [**Platform-Docs**](https://github.com/vindicta-platform/Platform-Docs).
>
> Any decision affecting multiple repos **must** be recorded there before implementation.

- 📋 [Feature Proposals](https://github.com/vindicta-platform/Platform-Docs/tree/main/docs/proposals)
- 🏗️ [Architecture Decisions](https://github.com/vindicta-platform/Platform-Docs/tree/main/docs)
- 📖 [Contributing Guide](https://github.com/vindicta-platform/Platform-Docs/blob/main/CONTRIBUTING.md)

## License
MIT License — See [LICENSE](./LICENSE) for details.
