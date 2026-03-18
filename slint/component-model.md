---
tags: [component, property, callback, naming, build, dsl]
concepts: [slint-component-model, property-direction, slint-naming, slint-build]
requires: [global/topology.md, uiux/components.md, uiux/state-flow.md]
feeds: [slint/rust-bridge.md, slint/globals.md, slint/responsive-layout.md]
related: [uiux/tokens.md, uiux/file-structure.md, uiux/mother-child.md]
keywords: [in-property, out-property, in-out, private, callback, kebab-case, export, import, build-rs, slint-build, include-modules, AppWindow, PascalCase]
layer: 2
---
# Slint Component Model

> `in property` = state in, `callback` = event out — each channel has one direction

---

VITAL: All `.slint` identifiers use `kebab-case` — the Rust generated API auto-converts to `snake_case`
VITAL: `.slint` files are UI-only — zero business logic, zero domain types, zero conditions in callbacks
RULE: `in property` for state the Adapter pushes in; `callback` for events the component fires out
RULE: `out property` for values the component computes and exposes (e.g. `pressed`, `has-focus`)
RULE: `private property` (or bare `property`) for internal UI state — hover, focus, animation progress
RULE: Component names are `PascalCase`; all other identifiers are `kebab-case`
RULE: One component per `.slint` file — filename is the component name in kebab-case
RULE: `export` every component used from another file
BANNED: `in-out property` on component interfaces — use `in property` + `callback` instead
BANNED: Logic inside callback bodies — one delegation call only (see validation.md)
BANNED: Literal values in components — use `Colors.accent`, `Spacing.md`, not `#4a90d9`, `16px`

## Property access specifiers

| Specifier | Set by | Read by | Use for |
|-----------|--------|---------|---------|
| `in property` | Outside (Adapter / parent) | Component | State pushed in from Rust |
| `out property` | Component itself | Outside (Rust can read) | Computed/exposed state |
| `in-out property` | Everyone | Everyone | Delegation via `<=>` only — see below |
| `private property` | Component itself | Component | Internal UI state |

```slint
export component ItemCard {
    // State in — Adapter pushes these
    in property <string> title;
    in property <bool>   is-selected;

    // Events out — component fires these, Adapter registers handlers
    callback select-requested();
    callback rename-requested(string);   // callback with argument

    // Component exposes computed state — Rust can read via get_has_focus()
    out property <bool> has-focus <=> focus-scope.has-focus;

    // Internal UI state — invisible to Rust
    private property <bool> hovered: false;
}
```

## Two-way binding `<=>` — the only valid use of `in-out property`

`<=>` delegates an inner element's property to the component's public interface.
This re-exposes an inner property, not an Adapter contract.

```slint
export component SearchBox {
    in-out property <string> text <=> field.text;  // delegates TextField's text

    TextField { id: field; }
}
```

RULE: `<=>` is the only reason to write `in-out property`
BANNED: `in-out property` without `<=>` to share state directly with the Adapter

## Naming

All `.slint` identifiers compile to snake_case in the generated Rust API:
- property `is-selected` → `set_is_selected()` / `get_is_selected()`
- callback `select-requested` → `on_select_requested()` / `invoke_select_requested()`

## Build setup

```toml
# Cargo.toml
[dependencies]
slint = "1"

[build-dependencies]
slint-build = "1"
```

```rust
// build.rs — compile the entry-point .slint file; all imports followed transitively
fn main() {
    slint_build::compile("ui/app-window.slint").unwrap();
}

// src/main.rs (or src/ui/mod.rs) — pull in all generated types
slint::include_modules!();
```

RULE: `.slint` files live in `ui/` at project root — separate from `src/` Rust source
RULE: `app-window.slint` is the single entry point — `export component AppWindow inherits Window`
RULE: Call `include_modules!()` in the file that creates the `AppWindow`

RESULT: Component interfaces are typed contracts verified at compile time
REASON: One direction per channel — every data flow is explicit and traceable
