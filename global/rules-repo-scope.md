---
tags: [scope, ai-behavior, rules-repo, infrastructure, mandatory]
concepts: [ai-constraints, scope-control]
requires: [global/know-before-change.md, global/read-before-write.md]
related: [global/startup.md, global/initialize.md]
keywords: [rules repo, scope, infrastructure, install, editable, pip, mcp server, architecture change]
layer: 1
---
# Rules Repo — AI Scope Constraints

> When working in D:/REPO/Rules — content only, never infrastructure

---

VITAL: This repo has two distinct concerns — CONTENT and INFRASTRUCTURE
VITAL: AI is authorized to change CONTENT — AI is NOT authorized to change INFRASTRUCTURE
VITAL: If unsure which category an action falls into — ASK before acting

---

## CONTENT — AI may change freely

- Rule `.md` files in `Rules/<category>/`
- Frontmatter (tags, concepts, keywords, edges)
- `register.jsonl` — only via `python tools/build-register.py`, never by hand

## INFRASTRUCTURE — AI must NOT change without explicit instruction

BANNED: Changing how packages are installed (`pip install -e .` vs `pip install .`)
BANNED: Changing the install target (site-packages location, user vs system)
BANNED: Modifying `pyproject.toml` package structure or entry points
BANNED: Modifying MCP server startup, transport, or configuration
BANNED: Changing `claude_desktop_config.json` MCP server definitions
BANNED: Refactoring scanner architecture (how languages are loaded, dispatched)
BANNED: Adding new dependencies to `pyproject.toml` without explicit request
BANNED: "Improving" the flow because it seems suboptimal — the flow is intentional

## The install flow is fixed

```
Edit .md → build-register.py → git push → MCP re-pulls (TTL 1h)
Edit .py  → pip install .     → restart Claude Code
```

This flow is INTENTIONAL. Do not introduce editable installs, symlinks,
or other mechanisms to make updates "faster" or "more convenient".

## When asked to "fix" something in this repo

1. Identify: is the fix in CONTENT or INFRASTRUCTURE?
2. CONTENT: proceed
3. INFRASTRUCTURE: explain what you found and ask for explicit authorization
4. Never fix infrastructure by changing adjacent infrastructure — find root cause

## Why this rule exists

An AI introduced `pip install -e .` (editable install) to avoid reinstalling
after changes. This created a dependency on `D:/REPO/` being present at runtime,
broke the site-packages isolation, and required manual cleanup across three repos.
The "improvement" caused more damage than the original inconvenience.

PRINCIPLE: Stability over cleverness — the boring solution that always works
beats the elegant solution that sometimes breaks.
