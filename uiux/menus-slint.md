---
tags: [uiux, menus, slint, rust, cross-platform, muda]
concepts: [native-menus, cross-platform-ui, slint, rust]
feeds: [uiux/menus-macos.md, uiux/menus-windows.md, uiux/menus-gnome.md, uiux/menus-kde.md]
related: [uiux/help-about.md, uiux/keyboard.md, uiux/context-menus.md]
keywords: [menu, muda, slint, rust, native, menubar, about, shortcuts, help, platform, winit]
layer: 3
---
# Menus in Rust + Slint

> Native menus via `muda` on macOS/Windows — Slint-native on Linux

---

VITAL: Use platform-native menus where the platform has them — never fake a menubar with Slint widgets on macOS or Windows
RULE: `muda` is the crate for native menus in Rust — works with Slint's winit backend
RULE: Menu structure (items, labels, shortcuts) is identical across platforms — only delivery differs
RULE: All menu events are handled in the main Rust event loop, not in Slint callbacks
RULE: About, Shortcuts, and Help are required in every app — see help-about.md
BANNED: Custom drawn menubar on macOS or Windows — use native
BANNED: Blocking the Slint event loop with menu callbacks

## Cargo dependencies

```toml
[dependencies]
slint = "1"
muda = "0.15"

[target.'cfg(target_os = "macos")'.dependencies]
objc2-app-kit = { version = "0.2", features = ["NSApplication"] }

[target.'cfg(target_os = "linux")'.dependencies]
# No muda needed — use Slint-native header bar widgets
```

## Shared Menu Structure

Define menu content once — platform files handle delivery:

```rust
// src/ui/menu.rs — shared menu definition (no platform code here)
pub struct AppMenu {
    pub about_item:     muda::MenuItem,
    pub shortcuts_item: muda::MenuItem,
    pub help_item:      muda::MenuItem,
    pub quit_item:      muda::PredefinedMenuItem,
}

impl AppMenu {
    pub fn new() -> Self {
        Self {
            about_item:     muda::MenuItem::new("About MyApp", true, None),
            shortcuts_item: muda::MenuItem::new("Keyboard Shortcuts", true,
                                Some(muda::accelerator::Accelerator::new(
                                    Some(muda::accelerator::Modifiers::CONTROL),
                                    muda::accelerator::Code::Slash,
                                ))),
            help_item:      muda::MenuItem::new("Help", true,
                                Some(muda::accelerator::Accelerator::new(
                                    None, muda::accelerator::Code::F1,
                                ))),
            quit_item:      muda::PredefinedMenuItem::quit(Some("Quit MyApp")),
        }
    }
}
```

## Platform files

| Platform | File | Delivery |
|----------|------|---------|
| macOS | [menus-macos.md](menus-macos.md) | NSMenu via muda — always visible at top of screen |
| Windows | [menus-windows.md](menus-windows.md) | Win32 menu via muda — inside the window frame |
| GNOME | [menus-gnome.md](menus-gnome.md) | Slint HeaderBar with hamburger PopupMenu |
| KDE | [menus-kde.md](menus-kde.md) | Slint HeaderBar — optionally exported to global menu via DBus |

## Menu Event Loop Pattern

```rust
// main.rs — handle menu events from muda alongside Slint
fn main() {
    let app_menu = AppMenu::new();
    platform::install_menu(&app_menu, &window); // platform-specific

    let ui = AppWindow::new().unwrap();
    let ui_weak = ui.as_weak();

    // Poll muda events each frame
    ui.window().on_render_post(move || {
        if let Ok(event) = muda::MenuEvent::receiver().try_recv() {
            let ui = ui_weak.unwrap();
            if event.id == app_menu.about_item.id() {
                ui.invoke_show_about();
            } else if event.id == app_menu.shortcuts_item.id() {
                ui.invoke_show_shortcuts();
            } else if event.id == app_menu.help_item.id() {
                ui.invoke_show_shortcuts(); // F1 → shortcuts for small apps
            }
        }
    });

    ui.run().unwrap();
}
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
