---
tags: [fixes, problem-solution, ai-memory]
concepts: [problem-solving, ai-memory]
requires: [project-files/issues-file.md]
related: [project-files/rag-file.md, global/persistent-memory.md]
layer: 2
---
# FIXES.md File

> Problem-solution pairs — AI reads before coding, writes after fixing

---

## Quick Reference

- **Location:** `proj/FIXES.md`
- **Format:** Markdown — `## YYYY-MM-DD: title` sections, newest first
- **Required:** Always
- **Read by AI:** Before coding any area — to avoid repeating past mistakes

Append-only log of problems and their solutions. Every resolved ISSUES.md
entry must have a corresponding FIXES.md entry. AI reads this before starting
work to avoid repeating known mistakes.

---

RULE: File lives at `proj/FIXES.md`
RULE: AI MUST read FIXES.md before coding — every session
RULE: Every resolved ISSUES.md entry → add entry to FIXES.md
RULE: Newest entries at TOP
RULE: Problem → Cause → Solution format — never skip Cause

## Format

```markdown
# FIXES: project-name

## 2026-01-24: Build script ignores .env

**Problem:** Config parsing fails silently when .env is not loaded.
**Cause:** dotenv was imported but not called before config module loaded.
**Solution:** Call `dotenv.load_dotenv()` at top of entry point, before any imports that read env vars.

---

## 2026-01-20: CSS grid breaks on mobile Safari

**Problem:** Grid items overlap at viewport < 375px on Safari iOS.
**Cause:** Safari does not support `grid-template-columns: subgrid` without prefix.
**Solution:** Replace subgrid with explicit column definitions. See src/styles/grid.css.
```

## Rules

RULE: `Cause:` is mandatory — without it the fix cannot be understood or reused
RULE: `Solution:` must reference the specific file/line changed where relevant
RULE: Short title on `##` heading — enough to find it by scanning
