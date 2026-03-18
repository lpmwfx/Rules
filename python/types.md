---
tags: [types, annotations, dataclass, mypy]
concepts: [type-safety, type-checking]
requires: [global/validation.md]
feeds: [python/validation.md, python/testing.md]
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

BANNED: `Optional[T]` — write `T | None` (requires `from __future__ import annotations`)
BANNED: Bare `except:` without exception type — always catch specific exceptions
BANNED: Mutable default arguments (`def f(x=[])`) — use `None` and assign inside body
BANNED: `global` keyword — use dependency injection or return values instead
BANNED: `print()` in library/application code — use `logging` or `structlog`

## Exemption: tools/ directory

Files in `tools/` at the project root are build scripts and CLI tools — not library code.
`print()` is allowed in `tools/` files. All other rules still apply.

RULE: `tools/` is the only allowed location for build scripts and one-off CLI tools
BANNED: Build scripts or print-based CLI scripts anywhere outside `tools/`
