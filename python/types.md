---
tags: [python, types, annotations, dataclass, mypy]
concepts: [type-safety, type-checking]
requires: [global/validation.md]
feeds: [python/testing.md]
related: [rust/types.md, cpp/types.md]
keywords: [future-annotations, dataclass, typed-dict, mypy, pyright]
layer: 3
---
# Type Safety

> from __future__ import annotations in every file

---

RULE: `from __future__ import annotations` — ALL files, first import
RULE: Modern unions: `str | None` (NEVER `Optional[str]`)
RULE: `@dataclass` for data structures with properties
RULE: `TypedDict` for dict-based typed structures
RULE: Strict mode: mypy + pyright both enabled

## Docstrings (Google Style)

```python
"""
Brief description.

Args:
    param: Description

Returns:
    Description of return value
"""
```

## Context Managers

RULE: Use `@contextmanager` for resource management
RULE: Explicit enter/exit, used with `with` statement
RULE: Database connections always via context manager
