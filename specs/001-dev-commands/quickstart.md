# Quickstart: Developer Commands for Platform Management

**Feature**: 001-dev-commands
**Date**: 2026-02-07

## Prerequisites

- **Python** >= 3.10 (`python --version`)
- **Git** >= 2.30 (`git --version`)
- **GitHub CLI** >= 2.0 (`gh --version`), authenticated (`gh auth status`)
- **uv** (recommended for package management: `pip install uv`)
- **Node.js** >= 18.0 (for JavaScript repositories)

## Installation

```bash
# Clone CLI repo
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI

# Install in development mode
uv pip install -e ".[dev]"

# Verify installation
vindicta --help
```

## First-Time Setup (New Developer)

```bash
# 1. Initialize workspace (clones all 26 repos)
vindicta dev init --workspace ~/vindicta-platform

# 2. Install dependencies and hooks
vindicta dev setup

# 3. Verify environment
vindicta dev doctor

# 4. Check workspace status
vindicta dev status
```

**Expected time**: ~10 minutes for full initialization.

## Core Workflows

### Morning Sync

```bash
# Fetch + show ahead/behind for all repos
vindicta dev sync

# Fetch + auto-pull clean repos
vindicta dev sync --pull
```

### Before Creating a PR

```bash
# Validate constitution compliance
vindicta dev validate

# Auto-fix what's possible
vindicta dev validate --fix
```

### Weekly Maintenance

```bash
# Check workspace health with CI status
vindicta dev status --ci --detailed

# Clean build artifacts
vindicta dev clean --dry-run   # Preview first
vindicta dev clean             # Execute cleanup
```

### Selective Setup

```bash
# Initialize only core repos (P0 + P1)
vindicta dev init --tier P0 --tier P1

# Setup specific repos
vindicta dev setup --repo Vindicta-Core --repo Vindicta-API
```

## Configuration

```bash
# Increase parallel sync for faster operations
vindicta dev config set parallel_count 8

# Enable auto-fix by default
vindicta dev config set auto_fix true

# View all settings
vindicta dev config list
```

## Troubleshooting

```bash
# Run diagnostics
vindicta dev doctor

# Auto-fix common issues
vindicta dev doctor --fix

# Verbose mode for debugging
vindicta dev sync --verbose
```

## JSON Output (for scripting)

```bash
# Get JSON status for external processing
vindicta dev status --json | jq '.repos[] | select(.git_healthy == false)'

# JSON validation results
vindicta dev validate --json > validation-report.json
```
