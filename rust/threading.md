# Threading

> Async, channels, Arc+Mutex — prefer message passing

---

RULE: tokio for async I/O (if needed)
RULE: `std::sync::mpsc` or crossbeam for channels
RULE: `Arc<Mutex<T>>` for shared mutable state
RULE: Prefer message passing over shared state
RULE: All spawned tasks must be stoppable deterministically

```rust
// GOOD: Channel-based communication
let (tx, rx) = std::sync::mpsc::channel();
std::thread::spawn(move || {
    tx.send(result).unwrap();
});

// GOOD: GTK + glib main context
glib::MainContext::default().spawn_local(async move {
    // async work
});
```
