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

VITAL: proj/PROJECT is the only source of truth — not doc/, not README, not any other file
VITAL: If proj/PROJECT contradicts another file, proj/PROJECT wins — update the other file, not PROJECT
RULE: AI reads proj/PROJECT first, every session — before any work
RULE: AI maintains proj/PROJECT — keeps it current after every significant change
RULE: User reviews and approves updates to proj/PROJECT
RULE: AI never changes the `## Goal` section without explicit user approval
BANNED: Storing architectural decisions, stack choices, or project state anywhere except proj/PROJECT

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
| PROJECT | AI | Writes and maintains — the only source of truth |
| PHASES | User | AI reads for overview, suggests updates |
| TODO | AI | Writes tasks, updates status |
| DONE | AI | Appends completed phases |
| ISSUES | Both | AI adds discovered issues, user prioritizes |
| FIXES | AI | Writes after solving problems |
| RAG | AI | Writes discoveries and patterns |
| INSTALL | User | AI reads, suggests updates |
| UIUX | Both | UI/UX source of truth for GUI projects — READ before any UI work, WRITE conventions |
| AUTHORS | User | AI reads for attribution |
| CHANGELOG | Both | AI drafts, user approves on release |

BANNED: `doc/project.md`, `README.md`, or any file outside `proj/` as ongoing architectural reference
RULE: External docs (doc/, README) may exist for humans — AI ignores them in favour of proj/PROJECT

## Project Initialisation — Bootstrapping proj/PROJECT

When `proj/PROJECT` does not yet exist, a source document may be provided (doc/project.md, a brief, a README, etc.).

RULE: Read the source document once — extract goal, stack, structure, patterns, and decisions
RULE: Write everything extracted into proj/PROJECT in the standard format
RULE: Everything that comes up during development is added to proj/PROJECT, not to the source document
RULE: After bootstrapping, the source document is frozen — it is not updated, not referenced again
BANNED: Treating the bootstrap source as a living document alongside proj/PROJECT
BANNED: Splitting truth between the source document and proj/PROJECT at any point after init


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
