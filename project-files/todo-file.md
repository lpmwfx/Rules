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

- **Location:** `proj/TODO` (primary), `proj/<NAME>-TODO` (additional)
- **Format:** Markdown headings + YAML list items in body
- **Required:** Always
- **Phase lock:** `phase` and `id` must match `proj/PROJECT`

`TODO` is the primary task truth for the active phase. Additional TODO files
(`TOOL-TODO`, `AUT-TODO`, etc.) may run in parallel for separate workstreams.
When a TODO file is fully done, move it as-is to `proj/DONES/` and create a new one.

---

RULE: Primary file lives at `proj/TODO`
RULE: `phase` and `id` at top MUST match PROJECT current phase
RULE: Tasks MUST belong to the current phase — no scope creep
RULE: AI updates task status as work progresses
RULE: When all tasks in a TODO file are done → move the file to `proj/DONES/` and create a new TODO
RULE: `pass:` defines the success criterion — how to verify the task is truly done
RULE: Additional TODO files may be named `proj/<NAME>-TODO` for parallel workstreams
RULE: `proj/TODO` is always the top task truth — other TODO files are subordinate

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
```

## Task Status Values

- `pending` — Not started
- `in_progress` — Currently working on (only one at a time per AI session)
- `done` — Completed and verified — remove from file when whole TODO is archived

## Rules

RULE: One task `in_progress` at a time per AI session
RULE: `pass:` is binary — it either passes or it doesn't
RULE: Completed tasks are removed when the whole TODO file moves to `proj/DONES/`
RULE: New tasks discovered during work go to ISSUES first, not directly to TODO
RULE: Keep TODO files to a manageable size — split into named TODO files if needed


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
