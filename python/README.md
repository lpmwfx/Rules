---
tags: []
concepts: [python-rules]
related: [python/types.md, python/structure.md, python/naming.md, python/ack-pattern.md, python/nesting.md, python/testing.md, python/dependencies.md, python/distribution.md, global/module-tree.md]
layer: 6
---
# Python Rules

> Type-safe, flat, tested Python — 3.11+

---

## Philosophy

RULE: One module per file — nesting = package of files, not nested classes inside one file
RULE: Stateless functions — all app state passed in as arguments or held in a central dataclass; functions transform, never store
RULE: Encapsulate behind `__all__` — nothing public unless explicitly exported

See: [global/module-tree.md](../global/module-tree.md)

## Files

| File | Topic |
|------|-------|
| [types.md](types.md) | Type safety (future annotations, unions) |
| [structure.md](structure.md) | File/module structure, pyproject.toml |
| [nesting.md](nesting.md) | Flat code, max 3 levels, early returns |
| [ack-pattern.md](ack-pattern.md) | ACK return pattern |
| [naming.md](naming.md) | Naming conventions |
| [testing.md](testing.md) | TDD, real DBs, no mocks |
| [dependencies.md](dependencies.md) | Preferred libs + linting config |
| [quick-ref.md](quick-ref.md) | Quick reference table |
