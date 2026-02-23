# Project Files Specification

> Standard project files for AI-assisted development

---

All AI tools should read/write these files consistently.

## File Overview

| File | Format | Purpose | AI Action |
|------|--------|---------|-----------|
| PROJECT | YAML | Project state (past, present, future) | READ first |
| TODO | YAML | Current phase tasks | READ for work, UPDATE status |
| DONE | YAML | Completed phases + tasks | APPEND when phase complete |
| FIXES | Text | Problem → Cause → Solution | READ before coding, WRITE after fixing |
| RAG | Text | Knowledge, links, discoveries | READ for context, WRITE findings |
| INSTALL | Text | Setup instructions | READ for environment setup |
| AUTHORS | Text | Contributors (human + AI) | READ for attribution |
| CHANGELOG | Text | Release notes (user-facing) | APPEND on release |
| doc/project.md | Markdown | Human narrative (WHY) | READ for architecture rationale |

## Files

| File | Topic |
|------|-------|
| [project-file.md](project-file.md) | PROJECT spec |
| [todo-file.md](todo-file.md) | TODO spec |
| [done-file.md](done-file.md) | DONE spec |
| [fixes-file.md](fixes-file.md) | FIXES spec |
| [rag-file.md](rag-file.md) | RAG spec |
| [changelog-file.md](changelog-file.md) | CHANGELOG spec |
| [install-file.md](install-file.md) | INSTALL spec |
| [authors-file.md](authors-file.md) | AUTHORS spec |
| [workflow.md](workflow.md) | Workflow + validation |
