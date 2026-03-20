---
tags: []
concepts: []
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


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
