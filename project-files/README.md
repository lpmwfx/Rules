---
tags: [project-files, overview, specification]
concepts: [project-methodology, file-specification]
related: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md, project-files/done-file.md, project-files/issues-file.md, project-files/fixes-file.md, project-files/rag-file.md, project-files/workflow.md, project-files/changelog-file.md, project-files/install-file.md, project-files/uiux-file.md, project-files/authors-file.md, project-files/goal-chain.md]
layer: 6
---
# Project Files Specification

> Standard project files for AI-assisted development — all live in `proj/` as `.md` files

---

All AI tools should read/write these files consistently.

## Location Convention

VITAL: All project files live in the `proj/` subfolder — never in the project root
VITAL: All project files use `.md` extension
RULE: Create `proj/` on project init if it does not exist
RULE: `proj/` is excluded from the public repo — it is private dev state
BANNED: Placing project files in project root
BANNED: Using `.yaml`, `.txt` or no extension for project files

```
my-project/
├── src/
├── tests/
├── proj/                ← all project files live here
│   ├── PROJECT.md       ← Markdown narrative (goal, architecture, history)
│   ├── PHASES.md        ← Markdown + YAML task-list body (milestones)
│   ├── TODO.md          ← Markdown + YAML task-list body (current phase)
│   ├── DONE.md          ← Markdown append-only log
│   ├── ISSUES.md        ← Markdown FIFO queue + DONES separator
│   ├── FIXES.md         ← Markdown append-only log
│   ├── RAG.md           ← Markdown freeform knowledge base
│   ├── INSTALL.md       ← Markdown setup + publish instructions
│   ├── UIUX.md          ← Markdown UI/UX spec (GUI projects only)
│   ├── AUTHORS.md       ← Markdown contributor list
│   └── CHANGELOG.md     ← Markdown release notes (newest first)
└── doc/
    └── project.md       ← human narrative (WHY) — not a management file
```

## File Overview

| File | Format | Required | Purpose | AI Action |
|------|--------|----------|---------|-----------|
| PROJECT.md | Markdown | Always | Project identity + state | READ first, WRITE to maintain |
| PHASES.md | Markdown + YAML list | Always | Milestones + delivers | READ for overview |
| TODO.md | Markdown + YAML list | Always | Current phase tasks | READ for work, UPDATE status |
| DONE.md | Markdown | Always | Completed phases archive | APPEND when phase complete |
| ISSUES.md | Markdown | Always | Problem queue (FIFO) | READ + WRITE |
| FIXES.md | Markdown | Always | Problem → Cause → Solution | READ before coding, WRITE after fixing |
| RAG.md | Markdown | Always | Knowledge, links, discoveries | READ for context, WRITE findings |
| INSTALL.md | Markdown | Always | Publishing + setup | READ for environment |
| UIUX.md | Markdown | GUI only | UI/UX specification | READ for GUI work |
| AUTHORS.md | Markdown | Always | Contributors (human + AI) | READ for attribution |
| CHANGELOG.md | Markdown | Always | Release notes (user-facing) | APPEND on release |

## Rule Files

| File | Topic |
|------|-------|
| [project-file.md](project-file.md) | PROJECT.md spec |
| [phases-file.md](phases-file.md) | PHASES.md spec |
| [todo-file.md](todo-file.md) | TODO.md spec |
| [done-file.md](done-file.md) | DONE.md spec |
| [issues-file.md](issues-file.md) | ISSUES.md spec |
| [fixes-file.md](fixes-file.md) | FIXES.md spec |
| [rag-file.md](rag-file.md) | RAG.md spec |
| [changelog-file.md](changelog-file.md) | CHANGELOG.md spec |
| [install-file.md](install-file.md) | INSTALL.md spec |
| [uiux-file.md](uiux-file.md) | UIUX.md spec |
| [authors-file.md](authors-file.md) | AUTHORS.md spec |
| [goal-chain.md](goal-chain.md) | Goal chain + DONES |
| [workflow.md](workflow.md) | Workflow, relations, publishing |
