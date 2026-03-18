---
tags: [error-handling, thiserror, result, exhaustive-match]
concepts: [rust-error-enum, exhaustive-matching, error-recovery]
requires: [global/error-flow.md, rust/types.md]
feeds: [rust/errors.md]
related: [rust/ownership.md]
keywords: [AppError, thiserror, Result, match, exhaustive, Transient, UserError, SystemError, Bug, no-wildcard]
layer: 3
---
# Rust Error Handling Implementation

> One `AppError_x` enum per crate boundary — exhaustive match, no wildcard arm

---

Define one `AppError_x` enum per crate boundary. Each variant belongs to exactly one class.

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError_x {
    #[error("Network timeout")]
    NetworkTimeout,                          // Transient

    #[error("Not found: {0}")]
    NotFound(String),                        // UserError

    #[error("Storage unavailable")]
    StorageFull,                             // SystemError

    #[error("Internal error: {context}")]
    Invariant { context: String },           // Bug
}

// Adapter layer — exhaustive match, no _ wildcard
fn handle_result(result: Result<Data, AppError_x>, ui: &mut UIState) {
    match result {
        Ok(data)                               => ui.update(data),
        Err(AppError_x::NetworkTimeout)        => retry_or_degrade(ui),
        Err(AppError_x::NotFound(r))           => ui.show_empty(&r),
        Err(AppError_x::StorageFull)           => ui.show_degraded("Storage unavailable"),
        Err(AppError_x::Invariant { context }) => crash_reporter::report(&context),
        // No _ arm — compiler enforces all variants are handled
    }
}
```

RULE: One `AppError_x` enum per crate — variants map to taxonomy classes (Transient/UserError/SystemError/Bug)
RULE: Exhaustive match at Adapter layer — no `_` wildcard arm
RULE: Each variant carries enough context for the recovery strategy

RESULT: Compiler enforces that every error case has a recovery path — no silent swallowing
REASON: A `_ => {}` arm defeats the entire purpose of typed error handling
