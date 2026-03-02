---
tags: [project-files, overview, specification]
concepts: [project-methodology, file-specification]
related: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md, project-files/done-file.md, project-files/issues-file.md, project-files/fixes-file.md, project-files/rag-file.md, project-files/workflow.md, project-files/changelog-file.md, project-files/install-file.md, project-files/uiux-file.md, project-files/authors-file.md, project-files/goal-chain.md]
layer: 6
---
# Project Files Specification

> Standard project files for AI-assisted development — all live in `proj/`, no file extension

---

All AI tools should read/write these files consistently.

## Location Convention

VITAL: All project files live in the `proj/` subfolder — never in the project root
VITAL: Project files have NO file extension — `proj/PROJECT` not `proj/PROJECT.md`
RULE: Create `proj/` on project init if it does not exist
RULE: `proj/` is excluded from the public repo — it is private dev state
BANNED: Placing project files in project root
BANNED: Adding any extension (.md, .yaml, .txt) to project files

```
my-project/
├── src/
├── tests/
├── proj/              ← all project files live here, NO extensions
│   ├── PROJECT        ← Markdown narrative (goal, architecture, history)
│   ├── PHASES         ← Markdown + YAML list body (milestones)
│   ├── TODO           ← Markdown + YAML list body (current phase)
│   ├── DONE           ← Markdown append-only log
│   ├── ISSUES         ← Markdown FIFO queue + DONES separator
│   ├── FIXES          ← Markdown append-only log
│   ├── RAG            ← Markdown freeform knowledge base
│   ├── INSTALL        ← Markdown setup + publish instructions
│   ├── UIUX           ← Markdown UI/UX spec (GUI projects only)
│   ├── RULES          ← AI rule observations + active MCP rules for this phase
│   ├── AUTHORS        ← Markdown contributor list
│   └── CHANGELOG      ← Markdown release notes (newest first)
```

## File Overview

| File | Format | Required | Purpose | AI Action |
|------|--------|----------|---------|-----------|
| PROJECT | Markdown | Always | Project identity + state — only source of truth | READ first, WRITE to maintain |
| RULES | Markdown | Always | Active MCP rules + project-specific conventions | READ second, WRITE on observation |
| PHASES | Markdown + YAML list | Always | Milestones + delivers | READ for overview |
| TODO | Markdown + YAML list | Always | Current phase tasks | READ for work, UPDATE status |
| DONE | Markdown | Always | Completed phases archive | APPEND when phase complete |
| ISSUES | Markdown | Always | Problem queue (FIFO) | READ + WRITE |
| FIXES | Markdown | Always | Problem → Cause → Solution | READ before coding, WRITE after fixing |
| RAG | Markdown | Always | Knowledge, links, discoveries | READ for context, WRITE findings |
| INSTALL | Markdown | Always | Publishing + setup | READ for environment |
| UIUX | Markdown | All GUI projects | UI/UX source of truth — platform, flows, conventions | READ before any UI work, WRITE on discovery |
| AUTHORS | Markdown | Always | Contributors (human + AI) | READ for attribution |
| CHANGELOG | Markdown | Always | Release notes (user-facing) | APPEND on release |

## Rule Files

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
| [rules-file.md](rules-file.md) | RULES spec |
| [authors-file.md](authors-file.md) | AUTHORS spec |
| [goal-chain.md](goal-chain.md) | Goal chain + DONES |
| [workflow.md](workflow.md) | Workflow, relations, publishing |
