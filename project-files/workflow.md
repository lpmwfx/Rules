---
tags: [workflow, session, relations, publishing]
concepts: [workflow, file-relations, publishing-flow]
requires: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md]
related: [global/startup.md, project-files/install-file.md]
keywords: [dones, ownership, dual-repo]
layer: 2
---
# Workflow, Relations, and Publishing

> How files connect, who owns what, and how work flows from start to publish

---

## Session Workflow

```
1. Start session
   → Read PROJECT (understand state)
   → Read PHASES (know the milestone)
   → Read TODO (know current tasks)
   → Check FIXES (avoid past mistakes)

2. Work on task
   → Update TODO task status to in_progress
   → Code, test, verify

3. Complete task
   → Update TODO task status to done
   → If problem solved → add to FIXES
   → If learned something → add to RAG

4. Complete phase (all tasks done)
   → Move TODO content to DONE
   → Move PHASES entry below DONES
   → Update PROJECT (done: + new phase:)
   → Create new TODO for next phase
```

## File Relations

```
PROJECT Goal (the vision)
  │
  ├── PHASES milestone (each serves the Goal)
  │     └── PHASES delivers (what gets built)
  │           └── TODO tasks (current work)
  │                 └── TODO pass (proves milestone reached)
  │
  ├── ISSUES (problems found during work)
  │     └── FIXES (resolved issues → Problem/Cause/Solution)
  │
  ├── RAG (knowledge discovered during work)
  │
  └── DONE (completed phases archive)

  INSTALL ← publishing and setup (references PROJECT identity)
  UIUX ← UI/UX spec for GUI projects (referenced by TODO tasks)
  AUTHORS ← contributors (human + AI)
  CHANGELOG ← user-facing release notes
```

## Ownership

| File | Owner | Writes | Approves |
|------|-------|--------|----------|
| PROJECT | AI | AI maintains | User approves |
| PHASES | User | User defines milestones | User owns |
| TODO | AI | AI writes tasks + status | User approves scope |
| DONE | AI | AI appends | Automatic on phase complete |
| ISSUES | Both | AI discovers, user reports | User prioritizes |
| FIXES | AI | AI writes after solving | Automatic |
| RAG | AI | AI writes discoveries | Automatic |
| INSTALL | User | User defines, AI suggests | User owns |
| UIUX | User | User defines UI/UX | User owns |
| AUTHORS | User | User manages | User owns |
| CHANGELOG | Both | AI drafts | User approves on release |

## DONES Mechanics

Three files use the `# --- DONES ---` separator:

| File | Above DONES | Below DONES |
|------|-------------|-------------|
| TODO | pending, in_progress | done |
| ISSUES | open, committed | resolved |
| PHASES | planned, active, blocked | done |

RULE: Items move DOWN across DONES — never back up
RULE: Moving below DONES means evaluated and closed

## Publishing Workflow

```
1. Phase complete
   → All TODO tasks done
   → All tests pass
   → PHASES milestone verified

2. Prepare for publish
   → Update CHANGELOG with user-facing changes
   → Verify INSTALL instructions current
   → Bump version in package metadata

3. Publish to public repo
   → Copy publishable files (see INSTALL for what/what not)
   → Verify no secrets, no project files in public
   → Push to public remote

4. CI/CD
   → Automated tests on public repo
   → Build + publish package

5. Test install
   → Install from public source on clean machine
   → Verify installed identity (not DEV identity)
   → Run smoke tests

6. Verify
   → Installed version matches CHANGELOG
   → Identity is correct (paths, names, logging)
   → Basic user flow works
```

## Dual-Repo Pattern

```
~/REPO (private)              Public repo
├── PROJECT, TODO, etc   →    ├── src/
├── src/                 →    ├── tests/
├── tests/               →    ├── README.md
├── .env                      ├── LICENSE
├── doc/project.md            ├── CHANGELOG
└── dev scripts               └── pyproject.toml
```

RULE: Private repo is source of truth for development
RULE: Public repo is clean, publishable subset
RULE: Never push project files (PROJECT, TODO, FIXES, etc) to public

## Validation

AI should verify at session start:

```
TODO.phase == PROJECT.phase      # Must match
TODO.id == PROJECT.id            # Must match
TODO.id in PHASES (active)       # Must be the active phase
All done tasks → ready for DONE  # Phase complete check
```

RULE: If validation fails → STOP and ask user
