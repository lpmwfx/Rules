---
tags: [nesting, flat, readability, early-return]
concepts: [code-style, readability]
feeds: [python/nesting.md, cpp/nesting.md, rust/nesting.md]
related: [global/consistency.md]
keywords: [max-3-levels, early-return, extract-helper, flat-code]
layer: 1
---
# Flat Code

> Max 3 nesting levels — early returns, extract helpers

---

VITAL: Flat is better than nested — all languages, no exceptions
RULE: Max 3 nesting levels — extract to helper function if deeper
RULE: Early returns to reduce nesting — guard clauses at top
RULE: Extract helpers for complex logic — name the intent
RULE: If/else on same level, not nested
BANNED: Deep nesting (4+ levels)
