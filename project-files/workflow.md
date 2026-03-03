---
tags: [workflow, session, relations, publishing]
concepts: [workflow, file-relations, publishing-flow]
requires: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md]
related: [global/startup.md, project-files/install-file.md, project-files/project-process.md]
keywords: [dones, ownership, dual-repo, proj]
layer: 2
---
# Workflow, Relations, and Publishing

> How files connect, who owns what, and how work flows from start to publish

---

> Session workflow, state transitions, and DONES mechanics → see [project-process.md](project-process.md)

## File Relations

```
proj/PROJECT Goal (the vision)
  │
  ├── proj/PHASES milestone (each serves the Goal)
  │     └── PHASES.md delivers (what gets built)
  │           └── proj/TODO tasks (current work)
  │                 └── TODO.md pass (proves milestone reached)
  │
  ├── proj/ISSUES (problems found during work)
  │     └── proj/FIXES (resolved → Problem/Cause/Solution)
  │
  ├── proj/RAG (knowledge discovered during work)
  │
  └── proj/DONE (completed phases archive)

  proj/INSTALL  ← publishing and setup (references PROJECT.md identity)
  proj/UIUX     ← UI/UX spec for GUI projects (referenced by TODO.md tasks)
  proj/AUTHORS  ← contributors (human + AI)
  proj/CHANGELOG ← user-facing release notes (published to public repo)
```

## Ownership

| File | Owner | Writes | Approves |
|------|-------|--------|----------|
| PROJECT.md | AI | AI maintains | User approves |
| PHASES.md | User | User defines milestones | User owns |
| TODO.md | AI | AI writes tasks + status | User approves scope |
| DONE.md | AI | AI appends | Automatic on phase complete |
| ISSUES.md | Both | AI discovers, user reports | User prioritizes |
| FIXES.md | AI | AI writes after solving | Automatic |
| RAG.md | AI | AI writes discoveries | Automatic |
| INSTALL.md | User | User defines, AI suggests | User owns |
| UIUX.md | User | User defines UI/UX | User owns |
| AUTHORS.md | User | User manages | User owns |
| CHANGELOG.md | Both | AI drafts | User approves on release |

## Publishing Workflow

```
1. Phase complete
   → All TODO.md tasks done
   → All tests pass
   → PHASES.md milestone verified

2. Prepare for publish
   → Update proj/CHANGELOG with user-facing changes
   → Verify proj/INSTALL instructions current
   → Bump version in package metadata

3. Publish to public repo
   → Copy publishable files (see INSTALL.md for what/what not)
   → Verify proj/ not in public repo — never push project files
   → Push to public remote

4. CI/CD
   → Automated tests on public repo
   → Build + publish package

5. Test install
   → Install from public source on clean machine
   → Verify installed identity (not DEV identity)
   → Run smoke tests

6. Verify
   → Installed version matches CHANGELOG.md
   → Identity is correct (paths, names, logging)
   → Basic user flow works
```

## Dual-Repo Pattern

```
~/REPO (private)              Public repo
├── proj/               →    (excluded)
│   ├── PROJECT.md
│   ├── TODO.md
│   └── ...
├── src/                →    ├── src/
├── tests/              →    ├── tests/
├── .env                     ├── README.md
├── doc/project.md           ├── LICENSE
└── dev scripts              ├── CHANGELOG.md
                             └── pyproject.toml
```

RULE: Private repo is source of truth for development
RULE: Public repo is clean, publishable subset
RULE: Never push proj/ to public repo

