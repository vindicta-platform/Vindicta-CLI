# Contributing to Vindicta-CLI

Thank you for contributing to Vindicta-CLI! All contributions **must** follow the [Platform Constitution](https://github.com/vindicta-platform/.specify/blob/main/memory/constitution.md).

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — package & virtualenv manager
- **[pre-commit](https://pre-commit.com/)** — git hook framework
- **Git** configured with your GitHub account

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI

# 2. Create a virtual environment and install dev dependencies
uv venv
uv pip install -e ".[dev]"

# 3. ⚠️ MANDATORY — Install pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push

# 4. Verify your setup
pre-commit run --all-files
pytest tests/ -v
```

> [!IMPORTANT]
> **Steps 3 is non-negotiable.** Pre-commit hooks enforce linting (ruff), formatting (ruff-format), trailing whitespace removal, end-of-file fixing, and YAML validation. Skipping this step means your commits will fail CI.

## Pre-Commit Hooks

The `.pre-commit-config.yaml` enforces the following on every commit:

| Hook                  | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| `ruff`                | Lint Python code (E, F, I, W rules) with auto-fix |
| `ruff-format`         | Format Python code (88-char line length)          |
| `trailing-whitespace` | Remove trailing whitespace                        |
| `end-of-file-fixer`   | Ensure files end with a newline                   |
| `check-yaml`          | Validate YAML syntax                              |

To run hooks manually against all files:

```bash
pre-commit run --all-files
```

To update hooks to their latest versions:

```bash
pre-commit autoupdate
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feat/<ID>-<short-name>
# Example: git checkout -b feat/042-credit-ledger
```

### 2. Follow the SDD Lifecycle

Every feature must go through Spec-Driven Development:

1. **Specify** — Create spec in `specs/<ID>-<name>/spec.md`
2. **Plan** — Write `plan.md` with architecture and file changes
3. **Tasks** — Generate dependency-ordered `tasks.md`
4. **Implement** — Atomic TDD commits (Red → Green → Refactor)
5. **Verify** — Verification checklist with evidence

### 3. Write Tests First (TDD)

```bash
# Run the full test suite
pytest tests/ -v

# Run a specific test file
pytest tests/unit/test_example.py -v

# Run with coverage
pytest tests/ -v --cov=src/vindicta_cli
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat(<scope>): <description>"
# Pre-commit hooks run automatically here
git push origin feat/<ID>-<short-name>
```

### 5. Open a Pull Request

- Target: `main`
- Reference the SDD spec ID in the PR description
- Include a verification checklist
- All CI checks must pass before merge

## Quality Gates

| Gate                 | Requirement                                     |
| -------------------- | ----------------------------------------------- |
| **Pre-commit hooks** | All hooks pass (ruff, format, whitespace, YAML) |
| **Unit tests**       | 100% pass, >80% coverage on critical paths      |
| **CI pipeline**      | GitHub Actions checks green                     |
| **Code review**      | At least one approval                           |

## Code Style

- **Line length**: 88 characters (configured in `pyproject.toml`)
- **Linter**: ruff with `E, F, I, W` rule sets
- **Target**: Python 3.10+
- **Imports**: Sorted by `isort` (via ruff `I` rules)

## Project Structure

```
Vindicta-CLI/
├── src/vindicta_cli/   # Source code
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── docs/               # Documentation (mkdocs)
├── specs/              # SDD specification bundles
├── .pre-commit-config.yaml
├── pyproject.toml
└── CONTRIBUTING.md     # ← You are here
```

## License

MIT License — See [LICENSE](./LICENSE) for details.
