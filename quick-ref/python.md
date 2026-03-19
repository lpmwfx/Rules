---
tags: [combo, python]
concepts: [quick-ref, project-type]
keywords: [python, pyproject, ruff, mypy]
requires: [global/quick-ref.md, python/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: Python Project

> Python CLI, library, or service. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | Python: 250 lines max. Split into mother/child folder | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## Python-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Imports | `from __future__ import annotations` first | [python/types.md](../python/types.md) |
| Unions | `str \| None` not `Optional[str]` | [python/types.md](../python/types.md) |
| Data | `@dataclass` or `TypedDict` | [python/types.md](../python/types.md) |
| Functions | Max 20 lines, verb_noun naming | [python/naming.md](../python/naming.md) |
| Structure | One module per file, `__init__.py` as mother | [python/structure.md](../python/structure.md) |
| Returns | ACK: `{"success": bool, "data"/"error": ...}` | [python/ack-pattern.md](../python/ack-pattern.md) |
| Testing | Real SQLite, no mocks | [python/testing.md](../python/testing.md) |
| Config | `pyproject.toml` only | [python/structure.md](../python/structure.md) |
| Linting | ruff + mypy + pyright strict | [python/structure.md](../python/structure.md) |
| Deps | httpx, pydantic, beartype | [python/structure.md](../python/structure.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | `ruff check`, `mypy --strict`, `pyright` |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all Python checks |

## BANNED

- Files over 250 lines
- Deep nesting (4+ levels)
- `Optional[str]` — use `str \| None`
- Mutable default arguments
- `utils.py`, `helpers.py`, `common.py`
- Hardcoded values in business logic
- `TODO`/`FIXME`/`HACK` in committed code
- Non-English code, comments, or identifiers

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`
