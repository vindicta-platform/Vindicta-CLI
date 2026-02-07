# Feature Proposal: Unified CLI Experience

**Proposal ID**: FEAT-013
**Author**: Unified Product Architect (Autonomous)
**Created**: 2026-02-01
**Status**: Draft
**Priority**: High

---

## Part A: Software Design Document (SDD)

### 1. Executive Summary

Consolidate all Vindicta command-line tools into a single unified CLI with subcommands, providing a consistent user experience for dice rolling, army list management, quota checks, and platform administration.

### 2. System Architecture

#### 2.1 Current State
- Separate CLI tools per repository
- Inconsistent command syntax
- No unified help system
- Fragmented configuration

#### 2.2 Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Vindicta CLI                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   vindicta                              │    │
│  │   ├── dice roll 2d6+4                                   │    │
│  │   ├── army import mylist.rosz                           │    │
│  │   ├── quota status                                      │    │
│  │   ├── oracle predict warscribe_list.json           │    │
│  │   └── admin users list                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│      ┌───────────────────────┼───────────────────────────┐      │
│      ▼                       ▼                       ▼          │
│ ┌──────────┐          ┌──────────┐          ┌──────────┐        │
│ │Dice-Engine│         │WARScribe │          │Meta-Oracle│       │
│ │  Plugin  │          │  Plugin  │          │  Plugin  │        │
│ └──────────┘          └──────────┘          └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.3 File Changes

```
Vindicta-CLI/
├── src/
│   └── vindicta_cli/
│       ├── __init__.py          [MODIFY] Plugin registration
│       ├── main.py              [MODIFY] Unified entry point
│       ├── plugins/
│       │   ├── __init__.py      [NEW]
│       │   ├── dice.py          [NEW] Dice subcommands
│       │   ├── army.py          [NEW] Army list subcommands
│       │   ├── oracle.py        [NEW] Meta-Oracle subcommands
│       │   ├── quota.py         [NEW] Quota subcommands
│       │   └── admin.py         [NEW] Admin subcommands
│       └── config.py            [NEW] Unified config
├── tests/
│   └── test_plugins.py          [NEW]
└── docs/
    └── unified-cli.md           [NEW]
```

### 3. Command Structure

| Command | Subcommand | Description |
|---------|------------|-------------|
| `vindicta dice` | `roll`, `stats`, `verify` | Dice operations |
| `vindicta army` | `import`, `export`, `validate` | Army list management |
| `vindicta oracle` | `predict`, `stats`, `trends` | Meta-Oracle queries |
| `vindicta quota` | `status`, `usage`, `forecast` | Quota monitoring |
| `vindicta battle` | `log`, `history`, `stats` | Battle tracking |
| `vindicta admin` | `users`, `config`, `audit` | Administration |

### 4. Plugin System

```python
from typer import Typer

class CLIPlugin:
    """Base class for CLI plugins."""
    name: str
    app: Typer

    def register(self, parent: Typer):
        parent.add_typer(self.app, name=self.name)

# Plugin discovery
def discover_plugins() -> list[CLIPlugin]:
    """Discover and load all installed plugins."""
    return [
        DicePlugin(),
        ArmyPlugin(),
        OraclePlugin(),
        QuotaPlugin(),
        BattlePlugin(),
    ]
```

### 5. Configuration

```toml
# ~/.vindicta/config.toml
[api]
base_url = "https://api.vindicta-warhammer.web.app"
timeout = 30

[auth]
token_path = "~/.vindicta/token"

[defaults]
output_format = "rich"  # rich, json, plain
verbose = false
```

---

## Part B: Behavior Driven Development (BDD)

### User Stories

#### US-001: Unified Commands
**As a** power user
**I want** one CLI for all Vindicta tools
**So that** I don't need to remember multiple command names

#### US-002: Consistent Output
**As a** script author
**I want** JSON output option for all commands
**So that** I can parse results programmatically

#### US-003: Plugin Extensibility
**As a** developer
**I want to** create custom CLI plugins
**So that** I can extend the platform for my needs

### Acceptance Criteria

```gherkin
Feature: Unified CLI

  Scenario: Roll dice via CLI
    When I run "vindicta dice roll 3d6+2"
    Then I should see the roll result
    And the notation should be validated

  Scenario: Import army list
    When I run "vindicta army import mylist.rosz"
    Then the BattleScribe file should be converted
    And saved to local storage

  Scenario: JSON output mode
    When I run "vindicta oracle stats --format json"
    Then the output should be valid JSON
    And parseable by jq

  Scenario: Help system
    When I run "vindicta --help"
    Then I should see all available subcommands
    And descriptions for each
```

---

## Implementation Estimate

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| Core Architecture | 4 hours | Typer |
| Plugin System | 6 hours | None |
| Migrate Commands | 8 hours | Existing CLIs |
| Configuration | 3 hours | None |
| Documentation | 3 hours | None |
| **Total** | **24 hours** | |
