# Vindicta-CLI

Unified command-line interface for the Vindicta Platform.

## Overview

Vindicta-CLI provides a Typer-based CLI for all platform operations, from dice rolling to Meta-Oracle queries.

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/Vindicta-CLI.git
```

Or clone locally:

```bash
git clone https://github.com/vindicta-platform/Vindicta-CLI.git
cd Vindicta-CLI
uv pip install -e .
```

## Usage

```bash
vindicta dice roll 2d6
vindicta economy balance
vindicta oracle predict --army mylist.warscribe
```

## License

MIT License - See [LICENSE](./LICENSE) for details.
