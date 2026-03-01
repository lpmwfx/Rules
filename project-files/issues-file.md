---
tags: [issues, fifo, problem-queue]
concepts: [issue-tracking, fifo, problem-resolution]
feeds: [project-files/fixes-file.md]
related: [project-files/todo-file.md]
keywords: [fifo, open, committed, resolved]
layer: 2
---
# ISSUES.md File

> Problem queue — FIFO order, no skipping

---

## Quick Reference

- **Location:** `proj/ISSUES.md`
- **Format:** Markdown — `## YYYY-MM-DD: title` sections + DONES separator
- **Required:** Always
- **Order:** FIFO — oldest open issue handled first

The problem queue. AI adds discovered issues here instead of fixing them
immediately. Issues must be resolved in order. Resolved entries move below
the DONES line and must have a corresponding FIXES.md entry.

---

RULE: File lives at `proj/ISSUES.md`
RULE: AI discovers issue → add to ISSUES.md, do NOT fix without user approval
RULE: FIFO order — handle oldest open issue first, no skipping
RULE: Resolved issues MUST have a corresponding FIXES.md entry
RULE: Resolved issues move below `# --- DONES ---` line

## Format

```markdown
# ISSUES: project-name

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
Resolution: Load dotenv at script entry. See FIXES.md 2026-02-20.
```

## Status Values

- `open` — Reported, not yet assigned
- `committed` — Assigned to a phase or task, being worked on
- `resolved` — Fixed and verified (must have FIXES.md entry)

## FIFO Rule

Issues are handled in order — oldest open first.
Exceptions require explicit user approval with documented reason.

## Relations

```
Problem discovered
  └── ISSUES.md entry (open)
        └── Assigned to phase/task (committed)
              └── Fixed and verified (resolved)
                    └── FIXES.md entry (Problem → Cause → Solution)
```
