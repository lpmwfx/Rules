---
tags: [todo, tasks, tracking, pass-criteria]
concepts: [task-tracking, pass-criteria]
requires: [project-files/phases-file.md, project-files/project-file.md]
feeds: [project-files/done-file.md]
related: [project-files/issues-file.md, project-files/project-process.md]
layer: 2
---
# TODO File

> Current phase tasks — tracks work, status, and pass criteria

---

## Quick Reference

- **Location:** `proj/TODO`
- **Format:** Markdown headings + YAML list items in body
- **Required:** Always
- **Phase lock:** `phase` and `id` must match `proj/PROJECT`

One TODO per active phase. Tasks are YAML list items grouped under
Markdown category headings. When all tasks are done, archive to DONE.

---

RULE: File lives at `proj/TODO`
RULE: `phase` and `id` at top MUST match PROJECT.md current phase
RULE: Tasks MUST belong to the current phase — no scope creep
RULE: AI updates task status as work progresses
RULE: When all tasks done → archive to DONE, update PROJECT, create new TODO.md
RULE: `pass:` defines the success criterion — how to verify the task is truly done

## Format

```markdown
# TODO: phase-title

phase: 25
id: content-expansion

## Category Name

- id: 1
  task: Description of what needs to be done
  pass: How to verify it's done (test, output, observable result)
  status: pending

- id: 2
  task: Another task in this category
  pass: What done looks like
  status: in_progress

## Another Category

- id: 3
  task: Task in second category
  status: pending

## Blockers

- blocker description, or leave empty

# --- DONES ---

- id: N
  task: Completed task description
  status: done
```

## Task Status Values

- `pending` — Not started
- `in_progress` — Currently working on (only one at a time per AI session)
- `done` — Completed and verified — move below DONES

## Rules

RULE: One task `in_progress` at a time per AI session
RULE: `pass:` is binary — it either passes or it doesn't
RULE: Completed tasks move below `# --- DONES ---`, not deleted
RULE: New tasks discovered during work go to ISSUES.md first, not directly to TODO.md
