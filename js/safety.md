---
tags: [javascript, safety, runtime, boundaries]
concepts: [runtime-validation, boundaries]
requires: [global/validation.md]
related: [js/validation.md]
layer: 4
---
# JS Safety — Runtime Over Static

> Where JavaScript beats TypeScript — runtime truth at boundaries

---

## Core Idea

TypeScript types disappear at runtime. JS becomes stronger than TS where you move truth to runtime:

- You validate and transform **real** data
- You enforce architecture/style/security with lints
- You test contracts systematically

## 1. Runtime Validation as Source of Truth (Zod/schema)

RULE: All untrusted input must go through schema at boundary

### Boundaries

- HTTP / API responses
- DB rows
- YAML/TOML/JSON configs
- CLI input
- IPC between UI ↔ backend

### Pattern

- `parse()` at boundary
- Internal functions assume "safe" data
- Transformations (defaults, coerce) happen in one place

## 2. JSDoc + @ts-check in Pure JS

RULE: JS is source of truth; types are metadata

Good for: small tools, validators, scripts, plugins, mixed-language repos.

## 3. ESLint as Policy Engine (Architecture + Security)

RULE: Lint rules > type rules for architecture

### Policy Categories

- No hardcode: colors/sizes/paths
- Layer rules: core must not import UI
- Async discipline
- Naming conventions
- Forbid dangerous APIs (`eval`, implicit coercion)

## 4. Contract Tests at Boundaries

RULE: If it can go wrong at runtime, it needs a test or schema-guard

- Schema tests: fixtures that must fail
- Golden files: for TOML/YAML/UI-token outputs
- Property-based: push "weird cases" through parser

## 5. Less Friction → More Rules Followed

RULE: Rules that are consistently used beat perfect rules that are bypassed

## Three-Layer Architecture (Cross-Platform)

```
ui/       → GJS widgets / QML views
adapter/  → UI ↔ core gateway, event-bus, IPC, bindings
core/     → business logic, state-machine, validators, storage
```

RULE: UI must never talk to core directly without adapter
RULE: All untrusted input must `parse()` at boundary
RULE: Schemas live in `core/schemas/` (shared across platforms)

## Boundary Ruleset

- [ ] All input must `parse()` at boundary
- [ ] No function accepts raw network/db/config data without schema
- [ ] No hardcoded colors/sizes in UI/SVG
- [ ] `core/` must not import `ui/`
- [ ] `ui/` must only talk to `adapter/`
- [ ] All promises handled
- [ ] IPC calls have timeouts + typed errors
