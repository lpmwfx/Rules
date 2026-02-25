---
tags: [issues, fifo, problem-queue]
concepts: [issue-tracking, fifo, problem-resolution]
feeds: [project-files/fixes-file.md]
related: [project-files/todo-file.md]
keywords: [fifo, open, committed, resolved]
layer: 2
---
# ISSUES File

> Problem queue — FIFO order, no skipping

---

Format: Plain text

```
# ISSUES

## 2026-02-25: Login fails after session timeout
Status: open
Found during: Phase 2, task "session management"
Description: After 30 min idle, login POST returns 500 instead of redirect.

## 2026-02-24: CSS grid breaks on mobile Safari
Status: committed
Found during: Phase 2, task "responsive layout"
Description: Grid items overlap when viewport < 375px.
Assigned: Phase 2 hotfix

# --- DONES ---

## 2026-02-20: Build script ignores .env
Status: resolved
Found during: Phase 1, task "build pipeline"
Description: dotenv not loaded before config parsing.
Resolution: Load dotenv at script entry. See FIXES 2026-02-20.
```

## Status Values

- `open` — Reported, not yet assigned
- `committed` — Assigned to a phase or task, being worked on
- `resolved` — Fixed and verified (must have FIXES entry)

## DONES Line

See [workflow.md](workflow.md) for full DONES mechanics. Issues move below DONES when resolved.

## FIFO Rule

Issues are handled in order — oldest first, no skipping ahead.

Exceptions require explicit user approval with documented reason.

## Rules

RULE: Date + short title for each entry
RULE: Include `Found during:` to trace back to phase/task
RULE: FIFO order — handle oldest open issue first
RULE: Resolved issues MUST have a corresponding FIXES entry
RULE: AI discovers issue → add to ISSUES, do NOT fix without approval
RULE: Move resolved issues below DONES line

## Relations

```
Problem discovered
  └── ISSUES entry (open)
        └── Assigned to phase/task (committed)
              └── Fixed and verified (resolved)
                    └── FIXES entry (Problem → Cause → Solution)
```
