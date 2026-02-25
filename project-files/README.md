---
tags: [project-files, overview, specification]
concepts: [project-methodology, file-specification]
related: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md, project-files/done-file.md, project-files/issues-file.md, project-files/fixes-file.md, project-files/rag-file.md, project-files/workflow.md, project-files/changelog-file.md, project-files/install-file.md, project-files/uiux-file.md, project-files/authors-file.md, project-files/goal-chain.md]
layer: 6
---
# Project Files Specification

> Standard project files for AI-assisted development

---

All AI tools should read/write these files consistently.

## File Overview

| File | Format | Purpose | AI Action |
|------|--------|---------|-----------|
| PROJECT | YAML | Project state (past, present, future) | READ first, WRITE to maintain |
| PHASES | YAML | Milestones + delivers | READ for overview |
| TODO | YAML | Current phase tasks | READ for work, UPDATE status |
| DONE | YAML | Completed phases + tasks | APPEND when phase complete |
| ISSUES | Text | Problem queue (FIFO) | READ + WRITE |
| FIXES | Text | Problem → Cause → Solution | READ before coding, WRITE after fixing |
| RAG | Text | Knowledge, links, discoveries | READ for context, WRITE findings |
| INSTALL | Text | Publishing + setup | READ for environment and publishing |
| UIUX | Text | UI/UX spec (GUI projects) | READ for GUI work |
| AUTHORS | Text | Contributors (human + AI) | READ for attribution |
| CHANGELOG | Text | Release notes (user-facing) | APPEND on release |
| doc/project.md | Markdown | Human narrative (WHY) | READ for architecture rationale |

## Files

| File | Topic |
|------|-------|
| [project-file.md](project-file.md) | PROJECT spec |
| [phases-file.md](phases-file.md) | PHASES spec |
| [todo-file.md](todo-file.md) | TODO spec |
| [done-file.md](done-file.md) | DONE spec |
| [issues-file.md](issues-file.md) | ISSUES spec |
| [fixes-file.md](fixes-file.md) | FIXES spec |
| [rag-file.md](rag-file.md) | RAG spec |
| [changelog-file.md](changelog-file.md) | CHANGELOG spec |
| [install-file.md](install-file.md) | INSTALL spec |
| [uiux-file.md](uiux-file.md) | UIUX spec |
| [authors-file.md](authors-file.md) | AUTHORS spec |
| [goal-chain.md](goal-chain.md) | Goal chain + DONES |
| [workflow.md](workflow.md) | Workflow, relations, publishing |
