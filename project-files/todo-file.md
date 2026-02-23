# TODO File

> Current phase tasks — must reference PROJECT phase

---

Format: YAML

```yaml
# TODO - Current Tasks

phase: 25
id: content-expansion
title: Content expansion

# Quick Reference
secrets: ~/.env/
  - api-key-file    # Description
rules: ~/.rules/
  - Python/RULES
  - JS/RULES
services:
  - service-name    # What it's for

tasks:
  - task: Description of task
    status: pending

  - task: Another task
    status: in_progress

  - task: Completed task
    status: done

blockers: []

notes: |
  Optional context for this phase.
```

## Task Status Values

- `pending` — Not started
- `in_progress` — Currently working on
- `done` — Completed

## Rules

RULE: `phase:` and `id:` MUST match PROJECT.phase and PROJECT.id
RULE: Tasks MUST belong to current phase (no scope creep)
RULE: When all tasks `done` → move to DONE, update PROJECT, start next phase
