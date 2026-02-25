---
tags: [validation, boundaries, runtime-checking]
concepts: [runtime-checking, boundaries, validation]
feeds: [python/types.md, js/validation.md, js/safety.md]
layer: 1
---
# Validation Over Abstraction

> Never hide complexity behind abstractions — expose and check

---

VITAL: Never hide complexity behind abstractions
VITAL: Use validation layers that EXPOSE and CHECK
VITAL: Each layer catches what the previous missed

## Validation Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Design-time | Type annotations (JSDoc, type hints) | Catch type mismatches |
| Build-time | Type checkers (tsc, mypy, pyright) | Verify types statically |
| Lint-time | Code quality (ESLint strict, ruff) | Enforce patterns |
| Run-time | Data validation (Zod, beartype, pydantic) | Validate boundaries |

PRINCIPLE: Abstraction says "trust me" — Validation says "verify"
REASON: AI can't debug hidden magic — AI CAN fix explicit errors
