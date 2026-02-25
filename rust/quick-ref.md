---
tags: [rust, quick-ref, reference, summary]
concepts: [reference, summary]
related: [rust/types.md, rust/ownership.md, rust/modules.md, rust/errors.md, rust/verification.md]
layer: 6
---
# Rust Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Edition | Rust 2021, stable toolchain |
| Platform | Linux/BSD, POSIX first |
| Memory | Owned types default, `&T` for borrows, `Rc/Arc` documented |
| Threads | tokio async, mpsc channels, `Arc<Mutex<T>>` |
| Errors | `Result<T,E>`, thiserror (libs), anyhow (CLI only) |
| Modules | One per file, `pub(crate)`, max 300 LOC |
| Nesting | Max 3 levels, early returns, `?` operator |
| Naming | Hex-suffix for pub items, lifecycle names, `is_` booleans |
| Types | Newtype, `Option<T>`, `&str`/`String`, `&[T]`/`Vec<T>` |
| GTK4 | `glib::clone!`, composite templates, weak refs |
| Verification | Level 0 (local) → Level 1 (merge) → Level 2 (release) |
| BANNED | `unwrap()` in libs, `panic!()`, `Box<dyn Error>`, deep nesting |

## Contract

This ruleset is:
- Binding for humans
- Binding for AI agents
- Not subject to "interpretation"

Rule violations → output rejection.
