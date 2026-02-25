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

Format: YAML

```yaml
# PHASES - Milestones and Delivers

phases:

  - phase: 1
    id: foundation
    title: "Project foundation"
    milestone: "Core architecture in place and testable"
    delivers:
      - Project structure
      - Base configuration
      - Test framework
    status: done

  - phase: 2
    id: core-features
    title: "Core features"
    milestone: "Primary user workflow functional end-to-end"
    delivers:
      - Feature A implementation
      - Feature B implementation
      - Integration tests
    status: active

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

# Phases below this line are completed and evaluated.
# Active and planned phases stay above.
```

## Status Values

- `planned` — Scheduled but not started
- `active` — Currently being worked on (only ONE phase active at a time)
- `blocked` — Cannot proceed (blocker documented in ISSUES)
- `done` — All delivers verified, milestone reached

## DONES Line

See [workflow.md](workflow.md) for full DONES mechanics. Phases move below DONES when completed.

## Rules

RULE: Each phase must have a `milestone:` that traces to PROJECT Goal
RULE: `delivers:` lists concrete outputs — not vague descriptions
RULE: Only ONE phase may be `active` at a time
RULE: `active` phase must match PROJECT.phase and TODO.phase
RULE: User owns PHASES — AI reads for overview, suggests updates
RULE: When phase completes → move below DONES, update PROJECT, archive TODO to DONE

## Relations

```
PROJECT Goal
  └── PHASES milestone    (each milestone serves the Goal)
        └── PHASES delivers  (what gets built)
              └── TODO tasks   (current work within active phase)
```
