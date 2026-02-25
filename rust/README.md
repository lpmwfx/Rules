---
tags: [rust, overview, rules]
concepts: [rust-rules, overview]
related: [rust/types.md, rust/ownership.md, rust/modules.md, rust/errors.md, rust/naming.md, rust/threading.md, rust/nesting.md, rust/gtk.md, rust/verification.md]
layer: 6
---
# Rust Rules

> Modern Rust 2021 — ownership, Result types, Linux/BSD

---

## Target

PLATFORM: Linux (Ubuntu 24.04+), BSD
EDITION: Rust 2021
TOOLCHAIN: stable (latest)
BUILD: Cargo (libraries), Meson (GTK app integration)

## Philosophy

RULE: Modern Rust 2021 idioms — not "all of Rust"
RULE: Pro-Linux/BSD — POSIX first
RULE: Ownership handles memory — no unsafe unless necessary
RULE: Result types for errors — never panic in library code
RULE: Same patterns as Python/JS — flat, explicit, validated

## Files

| File | Topic |
|------|-------|
| [ownership.md](ownership.md) | Ownership, borrowing |
| [threading.md](threading.md) | Async, channels, Arc+Mutex |
| [errors.md](errors.md) | Result, thiserror, anyhow |
| [modules.md](modules.md) | Closed modules, pub(crate) |
| [nesting.md](nesting.md) | Flat code |
| [naming.md](naming.md) | Naming + hex-suffix convention |
| [types.md](types.md) | Newtype, Option, slices |
| [gtk.md](gtk.md) | GTK4 gtk-rs patterns |
| [verification.md](verification.md) | Gating levels (clippy, deny, miri) |
| [quick-ref.md](quick-ref.md) | Quick reference |
