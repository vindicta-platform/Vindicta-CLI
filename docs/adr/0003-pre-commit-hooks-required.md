# Pre-commit Hooks Required

* Status: accepted
* Date: 2026-02-01

## Context and Problem Statement

We need a consistent code quality enforcement mechanism across the repository.

## Decision Outcome

All repositories MUST configure **pre-commit** hooks with ruff.

## Consequences

### Positive

- `.pre-commit-config.yaml` required in every repository
- Developers run `pre-commit install` on setup
- Consistent formatting and linting enforced automatically

### Negative

- Adds a setup step for new contributors
