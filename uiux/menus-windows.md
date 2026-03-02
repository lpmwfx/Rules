---
tags: [uiux, menus, windows, slint, rust, muda, win32]
concepts: [native-menus, windows-ux, win32-menu]
requires: [uiux/menus-slint.md]
related: [uiux/help-about.md, uiux/keyboard.md]
keywords: [windows, win32, muda, menubar, winui, about, shortcuts, slint, rust, HMENU]
layer: 4
---
# Windows Menus — Rust + Slint

> Win32 native menu via muda — attached to the window frame

---

VITAL: Windows apps should have a native menu bar attached to the window — not a custom Slint toolbar
RULE: Use `Ctrl+,` for Preferences (Windows convention, not Cmd)
RULE: Use `Ctrl+Q` for Quit (Windows convention)
RULE: Use `Ctrl+?` for Shortcuts (Ctrl+Shift+/)
RULE: Menu is attached to the HWND after Slint creates the window
RULE: About dialog is a custom ContentDialog-equivalent — no native standard exists on Windows
BANNED: Alt+F4 in the menu — it is a system shortcut, already works without listing it

## Windows Menu Structure

```
File          Edit          View          Help
────          ────          ────          ────
Preferences   Undo Ctrl+Z   Zoom          Keyboard Shortcuts Ctrl+?
───           Redo          ───           Report Issue
Quit Ctrl+Q   ───           Sidebar F9    ───
              Cut           Fullscreen    About MyApp
              Copy          F11
              Paste
              Select All
```

## Implementation

```rust
// src/platform/windows.rs
use muda::{Menu, Submenu, MenuItem, PredefinedMenuItem};
use muda::accelerator::{Accelerator, Modifiers, Code};
use raw_window_handle::HasWindowHandle;

pub fn install_menu(app_menu: &crate::ui::menu::AppMenu) -> Menu {
    let menu_bar = Menu::new();

    // File menu
    let file = Submenu::new("&File", true);
    file.append(&MenuItem::new(
        "&Preferences\tCtrl+,",
        true,
        Some(Accelerator::new(Some(Modifiers::CONTROL), Code::Comma)),
    )).unwrap();
    file.append(&PredefinedMenuItem::separator()).unwrap();
    file.append(&app_menu.quit_item).unwrap();
    menu_bar.append(&file).unwrap();

    // Edit menu
    let edit = Submenu::new("&Edit", true);
    edit.append(&PredefinedMenuItem::undo(None)).unwrap();
    edit.append(&PredefinedMenuItem::redo(None)).unwrap();
    edit.append(&PredefinedMenuItem::separator()).unwrap();
    edit.append(&PredefinedMenuItem::cut(None)).unwrap();
    edit.append(&PredefinedMenuItem::copy(None)).unwrap();
    edit.append(&PredefinedMenuItem::paste(None)).unwrap();
    edit.append(&PredefinedMenuItem::select_all(None)).unwrap();
    menu_bar.append(&edit).unwrap();

    // Help menu
    let help = Submenu::new("&Help", true);
    help.append(&app_menu.shortcuts_item).unwrap();
    help.append(&app_menu.help_item).unwrap();
    help.append(&PredefinedMenuItem::separator()).unwrap();
    help.append(&app_menu.about_item).unwrap();
    menu_bar.append(&help).unwrap();

    menu_bar
}

pub fn attach_to_window(menu: &Menu, window: &slint::Window) {
    use raw_window_handle::{HasWindowHandle, RawWindowHandle};
    let handle = window.window_handle().window_handle().unwrap();
    if let RawWindowHandle::Win32(win32) = handle.as_ref() {
        unsafe { menu.init_for_hwnd(win32.hwnd.get() as _).unwrap() }
    }
}
```

```rust
// main.rs — Windows branch
#[cfg(target_os = "windows")]
fn setup_menu(app_menu: &AppMenu, window: &slint::Window) {
    let menu = platform::windows::install_menu(app_menu);
    platform::windows::attach_to_window(&menu, window);
}
```

## About Dialog on Windows

No native About standard — show a Slint dialog via callback:

```rust
// In menu event handler:
if event.id == app_menu.about_item.id() {
    ui.invoke_show_about(); // Slint callback → shows AboutDialog component
}
```

```slint
// AboutDialog.slint
component AboutDialog inherits Dialog {
    title: "About MyApp";
    Text { text: "MyApp"; font-size: 20px; }
    Text { text: "Version " + AppGlobals.version; }
    Text { text: "© 2024–2026 Your Name"; }
    Button { text: "yoursite.example"; clicked => { open-url("https://yoursite.example"); } }
    Button { text: "License: GPL-3.0"; clicked => { open-url(AppGlobals.license-url); } }
    Button { text: "Close"; clicked => { self.close(); } }
}
```

RULE: About dialog shows: name, version, description, author, website, license — all fields
RULE: Website and license are clickable links, not plain text
