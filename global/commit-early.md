---
tags: [git, commit, workflow, precommit, incremental]
concepts: [commit-workflow, incremental-commits, precommit]
related: [global/validation.md, global/tech-debt.md, global/startup.md]
keywords: [commit, pre-commit, queue, staged, clean, incremental, as-you-go]
layer: 1
---
# Commit Early — Clean Files First

> Commit every error-free file immediately — never let a clean queue grow

---

RULE: When pre-commit checks pass for a file, commit it immediately
RULE: Never batch clean files waiting for other files to be fixed
RULE: The only uncommitted files should be those that still have errors

PRINCIPLE: Small, frequent commits beat large, delayed commits
REASON: Pre-commit hooks reject files with errors — files that pass are ready now

## Why This Matters

AI sessions produce many file changes. Pre-commit scanners block files with errors.
If you wait until everything is clean, the commit queue grows and becomes hard to review.
Committing clean files as you go keeps the queue small and the diff reviewable.

## Workflow

```
1. Edit file
2. Scanner runs (PostToolUse hook or manual scan)
3. File has zero errors?
   YES → stage and commit immediately
   NO  → fix errors first, then commit
4. Repeat — uncommitted files = only those with remaining errors
```

RULE: Each commit should contain only related changes — do not lump unrelated clean files
RULE: Commit messages describe what changed — not "batch commit" or "fix everything"

## What This Prevents

- Enormous diffs that are impossible to review
- Merge conflicts from holding changes too long
- Lost work when sessions are interrupted
- Confusion about which files are done vs. in progress

BANNED: Holding back clean files to "commit everything at once"
BANNED: Commit messages like "batch update" or "fix all files" — each commit has a purpose
