---
tags: [modules, crate, visibility]
concepts: [encapsulation, architecture]
requires: [global/consistency.md, global/module-tree.md]
keywords: [mod, pub, crate, workspace]
layer: 3
---
# Module Structure

> One module per file — pub(crate) for internal, pub for external

---

RULE: One module per file (`mod.rs` only for re-exports)
RULE: `pub(crate)` for internal APIs
RULE: `pub` for public APIs only
RULE: No circular dependencies
RULE: Max ~200 LOC per file (see global/module-tree.md — Rust's density allows up to ~300 for complex trait implementations)
RULE: Max ~10 pub items per module
RULE: No `utils.rs`, `helpers.rs`, `common.rs` without explicit domain

## Layout

```
src/
├── lib.rs           # Crate root, pub exports only
├── config.rs        # Config module
├── terminal/
│   ├── mod.rs       # Re-exports only
│   ├── session.rs   # Terminal session
│   └── pty.rs       # PTY handling
└── main.rs          # Binary entry point
```

Split if:
- More than one concept explained in module top-doc
- Multiple lifecycles mixed (init, runtime, shutdown)

## Performance Observation

NOTE: Encapsulated modules = faster code
NOTE: Rust compiler optimizes better with clear module boundaries
NOTE: Better inlining decisions and dead code elimination
NOTE: Cache efficiency: smaller, focused modules = better instruction cache
NOTE: Cargo can compile independent modules in parallel
NOTE: LTO works better with clean boundaries
