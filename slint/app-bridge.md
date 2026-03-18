---
tags: [app-bridge, callbacks, event-routing, global]
concepts: [centralised-event-routing, app-bridge-global]
requires: [slint/globals.md, slint/component-model.md]
related: [slint/rust-bridge.md, global/adapter-layer.md]
keywords: [AppBridge, callback, collection-selected, item-selected, save-requested, delete-confirmed, on_collection_selected, Adapter, event-routing, delegate]
layer: 3
---
# Slint AppBridge — Centralised Event Routing

> Components delegate to AppBridge instead of exposing callbacks up the tree

---

`AppBridge` is a global that centralises all component callbacks in one place.
Components delegate to `AppBridge` instead of exposing callbacks up the tree.

```slint
// ui/globals/app-bridge.slint
export global AppBridge {
    callback collection-selected(string);   // collection id
    callback item-selected(string);         // item id
    callback save-requested(string);        // serialized payload
    callback delete-confirmed(string);      // item id
}

// In a component — delegate immediately, no logic:
Button {
    clicked => { AppBridge.save-requested(root.payload); }
}
```

```rust
// Adapter::init — register all AppBridge handlers in one place
let bridge = ui.global::<AppBridge>();

let ui_weak = ui.as_weak();
bridge.on_collection_selected(move |id| {
    if let Some(ui) = ui_weak.upgrade() {
        let items = core.load_items(id.as_str());
        ui.set_items(make_model(&items));
    }
});
```

RULE: `AppBridge` handlers are registered in `Adapter::init()` — same place as direct `ui.on_*()` handlers
RULE: Components delegate to `AppBridge` with a single call — no conditions, no logic in the callback body
RULE: All routing decisions live in the Adapter's `AppBridge` handlers, not in `.slint` files

RESULT: All event routing is in one Rust file — adding a new event means one handler, not a chain of re-exports
REASON: `AppBridge` eliminates callback bubbling through the component tree
