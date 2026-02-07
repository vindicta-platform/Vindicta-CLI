# CLI Contract: `vindicta dev` Commands

**Feature**: 001-dev-commands
**Date**: 2026-02-07

## Command Reference

All commands follow the `vindicta dev [command]` pattern.

### Global Flags (available on all `dev` commands)

| Flag               | Type | Default | Description                                                    |
| ------------------ | ---- | ------- | -------------------------------------------------------------- |
| `--json`           | bool | false   | Output structured JSON instead of human-readable text          |
| `--verbose` / `-v` | bool | false   | Stream real-time command output instead of progress indicators |
| `--help`           | bool | —       | Show command help                                              |

---

### `vindicta dev init`

**Purpose**: Initialize workspace by cloning repositories from GitHub organization.

```bash
vindicta dev init [OPTIONS]
```

| Option               | Type        | Default | Description                                   |
| -------------------- | ----------- | ------- | --------------------------------------------- |
| `--tier` / `-t`      | str (multi) | all     | Filter by tier: P0, P1, P2, P3 (repeatable)   |
| `--repo` / `-r`      | str (multi) | all     | Specific repository names (repeatable)        |
| `--workspace` / `-w` | Path        | `.`     | Target workspace directory                    |
| `--skip-setup`       | bool        | false   | Clone only, skip dependency install and hooks |

**stdout** (human):
```
Initializing Vindicta workspace...
[1/26] Cloning Vindicta-Core... ✓
[2/26] Cloning Vindicta-API... ✓
...
✓ Initialized 26 repositories in 7m 23s
```

**stdout** (`--json`):
```json
{
  "status": "success",
  "repos_cloned": 26,
  "repos_failed": 0,
  "duration_seconds": 443,
  "failures": []
}
```

**Exit codes**: 0 = success, 1 = partial failure (some repos failed), 2 = total failure

---

### `vindicta dev sync`

**Purpose**: Synchronize all repositories with remote state.

```bash
vindicta dev sync [OPTIONS]
```

| Option              | Type        | Default    | Description                                          |
| ------------------- | ----------- | ---------- | ---------------------------------------------------- |
| `--pull`            | bool        | config     | Auto-pull after fetch (overrides config `auto_pull`) |
| `--parallel` / `-p` | int         | config (4) | Max concurrent sync operations                       |
| `--tier` / `-t`     | str (multi) | all        | Filter by tier                                       |
| `--force`           | bool        | false      | Force pull even on non-default branches              |

**stdout** (human):
```
Syncing workspace...
  Vindicta-Core     main   ✓ up-to-date
  Vindicta-API      main   ↓ 3 behind
  Logi-Slate-UI     feat/x ⚠ skipped (dirty)
...
✓ Synced 24/26 repos in 45s (2 skipped)
```

**Exit codes**: 0 = all synced, 1 = some skipped (dirty/non-default), 2 = network failure

---

### `vindicta dev setup`

**Purpose**: Install dependencies and configure tooling for repositories.

```bash
vindicta dev setup [OPTIONS]
```

| Option          | Type        | Default | Description                       |
| --------------- | ----------- | ------- | --------------------------------- |
| `--repo` / `-r` | str (multi) | all     | Specific repository names         |
| `--skip-hooks`  | bool        | false   | Skip pre-commit hook installation |
| `--skip-venv`   | bool        | false   | Skip Python venv creation         |
| `--skip-node`   | bool        | false   | Skip Node.js dependency install   |

**Exit codes**: 0 = success, 1 = partial failure, 2 = total failure

---

### `vindicta dev status`

**Purpose**: Display workspace health dashboard.

```bash
vindicta dev status [OPTIONS]
```

| Option              | Type        | Default | Description                            |
| ------------------- | ----------- | ------- | -------------------------------------- |
| `--tier` / `-t`     | str (multi) | all     | Filter by tier                         |
| `--failing`         | bool        | false   | Show only repos with issues            |
| `--ci`              | bool        | false   | Include CI status (requires `gh` auth) |
| `--detailed` / `-d` | bool        | false   | Show expanded details per repo         |

