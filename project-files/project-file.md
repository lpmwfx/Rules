---
tags: [project, state, identity, source-of-truth]
concepts: [project-state, source-of-truth]
requires: [project-files/goal-chain.md]
feeds: [project-files/phases-file.md, project-files/todo-file.md]
related: [project-files/workflow.md]
layer: 2
---
# PROJECT File

> Project identity and state — what's built, where we are, what's planned

---

## Quick Reference

- **Location:** `proj/PROJECT`
- **Format:** Markdown narrative — headings and prose, no YAML lists
- **Required:** Always
- **Read by AI:** First, every session — before any work

Single source of truth for everything about the project: goal, stack,
infrastructure, patterns, history, and current phase. AI keeps it current.

---

RULE: File lives at `proj/PROJECT`
RULE: AI reads PROJECT.md before any work — no exceptions
RULE: AI maintains PROJECT.md — keeps it current after every significant change
RULE: User reviews and approves PROJECT.md updates
RULE: AI never changes the `## Goal` section without explicit user approval

## Format

```markdown
# PROJECT: project-name

## Goal
The vision — what we want to achieve. Free text, 2-5 sentences.
This section changes rarely. AI never edits without user approval.

## Stack
- Language: Python 3.11+ / Rust 2021 / Node 22
- Framework: FastAPI / Axum / React
- Tools: [key tools and libraries]

## Structure
- src:    src/
- output: dist/
- config: config/
- proj:   proj/

## Method
- Workflow: PROJECT → FIXES → TODO → code → test → DONE
- Branching: feature branches, never commit to main
- Testing: pytest / cargo test / vitest
- Deploy: rsync to VPS / cargo publish / npm publish

## Patterns
- pattern-name: short description of recurring pattern in this project

## Current
- phase: 25
- id: content-expansion
- status: development

## History
- phase 1–16, id: core, title: "Core functionality" — completed 2026-01-10
- phase 17–20, id: ui, title: "UI layer" — completed 2026-02-01
```

## PROJECT Is Single Source of Truth

All project circumstances go here:

| Category | Examples |
|----------|----------|
| Identity | Name, type, purpose, URLs |
| Infrastructure | SSH hosts, servers, paths, IPs |
| Domains | Production URL, dev URL, subdomains |
| Repositories | Git remote, hosting (GitHub/Codeberg) |
| Secrets | Location of API keys, env files (NOT the secrets themselves) |
| Credentials | Username references, auth methods (NOT passwords) |
| Services | External APIs, databases, CDNs |
| Deployment | rsync paths, deploy commands, environments |
| Protection | IP whitelists, basic auth setup, access rules |

**Security:** Document WHERE secrets are, never WHAT they contain.

## Ownership

| File | Owner | AI Action |
|------|-------|-----------|
| PROJECT.md | AI | Writes and maintains — single source of truth |
| PHASES.md | User | AI reads for overview, suggests updates |
| TODO.md | AI | Writes tasks, updates status |
| DONE.md | AI | Appends completed phases |
| ISSUES.md | Both | AI adds discovered issues, user prioritizes |
| FIXES.md | AI | Writes after solving problems |
| RAG.md | AI | Writes discoveries and patterns |
| INSTALL.md | User | AI reads, suggests updates |
| UIUX.md | User | AI reads for GUI work |
| AUTHORS.md | User | AI reads for attribution |
| CHANGELOG.md | Both | AI drafts, user approves on release |
