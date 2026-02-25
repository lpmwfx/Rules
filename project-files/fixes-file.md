---
tags: [fixes, problem-solution, ai-memory]
concepts: [problem-solving, ai-memory]
requires: [project-files/issues-file.md]
related: [project-files/rag-file.md, global/persistent-memory.md]
layer: 2
---
# FIXES File

> Problem-solution pairs — AI reads before coding, writes after fixing

---

Format: Plain text

```
# FIXES

## 2026-01-24: Short problem description

**Problem:** What went wrong
**Cause:** Why it happened
**Solution:** How it was fixed

---

## 2026-01-23: Another problem

**Problem:** ...
**Cause:** ...
**Solution:** ...
```

## Rules

RULE: Date + short title for each entry
RULE: Problem → Cause → Solution format
RULE: Newest entries at TOP
RULE: AI MUST check FIXES before coding similar areas
