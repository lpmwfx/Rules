---
tags: [topology, rust, slint, desktop, layers, workspace]
concepts: [rust-topology, layer-mapping-rust, desktop-gui-topology]
requires: [global/topology.md, global/topology-profiles.md]
related: [rust/workspace.md, rust/pal-structure.md, core/design.md, gateway/io.md, slint/README.md]
keywords: [topology, layers, src, mod, workspace, crate, slint, desktop, gui]
layer: 2
---
# Rust Desktop Topology

> 6-layer mapping for Rust + Slint desktop applications

---

| Layer | Tag | Rust mapping |
|---|---|---|
| ui | `_ui` | `ui/` — Slint files (.slint), UI definitions |
| adapter | `_adp` | `src/adapter/` — callbacks, ViewModel structs, Slint↔Rust bridge |
| core | `_core` | `src/core/` — domain logic, pure functions, no IO |
| gateway | `_gtw` | `src/gateway/` — file IO, network, config/state persistence |
| pal | `_pal` | `src/pal/` — OS abstraction (window, filesystem, clipboard, appearance) |
| shared | `_x` | `src/shared/` — AppError_x, Result_x, cross-layer enums |

## Module Ownership

```
src/
├── main.rs              ← system mother — wires all layers
├── adapter/
│   ├── mod.rs           ← adapter mother — owns AdapterState_sta
│   ├── callbacks.rs     ← child — registers UI event handlers
│   └── viewmodel.rs     ← child — Core→UI type mapping
├── core/
│   ├── mod.rs           ← core mother
│   └── domain.rs        ← child — pure business logic
├── gateway/
│   ├── mod.rs           ← gateway mother — owns GatewayState_sta
│   └── persistence.rs   ← child — disk IO
├── pal/
│   ├── mod.rs           ← pal mother — trait definitions
│   └── linux.rs         ← child — Linux implementation
└── shared/
    ├── mod.rs
    └── errors.rs        ← AppError_x
```

RULE: mod.rs is the mother file — children are stateless
RULE: Adapter owns the Slint↔Rust bridge — UI never calls Core directly
RULE: Gateway is the only crate that uses std::fs, std::net, reqwest, etc.
