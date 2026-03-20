---
tags: [uiux, menus, macos, slint, rust, muda, nsmenu]
concepts: [native-menus, macos-hig, nsmenu]
requires: [uiux/menus-slint.md]
related: [uiux/help-about.md, uiux/keyboard.md]
keywords: [macos, nsmenu, muda, menubar, apple-menu, cmd-q, cmd-comma, about, preferences, slint, rust]
layer: 4
---
# macOS Menus — Rust + Slint

> NSMenu via muda — the menubar lives at the top of the screen, always

---

VITAL: macOS apps MUST have a native NSMenu — Slint renders no menubar on macOS
VITAL: The Apple menu (leftmost) is system-managed — add About and Quit there via PredefinedMenuItem
RULE: Preferences uses `Cmd+,` — not `Ctrl+,`
RULE: Quit uses `Cmd+Q` — PredefinedMenuItem::quit() sets this automatically
RULE: Shortcuts window uses `Cmd+?` (Shift+Cmd+/)
RULE: Menu is installed before `ui.run()` — after the window handle is available
BANNED: Ctrl+Q or Ctrl+, on macOS — use Cmd modifiers
BANNED: Custom drawn menubar — NSMenu is mandatory on macOS

## macOS Menu Structure

```
MyApp          Edit          View          Help
─────          ────          ────          ────
About MyApp    Undo ⌘Z       Zoom ⌃⌘F     Keyboard Shortcuts ⌘?
───            Redo ⇧⌘Z      ───           Report Issue
Preferences ⌘, ───           Show Sidebar  ───
───            Cut ⌘X        Fullscreen    Help
Hide MyApp     Copy ⌘C
Hide Others    Paste ⌘V
───            Select All ⌘A
Quit MyApp ⌘Q
```

## Implementation

```rust
// src/platform/macos.rs
use muda::{Menu, Submenu, MenuItem, PredefinedMenuItem, MenuEvent};
use muda::accelerator::{Accelerator, Modifiers, Code};

pub fn install_menu(app_menu: &crate::ui::menu::AppMenu) -> Menu {
    let menu_bar = Menu::new();

    // App menu (leftmost — macOS shows app name automatically)
    let app_submenu = Submenu::new("MyApp", true);
    app_submenu.append(&PredefinedMenuItem::about(
        Some("About MyApp"),
        Some(muda::AboutMetadata {
            name:       Some("MyApp".into()),
            version:    Some(env!("CARGO_PKG_VERSION").into()),
            authors:    Some(vec!["Your Name".into()]),
            website:    Some("https://yoursite.example".into()),
            license:    Some("GPL-3.0".into()),
            copyright:  Some("© 2024–2026 Your Name".into()),
            ..Default::default()
        }),
    )).unwrap();
    app_submenu.append(&PredefinedMenuItem::separator()).unwrap();
    app_submenu.append(&PredefinedMenuItem::services(None)).unwrap();
    app_submenu.append(&PredefinedMenuItem::separator()).unwrap();
    app_submenu.append(&PredefinedMenuItem::hide(None)).unwrap();
    app_submenu.append(&PredefinedMenuItem::hide_others(None)).unwrap();
    app_submenu.append(&PredefinedMenuItem::show_all(None)).unwrap();
    app_submenu.append(&PredefinedMenuItem::separator()).unwrap();
    app_submenu.append(&app_menu.quit_item).unwrap();
    menu_bar.append(&app_submenu).unwrap();

    // Edit menu
    let edit = Submenu::new("Edit", true);
    edit.append(&PredefinedMenuItem::undo(None)).unwrap();
    edit.append(&PredefinedMenuItem::redo(None)).unwrap();
    edit.append(&PredefinedMenuItem::separator()).unwrap();
    edit.append(&PredefinedMenuItem::cut(None)).unwrap();
    edit.append(&PredefinedMenuItem::copy(None)).unwrap();
    edit.append(&PredefinedMenuItem::paste(None)).unwrap();
    edit.append(&PredefinedMenuItem::select_all(None)).unwrap();
    menu_bar.append(&edit).unwrap();

    // Help menu
    let help = Submenu::new("Help", true);
    help.append(&app_menu.shortcuts_item).unwrap();
    help.append(&app_menu.help_item).unwrap();
    menu_bar.append(&help).unwrap();

    menu_bar
}

pub fn attach_to_window(menu: &Menu) {
    // On macOS, set as application menu (not window menu)
    menu.init_for_nsapp();
}
```

```rust
// main.rs — macOS branch
#[cfg(target_os = "macos")]
fn setup_menu(app_menu: &AppMenu) {
    let menu = platform::macos::install_menu(app_menu);
    platform::macos::attach_to_window(&menu);
}
```

## Shortcuts Accelerators on macOS

```rust
// Use SUPER (Cmd) not CONTROL on macOS
fn cmd(code: Code) -> Option<Accelerator> {
    Some(Accelerator::new(Some(Modifiers::SUPER), code))
}

shortcuts_item: MenuItem::new("Keyboard Shortcuts", true, cmd(Code::Slash)),
// Renders as Cmd+? (Shift is implied by ?)
```

## About Dialog

`PredefinedMenuItem::about()` with `AboutMetadata` uses the native NSAboutPanel.
No custom dialog needed — fill the metadata struct completely.

RULE: Always set name, version, authors, website, license, copyright in AboutMetadata
RULE: issue_url optional but recommended — shows as "Report a Bug" link on macOS


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
