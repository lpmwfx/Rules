---
tags: [validation, boundaries, runtime-checking]
concepts: [runtime-checking, boundaries, validation]
keywords: [validate, input, boundary, schema, check, sanitize]
feeds: [python/types.md, js/validation.md, js/safety.md, slint/validation.md]
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

## Static Rule Scanner

RULE: Install rulestools in every project — scan on every commit, watch on every edit
RULE: Fix all errors before committing — warnings inform, errors block

rulestools enforces these rules statically across all supported languages.
Install once per project:

```bash
rulestools setup <project-path>   # detect languages + VSCode task + pre-commit hook
rulestools scan  <project-path>   # one-shot scan, writes proj/ISSUES
```

The scanner writes violations to `proj/ISSUES`. Each violation carries a rule ID
that maps back to this rules set via the MCP server:

```
rust/errors/no-unwrap  →  mcp__rules__get_rule(file="rust/errors.md")
```

AI assistants fixing issues should read `proj/RULES-MCP.md` for the full lookup workflow.
