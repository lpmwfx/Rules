---
tags: [theming, dark-mode, appearance, pal, adapter, invoke-from-event-loop]
concepts: [slint-dark-mode, pal-appearance-injection]
requires: [uiux/theming.md, slint/globals.md]
related: [slint/themes.md, slint/tokens.md, pal/traits.md]
keywords: [dark-mode, set_dark_mode, pal, appearance, invoke-from-event-loop, Colors-global, watch_appearance, is_dark_mode, live-switch]
layer: 3
---
# Slint Dark-Mode Implementation

> PAL reads OS preference → Adapter injects into token globals → live switching without restart

---

Slint does **not** auto-detect system appearance. The PAL layer reads the OS preference;
the Adapter injects it into the token globals at startup and on change.

See slint/themes.md for multi-theme support (folder structure, theme variants, Effects global).
See slint/globals.md for token global patterns.

```rust
// src/pal/appearance.rs — platform abstraction (one impl per OS)
pub fn is_dark_mode() -> bool { /* check registry / NSAppearance / portal */ }
pub fn watch_appearance(tx: std::sync::mpsc::Sender<bool>) { /* OS signals */ }
```

```rust
// Adapter::init — inject once at startup
ui.global::<Colors>().set_dark_mode(pal::appearance::is_dark_mode());

// Watch for live OS changes — update without restart
let ui_weak = ui.as_weak();
std::thread::spawn(move || {
    let (tx, rx) = std::sync::mpsc::channel();
    pal::appearance::watch_appearance(tx);
    for is_dark in rx {
        let ui_weak = ui_weak.clone();
        slint::invoke_from_event_loop(move || {
            if let Some(ui) = ui_weak.upgrade() {
                ui.global::<Colors>().set_dark_mode(is_dark);
            }
        }).ok();
    }
});
```

RULE: PAL layer reads system preference — Adapter injects into token globals via `set_dark_mode()`
RULE: Live OS change → PAL sends signal → `invoke_from_event_loop` updates globals — no restart
RULE: Only token globals branch on `dark-mode` — components never check it
BANNED: Components reading `dark-mode` directly to pick colors — use token references
BANNED: Hardcoded colors in components

RESULT: OS appearance change updates every Slint component instantly via token globals
REASON: Without PAL → Adapter injection, Slint has no system appearance awareness at all
