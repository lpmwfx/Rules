---
tags: [kotlin, nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md]
related: [python/nesting.md, rust/nesting.md, js/nesting.md]
keywords: [nesting, flat, early-return, when, guard]
layer: 4
---
# Flat Code — Kotlin

> See [global/nesting.md](../global/nesting.md) for shared rules

---

RULE: Max 3 levels of nesting — use early returns to flatten
RULE: Guard clauses: `if (condition) return` at top of function
RULE: Prefer `when` over nested `if-else` chains
RULE: Use scope functions (`let`, `run`, `also`) to flatten null checks
RULE: `?.let { }` instead of `if (x != null) { }`

BANNED: Nested `if-else` beyond 3 levels
BANNED: Deep `when` nesting — extract to function
BANNED: `else` after `return` / `throw`
