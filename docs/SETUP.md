# Setup Guide

## Prerequisites

| Tool                                  | Version | Purpose                      |
| ------------------------------------- | ------- | ---------------------------- |
| Python                                | 3.10+   | Runtime                      |
| [uv](https://docs.astral.sh/uv/)      | Latest  | Package & virtualenv manager |
| [pre-commit](https://pre-commit.com/) | 3.7+    | Git hook framework           |
| Git                                   | Latest  | Version control              |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI

# 2. Create virtualenv and install dependencies
uv venv
uv pip install -e ".[dev]"

# 3. ⚠️ MANDATORY — Install pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push
```

!!! warning "Do not skip step 3"
    Pre-commit hooks enforce formatting, linting, and validation on every commit.
    This is a **mandatory** part of the development setup per the Platform Constitution.

## Verify Your Setup

```bash
# Confirm pre-commit hooks are active
pre-commit run --all-files

# Confirm tests pass
pytest tests/ -v

# Confirm the CLI is installed
vindicta --version
```

## Shell Completion

```bash
# Bash
vindicta --install-completion bash

# Zsh
vindicta --install-completion zsh

# PowerShell
vindicta --install-completion powershell
```

## What's Next?

See the [Contributing Guide](contributing.md) for the full development workflow.
