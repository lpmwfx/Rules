---
tags: [index, navigation, yaml, auto-generated]
concepts: [codebase-index, navigation]
related: [global/startup.md, automation/tool-configs.md]
keywords: [index-yaml, regenerate]
layer: 1
---
# Index System

> Auto-generated index.yaml as single source of truth for codebase navigation

---

VITAL: Projects use auto-generated `index.yaml` as single source of truth
VITAL: Index maps domains → files → sections (no content, only addresses)
VITAL: Each repo has its own index.yaml (submodules not indexed by parent)

## Mandatory Workflow

```
Session start:  python tools/index_generator.py --verify
On commit:      Pre-commit hook runs incremental update (automatic)
In CI:          ./tools/ci_verify_index.sh (full regeneration + verify)
```

## Commands

- Verify: `python tools/index_generator.py --verify`
- Incremental: `python tools/index_generator.py`
- Full: `python tools/index_generator.py --full`

## Index Structure

```yaml
version: 1
generated: '2026-01-26T12:00:00Z'
commit: abc1234
domains:
  shared/theme:
    files:
      Color.kt:
        path: compose-multiplatform/shared/src/theme/Color.kt
        hash: a905a1ce
        lines: 44
        sections: [PsidPrimary, PsidBackground, ...]
```

## Rules

RULE: ALWAYS verify index at session start (step 0 in startup checklist)
RULE: NEVER edit index.yaml manually — always regenerate
RULE: Pre-commit hook updates automatically on commit
RULE: CI fails if index doesn't match regenerated version
RULE: Submodules have their own index.yaml
RULE: Index is deterministic: same input = same output

## Files Per Repo

- `index.yaml` — Generated index
- `tools/index_generator.py` — Generator script
- `tools/ci_verify_index.sh` — CI verification
- `.pre-commit-config.yaml` — Hook: update-index

## Why

- AI can navigate codebase via index lookup
- Hash detects what changed since last session
- Deterministic = verifiable in CI
- No content duplication = minimal size
- Each repo self-contained
