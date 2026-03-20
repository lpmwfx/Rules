---
tags: [uiux, menus, kde, linux, slint, rust, headerbar, global-menu]
concepts: [native-menus, kde-hig, global-menu, dbus]
requires: [uiux/menus-slint.md]
related: [uiux/menus-gnome.md, uiux/help-about.md, uiux/keyboard.md]
keywords: [kde, linux, plasma, global-menu, dbus, headerbar, hamburger, slint, rust, about, shortcuts]
layer: 4
---
# KDE Menus — Rust + Slint

> Hamburger menu by default — optional global menubar export via DBus for Plasma

---

VITAL: KDE Plasma supports a global menubar (exported via DBus) but does not require it
RULE: Default to hamburger menu in HeaderBar — same pattern as GNOME
RULE: If exporting to global menu: use `muda` with the `dbus` feature on Linux
RULE: Shortcuts use `Ctrl+?`, Preferences use `Ctrl+,`, Quit uses `Ctrl+Q`
RULE: About is a Slint dialog — same component as GNOME (reuse AboutDialog.slint)
RULE: Shortcuts window is a Slint dialog — same component as GNOME (reuse ShortcutsWindow.slint)
BANNED: Assuming global menu is always present — many KDE users disable it

## KDE Menu Structure

Default (hamburger — works everywhere):
```
┌──────────────────────────────────────────────┐
│  [‹] [›]   MyApp          [+] [Search] [≡]  │
└──────────────────────────────────────────────┘
                                              │
                                 ┌────────────┴───────┐
                                 │ Keyboard Shortcuts  │
                                 │ Preferences         │
                                 │ ─────────────────── │
                                 │ Help                │
                                 │ About MyApp         │
                                 └─────────────────────┘
```

With global menubar enabled in Plasma (optional):
```
File    Edit    View    Help
```

## Slint Implementation (Hamburger — default)

Reuse the same `HeaderBar.slint` and `AboutDialog.slint` from GNOME.
KDE and GNOME share the same Slint-native approach.

```rust
// src/platform/linux.rs — shared for GNOME and KDE
pub fn setup_keyboard_shortcuts(ui: &AppWindow) {
    let ui_weak = ui.as_weak();
    ui.window().on_key_pressed(move |event| {
        use slint::platform::Key;
        match (event.modifiers.control, event.text.as_str()) {
            (true, "/") | (true, "?") => {
                ui_weak.unwrap().invoke_show_shortcuts();
                slint::EventResult::Accept
            }
            _ if event.text == Key::F1.to_string() => {
                ui_weak.unwrap().invoke_show_shortcuts();
                slint::EventResult::Accept
            }
            (true, "q") => {
                slint::quit_event_loop().unwrap();
                slint::EventResult::Accept
            }
            _ => slint::EventResult::Reject,
        }
    });
}
```

## Optional: Global Menu via muda (Plasma only)

If the app targets KDE Plasma specifically and wants to integrate with the global menubar:

```toml
# Cargo.toml
[target.'cfg(target_os = "linux")'.dependencies]
muda = { version = "0.15", features = ["gtk"] }
gtk = "0.18"
```

```rust
// src/platform/kde.rs — only if opting into global menu
#[cfg(target_os = "linux")]
pub fn try_install_global_menu(app_menu: &crate::ui::menu::AppMenu) {
    // muda will attempt DBus export — silently does nothing if no global menu service
    let menu_bar = build_menu_bar(app_menu);
    // Attach to GTK window handle if available
    // Falls back gracefully if Plasma global menu is not running
}
```

RULE: Always fall back to hamburger if global menu DBus service is unavailable
RULE: Never require global menu — treat it as progressive enhancement

## Reuse from GNOME

KDE uses identical Slint components as GNOME:

| Component | File | Reuse |
|-----------|------|-------|
| HeaderBar | `src/ui/shared/HeaderBar.slint` | ✓ same file |
| AboutDialog | `src/ui/shared/AboutDialog.slint` | ✓ same file |
| ShortcutsWindow | `src/ui/shared/ShortcutsWindow.slint` | ✓ same file |
| Keyboard handler | `src/platform/linux.rs` | ✓ same file |

Platform detection for optional global menu:
```rust
fn is_kde_plasma() -> bool {
    std::env::var("XDG_CURRENT_DESKTOP")
        .map(|d| d.to_lowercase().contains("kde"))
        .unwrap_or(false)
}
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
