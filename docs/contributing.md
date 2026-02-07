# Contributing

Welcome to Vindicta-CLI! Before writing any code, please read the full [CONTRIBUTING.md](https://github.com/vindicta-platform/Vindicta-CLI/blob/main/CONTRIBUTING.md) guide.

## Quick Start

```bash
# Clone and install
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI
uv venv
uv pip install -e ".[dev]"

# ⚠️ MANDATORY — Install pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push

# Verify
pre-commit run --all-files
pytest tests/ -v
```

!!! warning "Pre-commit is required"
    Every contributor **must** run `pre-commit install` after cloning.
    Commits that skip pre-commit will be rejected by CI.

## Pre-Commit Hooks

The `.pre-commit-config.yaml` runs the following automatically on every commit:

| Hook                  | Purpose                            |
| --------------------- | ---------------------------------- |
| `ruff`                | Lint Python code with auto-fix     |
| `ruff-format`         | Format Python code (88-char lines) |
| `trailing-whitespace` | Remove trailing whitespace         |
| `end-of-file-fixer`   | Ensure files end with a newline    |
| `check-yaml`          | Validate YAML syntax               |

Run hooks manually:

```bash
pre-commit run --all-files
```

## Development Workflow

All contributions follow the **Spec-Driven Development** lifecycle defined in the [Platform Constitution](https://github.com/vindicta-platform/.specify/blob/main/memory/constitution.md):

1. **Specify** — User stories and acceptance criteria in `.specify/specs/`
2. **Plan** — Architecture and file changes in `plan.md`
3. **Tasks** — Dependency-ordered task list in `tasks.md`
4. **Implement** — Atomic TDD commits (Red → Green → Refactor)
5. **Verify** — Checklist with evidence

## Quality Gates

| Gate             | Requirement              |
| ---------------- | ------------------------ |
| Pre-commit hooks | All hooks pass           |
| Unit tests       | 100% pass, >80% coverage |
| CI pipeline      | GitHub Actions green     |
| Code review      | At least one approval    |

## Branch Naming

- Feature: `feat/<ID>-<short-name>`
- Bugfix: `fix/<ID>-<short-name>`
- Target: always `main`

## Running Tests

```bash
pytest tests/ -v                              # Full suite
pytest tests/unit/test_example.py -v          # Single file
pytest tests/ -v --cov=src/vindicta_cli       # With coverage
```

## License

MIT License
