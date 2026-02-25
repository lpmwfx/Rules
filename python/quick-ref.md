---
tags: [python, quick-ref, reference, summary]
concepts: [reference, summary]
related: [python/types.md, python/structure.md, python/naming.md, python/ack-pattern.md, python/testing.md]
layer: 6
---
# Python Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Imports | `from __future__ import annotations` first |
| Unions | `str \| None` not `Optional[str]` |
| Data | `@dataclass` or `TypedDict` |
| Functions | Max 20 lines, verb_noun naming |
| Files | Max 200-350 lines |
| Nesting | Max 3 levels, early returns |
| Returns | ACK: `{"success": bool, "data"/"error": ...}` |
| Testing | Real SQLite, no mocks |
| Config | `pyproject.toml` only |
| Linting | ruff + mypy + pyright strict |
| Deps | httpx, pydantic, beartype |
