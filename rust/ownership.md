---
tags: [rust, ownership, borrowing, lifetimes]
concepts: [memory-management, borrowing, ownership]
requires: [rust/types.md]
related: [cpp/memory.md]
keywords: [borrow, lifetime, clone, arc]
layer: 3
---
# Memory Management

> Ownership and borrowing — Rust's core model

---

RULE: Owned types as DEFAULT — `String`, `Vec`, `Box`
RULE: References (`&T`, `&mut T`) for borrowing
RULE: `Rc/Arc` only when explicitly needed (document why)
RULE: NEVER `unsafe` without comment explaining why
RULE: Clone only when necessary (prefer borrows)

```rust
// GOOD: Clear ownership
fn process(data: String) -> Result<Output, Error> { ... }

// GOOD: Borrowing for reads
fn validate(data: &str) -> bool { ... }

// GOOD: Explicit shared ownership (with reason)
// Shared across multiple GTK widget callbacks
let state = Rc::new(RefCell::new(AppState::new()));
```

## Concurrency and Unsafe

RULE: `unsafe` REQUIRES:
  - Invariant comment
  - Reference to doc/issue
  - Test that attempts to break the invariant
RULE: No fire-and-forget async tasks
RULE: All spawned tasks must be stoppable deterministically
