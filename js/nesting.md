---
tags: [nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md]
keywords: [nesting, flat, early-return, guard-clause]
layer: 4
---
# Flat Code — JavaScript/TypeScript

> See [global/nesting.md](../global/nesting.md) for shared rules

---

RULE: Max 3 levels of nesting — use early returns to flatten
RULE: Guard clauses at top of function: `if (!valid) return;`
RULE: Prefer `.map()` / `.filter()` over nested loops
RULE: Async: use `await` with early return, not nested `.then()` chains
RULE: Ternary only for simple expressions — never nested ternaries

BANNED: Nested `if-else` beyond 3 levels
BANNED: Callback hell — use async/await
BANNED: Nested ternary operators
BANNED: `else` after `return` / `throw` / `continue`
