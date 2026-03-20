---
tags: [uiux, dsl, rust, declarative]
concepts: [slint-overview, component-model, rust-slint-bridge]
feeds: [slint/component-model.md, slint/rust-bridge.md, slint/globals.md, slint/threading.md, slint/validation.md]
related: [uiux/tokens.md, uiux/menus-slint.md, uiux/theming.md, uiux/state-flow.md, global/adapter-layer.md, global/topology.md]
keywords: [dsl, rust, declarative-ui, cross-platform, desktop, embedded]
layer: 1
---
# Slint

> Declarative UI DSL for Rust — `.slint` is the `_ui` layer, Adapter owns the bridge

---

VITAL: `.slint` maps 1:1 to the `_ui` topology layer — no logic, no domain types, no state
RULE: Slint is the UI toolkit for cross-platform desktop (Windows, macOS, Linux) and embedded
RULE: Native menus are handled by `muda` alongside Slint — see uiux/menus-slint.md

## Topic files

| File | What it defines |
|------|-----------------|
| [component-model.md](component-model.md) | Property direction, naming, exports, build setup |
| [responsive-layout.md](responsive-layout.md) | AppWindow owns all sizes; modules use preferred-width + stretch |
| [rust-bridge.md](rust-bridge.md) | Adapter-owned `on_*` / `set_*` API, type mapping |
| [globals.md](globals.md) | `Colors`, `Spacing`, `Strings`, `AppBridge` globals |
| [threading.md](threading.md) | `invoke_from_event_loop`, `spawn_local`, `as_weak` |
| [validation.md](validation.md) | Token enforcement and callback discipline scanners |

## Five invariants

1. **`in property`** — Adapter pushes state in; component renders it
2. **`callback`** — component fires event; Adapter registers handler with `on_*()`
3. **Token globals** — all literal values live in `Colors`, `Spacing`, `Type` globals
4. **No logic in .slint** — callback body = one delegation call, nothing else
5. **Mother–child layout** — `AppWindow` owns all sizes and breakpoints; modules use `preferred-width: 100%` and stretch factors


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
