---
tags: [phases, milestones, planning]
concepts: [milestone-tracking, phase-management]
requires: [project-files/project-file.md]
feeds: [project-files/todo-file.md, project-files/done-file.md]
related: [project-files/goal-chain.md]
layer: 2
---
# PHASES File

> Milestone reference — what the project delivers and when

---

## Quick Reference

- **Location:** `proj/PHASES`
- **Format:** Markdown headings + YAML list items in body
- **Required:** Always
- **Owner:** User defines milestones — AI reads, suggests updates

Each phase has a milestone (what gets proven) and delivers (what gets built).
Only ONE phase is `active` at a time. Completed phases move below DONES.

---

RULE: File lives at `proj/PHASES`
RULE: Each phase must have a `milestone:` that traces to PROJECT.md Goal
RULE: `delivers:` lists concrete outputs — not vague descriptions
RULE: Only ONE phase may be `active` at a time
RULE: Active phase must match PROJECT.md current phase and TODO.md phase
RULE: User owns PHASES.md — AI reads for overview, suggests updates
RULE: When phase completes → move below DONES, update PROJECT.md, archive TODO.md to DONE.md

## Format

```markdown
# PHASES: project-name

## Active

- phase: 2
  id: core-features
  title: "Core features"
  milestone: "Primary user workflow functional end-to-end"
  delivers:
    - Feature A implementation
    - Feature B implementation
    - Integration tests
  status: active

## Planned

- phase: 3
  id: polish
  title: "Polish and publish"
  milestone: "Ready for public use"
  delivers:
    - Error handling
    - Documentation
    - Publishing pipeline
  status: planned

# --- DONES ---

- phase: 1
  id: foundation
  title: "Project foundation"
  milestone: "Core architecture in place and testable"
  delivers:
    - Project structure
    - Base configuration
    - Test framework
  status: done
  completed: 2026-01-10
```

## Status Values

- `planned` — Scheduled but not started
- `active` — Currently being worked on (only ONE at a time)
- `blocked` — Cannot proceed (blocker documented in ISSUES.md)
- `done` — All delivers verified, milestone reached

## DONES Line

Phases move below `# --- DONES ---` when completed.
See [workflow.md](workflow.md) for full DONES mechanics.

## Relations

```
PROJECT.md Goal
  └── PHASES.md milestone    (each milestone serves the Goal)
        └── PHASES.md delivers  (what gets built)
              └── TODO.md tasks   (current work within active phase)
```
