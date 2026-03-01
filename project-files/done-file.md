---
tags: [done, archive, completed-phases]
concepts: [phase-completion, archive]
requires: [project-files/todo-file.md, project-files/phases-file.md]
layer: 2
---
# DONE File

> Completed phases with their tasks — append-only archive

---

## Quick Reference

- **Location:** `proj/DONE`
- **Format:** Markdown headings + YAML list items in body
- **Required:** Always
- **Write rule:** Append only — newest phase at top, never edit past entries

Archive of completed phases. When a phase finishes, copy tasks from TODO.md
and append a new entry here. Never edit entries already in DONE.

---

RULE: File lives at `proj/DONE`
RULE: Append completed phases at TOP — newest first
RULE: Include `completed:` date on every entry
RULE: Copy task descriptions from TODO when phase completes
RULE: Never edit or delete existing entries — DONE is append-only
RULE: DONE grows forever — it is the project history

## Format

```markdown
# DONE: project-name

- phase: 25
  id: content-expansion
  title: "Content expansion"
  completed: 2026-02-15
  tasks:
    - Write content for section A
    - Update navigation links
    - Review and publish

- phase: 24
  id: css-refactor
  title: "CSS/JS Modular Refactor"
  completed: 2026-01-24
  tasks:
    - Separate colors from layout
    - Add CSS variables to theme
    - Update all components
```

## Rules

RULE: Tasks list is a summary — copy task descriptions, not full YAML task objects
RULE: If a phase had blockers, note them briefly in a `notes:` field
