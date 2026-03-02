---
tags: [rust, overview, rules]
concepts: [rust-rules, overview]
related: [rust/types.md, rust/ownership.md, rust/modules.md, rust/errors.md, rust/naming.md, rust/threading.md, rust/nesting.md, rust/verification.md, uiux/gtk.md, uiux/menus-slint.md]
layer: 6
---
# Rust Rules

> Modern Rust 2021 — ownership, Result types, Linux/BSD

---

## Target

PLATFORM: Linux (Ubuntu 24.04+), BSD
EDITION: Rust 2021
TOOLCHAIN: stable (latest)
BUILD: Cargo

## Philosophy

RULE: Modern Rust 2021 idioms — not "all of Rust"
RULE: Pro-Linux/BSD — POSIX first
RULE: Ownership handles memory — no unsafe unless necessary
RULE: Result types for errors — never panic in library code
RULE: Same patterns as Python/JS — flat, explicit, validated
RULE: One module per file — nesting = folder of files, not nested mod blocks
RULE: Stateless logic — all app state in a central `AppState_sta` type; functions transform, never store state
RULE: Encapsulate behind `pub(crate)` — nothing public unless needed at crate boundary

See: [global/module-tree.md](../global/module-tree.md) | [uiux/state-flow.md](../uiux/state-flow.md)

## Files

| File | Topic |
|------|-------|
| [ownership.md](ownership.md) | Ownership, borrowing |
| [threading.md](threading.md) | Async, channels, Arc+Mutex |
| [errors.md](errors.md) | Result, thiserror, anyhow |
| [modules.md](modules.md) | Closed modules, pub(crate) |
| [nesting.md](nesting.md) | Flat code |
| [naming.md](naming.md) | Naming + layer-tag convention |
| [types.md](types.md) | Newtype, Option, slices |
| [verification.md](verification.md) | Gating levels (clippy, deny, miri) |
| [quick-ref.md](quick-ref.md) | Quick reference |
