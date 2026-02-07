# Python as Primary Language

* Status: accepted
* Date: 2026-02-01

## Context and Problem Statement

This repository requires a programming language for implementation.

## Decision Outcome

We adopt **Python 3.10+** as the primary language.

### Rationale

- Vindicta Platform is Python-first
- Typer/Rich CLI ecosystem
- Seamless integration with other modules

## Considered Options

| Alternative | Decision                    |
| ----------- | --------------------------- |
| Rust        | Rejected — slower iteration |
| Go          | Rejected — less expressive  |

## Consequences

### Positive

- All source code uses Python 3.10+
- Type hints required on all public APIs

### Negative

- Limits performance-critical paths to Python's capabilities
