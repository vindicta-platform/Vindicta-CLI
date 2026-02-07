# Developer Commands Reference

> Full reference for all `vindicta dev` commands.

## Global Flags

Every dev command supports:

| Flag        | Type | Description                              |
| ----------- | ---- | ---------------------------------------- |
| `--json`    | bool | Output machine-readable JSON             |
| `--verbose` | bool | Show detailed subprocess output          |
| `--help`    | bool | Display command help and available flags |

---

## `vindicta dev init`

Initialize workspace by cloning platform repositories.

```bash
vindicta dev init -w ~/vindicta-workspace
vindicta dev init --tier P0 --tier P1
vindicta dev init --repo Vindicta-Core --repo Vindicta-API
```

| Flag              | Type       | Default | Description                      |
| ----------------- | ---------- | ------- | -------------------------------- |
| `--workspace, -w` | PATH       | `.`     | Workspace root directory         |
| `--tier, -t`      | TEXT (mul) | all     | Filter by tier (P0, P1, P2, P3)  |
| `--repo, -r`      | TEXT (mul) | all     | Filter by repo name              |
| `--skip-setup`    | bool       | false   | Skip post-clone dependency setup |
| `--parallel`      | int        | 4       | Max parallel clone operations    |

---

## `vindicta dev sync`

Synchronize workspace repositories with their remotes.

```bash
vindicta dev sync
vindicta dev sync --pull --tier P0
vindicta dev sync --force
```

| Flag         | Type       | Default | Description                  |
| ------------ | ---------- | ------- | ---------------------------- |
| `--pull`     | bool       | false   | Auto-pull when behind remote |
| `--tier, -t` | TEXT (mul) | all     | Filter by tier               |
| `--force`    | bool       | false   | Sync even dirty repos        |
| `--parallel` | int        | 4       | Max parallel operations      |

---

## `vindicta dev setup`

Install dependencies and tooling for workspace repos.

```bash
vindicta dev setup
vindicta dev setup --repo Vindicta-Core --skip-venv
```

| Flag           | Type       | Default | Description                          |
| -------------- | ---------- | ------- | ------------------------------------ |
| `--repo, -r`   | TEXT (mul) | all     | Filter by repo name                  |
| `--skip-venv`  | bool       | false   | Skip Python venv creation            |
| `--skip-hooks` | bool       | false   | Skip pre-commit hook installation    |
| `--skip-node`  | bool       | false   | Skip Node.js dependency installation |

---

## `vindicta dev status`

Display a tier-grouped health dashboard.

```bash
vindicta dev status
vindicta dev status --tier P0 --failing
vindicta dev status --json
```

| Flag         | Type       | Default | Description                 |
| ------------ | ---------- | ------- | --------------------------- |
| `--tier, -t` | TEXT (mul) | all     | Filter by tier              |
| `--failing`  | bool       | false   | Show only repos with issues |
| `--ci`       | bool       | false   | Include CI status (slower)  |
| `--detailed` | bool       | false   | Show per-file dirty list    |

---

## `vindicta dev validate`

Run Platform Constitution compliance checks.

```bash
vindicta dev validate
vindicta dev validate --fix
vindicta dev validate --check constitution --check hooks
```

| Flag         | Type       | Default | Description                |
| ------------ | ---------- | ------- | -------------------------- |
| `--repo, -r` | TEXT (mul) | all     | Filter by repo name        |
| `--fix`      | bool       | false   | Auto-fix remediable issues |
| `--check`    | TEXT (mul) | all     | Run specific checks only   |
| `--tier, -t` | TEXT (mul) | all     | Filter by tier             |

**Checks available**: `constitution`, `context`, `links`, `hooks`

---

## `vindicta dev doctor`

Diagnose development environment health.

```bash
vindicta dev doctor
vindicta dev doctor --fix
vindicta dev doctor --json
```

| Flag    | Type | Default | Description                         |
| ------- | ---- | ------- | ----------------------------------- |
| `--fix` | bool | false   | Attempt to auto-fix detected issues |

**Checks**: git, gh CLI, python, uv, node, npm, pre-commit, workspace config, stale locks.

---

## `vindicta dev clean`

Remove build artifacts and caches from workspace repos.

```bash
vindicta dev clean --dry-run
vindicta dev clean --type python --type node
vindicta dev clean --repo Vindicta-Core
```

| Flag         | Type       | Default | Description                         |
| ------------ | ---------- | ------- | ----------------------------------- |
| `--dry-run`  | bool       | false   | Report without deleting             |
| `--type`     | TEXT (mul) | all     | Filter by type (python, node, venv) |
| `--repo, -r` | TEXT (mul) | all     | Filter by repo name                 |

---

## `vindicta dev config`

Manage workspace configuration values stored in `.vindicta-workspace.yml`.

### `vindicta dev config get <key>`

```bash
vindicta dev config get parallel_count
```

### `vindicta dev config set <key> <value>`

```bash
vindicta dev config set parallel_count 8
vindicta dev config set auto_pull true
```

### `vindicta dev config list`

```bash
vindicta dev config list
vindicta dev config list --json
```

### `vindicta dev config reset [key]`

```bash
vindicta dev config reset parallel_count    # Reset one key
vindicta dev config reset                   # Reset all to defaults
```

**Available keys**:

| Key              | Type | Default | Range  | Description                  |
| ---------------- | ---- | ------- | ------ | ---------------------------- |
| `parallel_count` | int  | 4       | 1–16   | Max concurrent operations    |
| `auto_pull`      | bool | false   | —      | Auto-pull on sync            |
| `sync_timeout`   | int  | 120     | 10–600 | Sync operation timeout (sec) |
| `auto_setup`     | bool | true    | —      | Auto-setup after clone       |
| `auto_validate`  | bool | false   | —      | Auto-validate after sync     |