**stdout** (human):
```
Vindicta Platform Workspace Status
═══════════════════════════════════
P0 Core (3/3 healthy)
  ✓ Vindicta-Core     main  ↑0 ↓0  CI:✓
  ✓ Vindicta-API      main  ↑0 ↓2  CI:✓
  ✓ Vindicta-Portal   main  ↑1 ↓0  CI:✓

P1 Primary (4/4 healthy)
  ...

Summary: 26 repos | 24 healthy | 2 issues
```

**Exit codes**: 0 = all healthy, 1 = issues detected

---

### `vindicta dev validate`

**Purpose**: Validate Platform Constitution compliance across repositories.

```bash
vindicta dev validate [OPTIONS]
```

| Option          | Type        | Default | Description                                          |
| --------------- | ----------- | ------- | ---------------------------------------------------- |
| `--repo` / `-r` | str (multi) | all     | Specific repository names                            |
| `--fix`         | bool        | config  | Auto-fix where possible                              |
| `--check`       | str (multi) | all     | Specific checks: constitution, context, links, hooks |

**stdout** (human):
```
Validating compliance...
  Vindicta-Core
    ✓ Constitution present
    ✓ .antigravity/ context artifacts
    ✗ Broken link in README.md:45
    ✓ Pre-commit hooks
  ...

Score: 24/26 repos compliant (92.3%)
```

**Exit codes**: 0 = all pass, 1 = failures detected (non-zero failed checks)

---

### `vindicta dev doctor`

**Purpose**: Diagnose environment issues and recommend fixes.

```bash
vindicta dev doctor [OPTIONS]
```

| Option  | Type | Default | Description                |
| ------- | ---- | ------- | -------------------------- |
| `--fix` | bool | false   | Auto-fix detectable issues |

**stdout** (human):
```
Environment Diagnostics
═══════════════════════
  ✓ git       2.43.0  (required: >=2.30)
  ✓ gh        2.45.0  (required: >=2.0)
  ✓ python    3.11.7  (required: >=3.10)
  ✓ uv        0.5.1   (required: >=0.1)
  ✗ node      —       (required: >=18.0)

  ✓ Workspace config valid
  ✗ 2 repos missing pre-commit hooks

Recommendations:
  1. Install Node.js >= 18.0: https://nodejs.org
  2. Run `vindicta dev setup --repo X Y` to install hooks
```

**Exit codes**: 0 = all healthy, 1 = issues found

---

### `vindicta dev clean`

**Purpose**: Remove build artifacts and reclaim disk space.

```bash
vindicta dev clean [OPTIONS]
```

| Option          | Type        | Default | Description                                 |
| --------------- | ----------- | ------- | ------------------------------------------- |
| `--dry-run`     | bool        | false   | Show what would be removed without deleting |
| `--type`        | str (multi) | all     | Target: python, nodejs, all                 |
| `--repo` / `-r` | str (multi) | all     | Specific repository names                   |

**stdout** (human):
```
Cleaning build artifacts...
  Vindicta-Core     __pycache__ (2.1MB), .pytest_cache (0.3MB)
  Logi-Slate-UI     node_modules (312MB), dist (4.2MB)
  ...

Reclaimed 1.2GB across 18 repositories
```

**Exit codes**: 0 = success, 1 = partial failure (permission issues)

---

### `vindicta dev config`

**Purpose**: Manage workspace configuration.

```bash
vindicta dev config [SUBCOMMAND] [OPTIONS]
```

**Subcommands**:

| Subcommand | Usage                                   | Description            |
| ---------- | --------------------------------------- | ---------------------- |
| `get`      | `vindicta dev config get <key>`         | Get a config value     |
| `set`      | `vindicta dev config set <key> <value>` | Set a config value     |
| `list`     | `vindicta dev config list`              | List all config values |
| `reset`    | `vindicta dev config reset [key]`       | Reset to default(s)    |

**Config keys**: `parallel_count`, `auto_pull`, `auto_fix`, `default_tier`, `verbose`, `json_output`, `sync_timeout`, `install_hooks`, `create_venvs`, `constitution_check`, `link_check`

**Exit codes**: 0 = success, 1 = invalid key/value
