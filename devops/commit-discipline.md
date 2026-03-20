---
tags: [devops, git, commit, workflow, discipline]
concepts: [commit-discipline, micro-commit, wip-commit, staged-files, commit-trigger]
requires: [devops/workflow.md]
related: [personas/aidevops.md]
keywords: [commit, staged, files, wip, checkpoint, max-files, split, check_staged]
layer: 4
---
# Commit Discipline

> One task, one commit. Git history is the audit trail of what works.

---

RULE: Max 10 files per commit — if staged > 10 files, split into logical sub-commits
RULE: Call check_staged() before every git commit to verify file count
RULE: Commit trigger = task complete + tests pass — not "end of session"
RULE: WIP commits use prefix `wip/<phase>:` — valid for mid-task checkpoints that compile

BANNED: Committing everything at once after a long session — split by logical unit first
BANNED: Skipping check_staged() before git commit

## When to Commit

Commit immediately when:
- A single TODO task is done and its tests pass
- A logical sub-unit compiles and is independently testable
- You are about to switch context (different file area, different concern)

Do NOT wait for:
- The entire feature to be done
- All tests in the suite to pass
- The human to ask

## WIP Commit Pattern

Use WIP commits to checkpoint mid-task work that compiles but is not yet fully tested:

```
wip/auth-layer: JWT struct and parser compile — no tests yet
wip/auth-layer: session store added — unit tests pass
auth-layer/jwt-handling: full JWT flow — integration tests pass  ← clean commit
```

WIP commits are squashable. Use `git rebase -i` to squash before merging to main.

## File Count Enforcement

Before every commit, call `check_staged()` — the MCP tool returns staged file count.

If > 10 files staged, split by topic area:

```bash
git add src/auth/ && git commit -m "auth-layer/middleware: session middleware"
git add src/api/  && git commit -m "auth-layer/endpoints: login endpoint"
```

The pre-commit hook (`rulestools-mcp staged-check`) blocks oversized commits automatically.
If blocked: split the staged files into logical groups and commit each separately.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
