---
tags: [threading, async, event-loop, invoke-from-event-loop, spawn-local]
concepts: [thread-safety, event-loop, async-ui-update]
requires: [slint/rust-bridge.md, rust/threading.md]
related: [global/adapter-layer.md]
keywords: [invoke-from-event-loop, spawn-local, as-weak, upgrade, Weak, tokio, background-thread, event-loop-thread, safe-update]
layer: 4
---
# Slint Threading

> All Slint API calls on the event-loop thread — use `invoke_from_event_loop` to cross

---

VITAL: Slint is single-threaded — ALL `set_*()`, `on_*()`, `invoke_*()` calls must be on the event-loop thread
VITAL: `slint::invoke_from_event_loop()` is the ONLY safe path for background thread → UI updates
RULE: Store `ui.as_weak()` before spawning any thread or async task — never move the live `AppWindow`
RULE: Call `.upgrade()` inside `invoke_from_event_loop` — by the time the closure runs, the window may be gone
RULE: Prefer `slint::spawn_local()` for async work that needs no external thread — it runs on the event-loop thread
BANNED: `ui.set_*()` called directly from `std::thread::spawn` or a tokio task — Slint panics
BANNED: Storing a strong `AppWindow` reference inside a callback closure — causes memory leaks

## Background thread → UI update

```rust
// Pattern: weak ref captured before spawn, upgrade inside invoke_from_event_loop
let ui_weak = ui.as_weak();

std::thread::spawn(move || {
    let result = do_expensive_work();    // runs off the event-loop thread

    slint::invoke_from_event_loop(move || {
        if let Some(ui) = ui_weak.upgrade() {
            ui.set_result(result.into());
            ui.set_is_loading(false);
        }
    }).ok();
});
```

## Tokio async task → UI update

```rust
let ui_weak = ui.as_weak();

tokio::spawn(async move {
    let data = fetch_remote_data().await;    // async, off event-loop thread

    slint::invoke_from_event_loop(move || {
        if let Some(ui) = ui_weak.upgrade() {
            ui.set_items(make_model(&data));
        }
    }).ok();
});
```

## Async work on the event-loop thread — prefer `spawn_local`

When the async work does not block a thread (pure async I/O), run it on the event-loop thread directly.
No `invoke_from_event_loop` needed — the closure already runs on the correct thread.

```rust
let ui_weak = ui.as_weak();

slint::spawn_local(async move {
    let data = fetch_data().await;    // async, but on event-loop thread

    if let Some(ui) = ui_weak.upgrade() {
        ui.set_items(make_model(&data));
    }
}).unwrap();
```

RULE: Use `spawn_local` for async tasks that only do async I/O — no thread blocking
RULE: Use `invoke_from_event_loop` when work genuinely runs on a separate thread (CPU-bound, tokio::spawn)

## Slint-interpreter and dynamic UI

When using `slint-interpreter` (for runtime-generated `.slint` content), the same threading rules apply:
the interpreter's `ComponentInstance` is also bound to the event-loop thread.

```rust
// Update a dynamic Slint instance from a background result
let instance_weak = instance.as_weak();
slint::invoke_from_event_loop(move || {
    if let Some(inst) = instance_weak.upgrade() {
        inst.set_property("title", "Updated".into()).ok();
    }
}).ok();
```

RESULT: Threading bugs are prevented at the call site — the pattern is always the same weak+invoke pair
REASON: Slint's single-thread guarantee makes rendering deterministic; crossing it safely is one pattern only
