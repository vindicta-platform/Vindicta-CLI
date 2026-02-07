# Vindicta-CLI Roadmap

> **Vision**: Command-line interface for platform operations
> **Status**: Utility (P3)
> **Last Updated**: 2026-02-03

---

## v1.0 Target: Q2 2026

### Mission Statement
Provide a command-line interface for developers and power users to interact with Vindicta platform services without the web UI.

---

## Milestone Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│  Apr 2026          May 2026          Jun 2026                   │
│  ─────────────────────────────────────────────────────────────  │
│  [v0.1.0]          [v0.2.0]          [v1.0.0]                   │
│  Foundation        Core Commands     Full CLI                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## v0.1.0 — Foundation (Target: Apr 2026)

### Deliverables
- [ ] CLI framework (Click or Typer)
- [ ] Auth command (API key setup)
- [ ] Config management
- [ ] Help system

---

## v0.2.0 — Core Commands (Target: May 2026)

### Deliverables
- [ ] `vindicta grade <list.json>` — Grade a list via Meta-Oracle
- [ ] `vindicta meta snapshot` — Get current meta
- [ ] `vindicta game new` — Start recording a game
- [ ] `vindicta transcript <id>` — Export WARScribe transcript

---

## v1.0.0 — Full CLI (Target: Jun 2026)

### Deliverables
- [ ] All API endpoints accessible
- [ ] Scripting support (JSON output)
- [ ] Shell completions
- [ ] PyPI publication

---

## Dependencies

- Vindicta-API (backend)
- WARScribe-Core (transcript format)

---

*Maintained by: Vindicta Platform Team*
