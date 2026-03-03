---
tags: [slint, validation, tokens, callbacks, properties]
concepts: [validation, design-tokens, type-safety, boundaries]
requires: [global/validation.md, uiux/tokens.md, uiux/state-flow.md]
related: [css/validation.md, js/validation.md]
keywords: [slint, token, callback, property-binding, Theme]
layer: 4
---
# Slint Validation

> Tokens everywhere, callbacks delegate — never hardcode, never inline

---

RULE: All color and size properties must use `Theme.*` tokens — never literals
RULE: Callback bodies must be a single delegation call — no inline logic
RULE: Property types are declared explicitly — Slint's type system is the schema
RULE: Bi-directional bindings (`<=>`) are the data validation boundary

BANNED: Hardcoded hex colors in component properties
BANNED: Hardcoded `px` values on token-governed properties
BANNED: `if`-statements inside callback bodies
BANNED: Multiple `root.x =` mutations in one callback

## Tokens as the Schema

Slint's `Theme` struct is the design-system schema — every visual value
must come from it, just as JSON data must come from a Zod/pydantic schema.

```slint
// BANNED — value is not from the schema:
Rectangle { background: #3a7ff6; }

// CORRECT — value validated against the Theme schema:
Rectangle { background: Theme.color-accent; }
```

## Callbacks as Boundaries

A callback is a data boundary between the UI and the gateway layer.
Like an API boundary, it must validate by delegating immediately.

```slint
// BANNED — inline logic at the boundary:
button-clicked => {
    if root.is-logged-in { root.status = "ok"; }
}

// CORRECT — single delegation, gateway owns all logic:
button-clicked => { AppBridge.handle-button-clicked(); }
```

## Scanner

The `slint/checks/` scanners (rulestools) enforce these rules:
- `slint/checks/tokens.py` — hardcoded colors/sizes (`uiux/tokens.md`)
- `slint/checks/events.py` — callback logic violations (`uiux/state-flow.md`)
- `slint/checks/structure.py` — multiple components per file (`global/module-tree.md`)
