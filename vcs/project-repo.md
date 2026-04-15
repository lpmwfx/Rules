---
tags: [vcs, repo, project-init, forgejo, gitignore, proj]
concepts: [repo-per-project, proj-separation, gitignore-convention]
requires: [project-files/README.md]
related: [project-files/project-file.md, project-files/workflow.md]
keywords: [repo, forgejo, org, gitignore, proj, vcs, init, create]
layer: 2
---
# VCS: Project Repository

> Every project gets its own repo on Forgejo (git.lpmintra.com) at creation time

---

VITAL: When creating a new project, always create a matching repository on Forgejo via VCS MCP
VITAL: All non-code, non-documentation files live in `proj/` — never in project root
RULE: Ask the user which org to use if not already defined in project context
RULE: Initialize git in the project directory with the Forgejo repo as remote
RULE: Create a `.gitignore` that excludes `proj/` from the repository

## Workflow

### Step 1: Determine organization

If the project context defines an org, use it. Otherwise ask the user:

```
Which Forgejo org should this repo be created in?
(e.g. aigov, lpmwfx, tools)
```

### Step 2: Create repository

Use VCS MCP `create_repo` to create the repo on Forgejo:

```
create_repo(name: "project-name", org: "the-org", description: "Short description")
```

### Step 3: Initialize git locally

```bash
cd /path/to/project
git init
git remote add origin https://git.lpmintra.com/{org}/{repo}.git
```

### Step 4: Create .gitignore

The `.gitignore` must exclude `proj/` and any non-code, non-documentation content:

```gitignore
# Project state — private dev state, not source code
proj/
```

Add language/runtime-specific ignores as needed (node_modules/, .build/, etc.).

### Step 5: Create initial README

Create a `README.md` with project name and short description. Commit and push.

## What lives in proj/

Everything that is NOT source code or code-related documentation:

- Project state files (PROJECT, PHASES, TODO, ISSUES, FIXES, etc.)
- Design documents and planning files
- MCP-specific specs and integration plans
- Workspace files and editor configs
- Rule observations and RAG notes

See `project-files/README.md` for the full proj/ specification.

## What lives in the repo (tracked by git)

- Source code (`src/`, `lib/`, etc.)
- Tests (`tests/`, `__tests__/`, etc.)
- Code-related documentation (README.md, API docs, inline docs)
- Configuration files (tsconfig.json, package.json, Cargo.toml, etc.)
- Build and deploy configs (Dockerfile, docker-compose, CI configs)
- `.gitignore`
- `LICENSE`

## FAQ

**Q: Why a separate repo per project?**

A: Each project has its own lifecycle, history, and access control. Monorepos are fine for shared code, but project identity lives in its own repo.

**Q: Why exclude proj/ from git?**

A: `proj/` is private dev state — task tracking, phase planning, issue queues. It changes constantly and is not part of the deliverable. It may contain sensitive planning details not suitable for the repo.

**Q: What if the project already exists without a repo?**

A: Create the repo retroactively. Same workflow — create on Forgejo, init git, add remote, push existing code.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
