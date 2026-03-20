---
tags: [ipc, events, adapter, callbacks, decoupling, event-driven]
concepts: [event-adapter, decoupling, adapter-pattern, event-driven-architecture]
requires: [global/topology.md, global/adapter-layer.md]
related: [uiux/state-flow.md, global/mother-tree.md]
keywords: [event, callback, adapter, listener, decoupling, on_save, button, shortcut, mcp, signal]
layer: 3
---
# Event Adapter — Unified Event API

> One adapter file collects all input sources. Logic listens to events, not to input sources.

---

VITAL: The adapter is the ONLY place events are defined and exposed — it is the event API layer
RULE: One listener per event — never duplicated logic across input sources
RULE: Input sources (button, shortcut, MCP) bind to the event, not to each other
RULE: Logic layer is unaware of input source — complete decoupling
RULE: Events named by intention, not by input source: `on_save`, not `on_ctrl_s_pressed`
RULE: One adapter file per module/feature — not one per input source

BANNED: Direct call from button handler to logic function — bypass of adapter
BANNED: Logic that checks which input source triggered it
BANNED: Event names that reference UI elements: `on_save_button_clicked`
BANNED: Duplicating the same action in button handler AND keyboard shortcut handler

---

## Pattern

```
Input sources          Adapter              Logic
─────────────          ───────              ─────
Button.clicked ──┐
                 ├──→ on_save ──→ save_document()
Ctrl+S ──────────┘

MCP.save() ──────────→ on_save ──→ save_document()
```

All three input sources trigger the SAME event. Logic runs ONCE.

## Rust Example

```rust
// src/adapter/events.rs — the event API
pub enum AppEvent {
    Save,
    Undo,
    NewDocument,
    OpenFile(PathBuf),
}

// All input sources emit AppEvent
// Logic listens to AppEvent
// Neither knows about the other
```

## Slint Example

```slint
// Adapter callback — one per event
callback on-save();
callback on-undo();

// Button binds to event
SaveButton { clicked => { root.on-save(); } }

// Keyboard shortcut binds to same event
FocusScope {
    key-pressed(event) => {
        if event.modifiers.control && event.text == "s" {
            root.on-save();
        }
    }
}
```

## Why This Matters

Without this pattern, adding a new input source (e.g., MCP tool, voice command)
requires finding and duplicating logic from existing handlers. With the adapter pattern,
adding a new source = one line connecting it to the existing event.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
