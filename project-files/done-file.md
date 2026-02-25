---
tags: [done, archive, completed-phases]
concepts: [phase-completion, archive]
requires: [project-files/todo-file.md, project-files/phases-file.md]
layer: 2
---
# DONE File

> Completed phases with their tasks — append-only log

---

Format: YAML

```yaml
# DONE - Completed Work

phases:
  - phase: 24
    id: css-refactor
    title: "CSS/JS Modular Refactor"
    completed: 2026-01-24
    tasks:
      - Separate colors from layout
      - Add CSS variables to theme
      - Update all components

  - phase: 23
    id: netgiganten-deploy
    title: "Netgiganten Deploy"
    completed: 2026-01-20
    tasks:
      - Setup rsync
      - Configure SSH
      - Test deploy pipeline
```

## Rules

RULE: Append completed phases at TOP (newest first)
RULE: Include `completed:` date
RULE: Copy tasks from TODO when phase completes
