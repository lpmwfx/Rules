---
tags: [combo, slint-app, gui, rhai, scripting]
concepts: [quick-ref, project-type]
keywords: [rust, slint, rhai, scripting, gui, desktop]
requires: [quick-ref/rust-slint.md]
layer: 6
binding: true
---
# Quick Reference: Rust + Slint + Rhai (Scriptable GUI App)

> Desktop GUI app with Rhai scripting — extends rust-slint combo with scripting layer.
> For base Rust + Slint rules see [quick-ref/rust-slint.md](rust-slint.md).

---

## Base rules — rust-slint combo

All rules from [quick-ref/rust-slint.md](rust-slint.md) apply in full:
- Global foundation (topology, mother-child, file limits, naming)
- Rust rules (docs, errors, constants, modules, types, threading)
- Slint rules (component model, zero literals, globals, bridge)
- UI/UX rules (state flow, tokens, components)

This file adds the **Rhai scripting layer** on top.

## Rhai — role in the architecture

Rhai is the lightweight scripting engine for runtime behavior that doesn't warrant Rust code.
It sits between Slint (declarative UI) and Rust (compiled logic).

```
Slint (.slint)     → declarative layout + token bindings (no logic)
Rhai (.rhai)       → lightweight runtime behavior (validation, formatting, simple transforms)
Rust (src/)        → compiled business logic, IO, platform, state management
```

### When to use Rhai vs Rust

| Use Rhai for | Use Rust for |
|---|---|
| Input validation rules | Business logic |
| Display formatting | State management |
| Simple conditional visibility | IO / network / filesystem |
| User-configurable behavior | Performance-critical code |
| Rapid prototyping of logic | Anything needing type safety |

### Rhai rules

| Rule | Key point |
|------|-----------|
| Scope | Rhai handles presentation logic only — never business logic |
| State | Rhai functions are stateless transforms — no mutable globals |
| Bridge | Rhai ↔ Rust via registered functions. Rhai never calls IO directly |
| Errors | Rhai errors propagate to Rust Adapter — never silently swallowed |
| File limits | Rhai scripts: 150 lines max. Split by concern |
| Naming | `snake_case` for functions. Files match their concern: `validate_input.rhai` |
| Testing | Rhai scripts tested from Rust: call engine, assert result |
| No hardcoding | Config values come from Rust via registered constants |

### Rhai file structure

```
scripts/
├── validation/          ← input validation rules
│   ├── mod.rhai         ← re-exports
│   └── email.rhai       ← one concern per file
├── formatting/          ← display formatting
│   └── currency.rhai
└── transforms/          ← data transforms
    └── filter.rhai
```

### Rhai ↔ Rust bridge

```rust
/// Register Rhai functions in Adapter — same pattern as Slint bridge.
fn register_rhai(engine: &mut Engine) {
    engine.register_fn("validate_email", validate_email_core);
    engine.register_fn("format_currency", format_currency_core);
}
```

- Adapter owns the Rhai `Engine` — same as Adapter owns the Slint bridge
- Core functions are registered into Rhai — Rhai calls Rust, not the other way
- Rhai scripts are loaded by Gateway (file IO) — never hardcoded paths

## BANNED (additional to rust-slint)

- Rhai scripts with business logic — belongs in Rust Core
- Rhai calling IO/network directly — must go through registered Rust functions
- Rhai mutable global state — functions are stateless transforms
- Rhai scripts over 150 lines — split by concern
- Hardcoded values in Rhai — use registered constants from Rust
