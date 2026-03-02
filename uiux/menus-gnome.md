---
tags: [uiux, menus, gnome, linux, slint, rust, headerbar, hamburger]
concepts: [native-menus, gnome-hig, headerbar, hamburger-menu]
requires: [uiux/menus-slint.md]
related: [uiux/help-about.md, uiux/keyboard.md, uiux/context-menus.md]
keywords: [gnome, linux, headerbar, hamburger, popupmenu, slint, rust, about, shortcuts, no-menubar, adwaita]
layer: 4
---
# GNOME Menus — Rust + Slint

> No native menubar on GNOME — use HeaderBar with hamburger PopupMenu in Slint

---

VITAL: GNOME does NOT have a window menubar — never add one, it violates HIG
VITAL: Primary actions go in the HeaderBar — secondary actions in the hamburger PopupMenu
RULE: Hamburger menu (≡) in top-right of HeaderBar contains: Shortcuts, Preferences, Help, About
RULE: About is a Slint dialog (no GTK AdwAboutDialog available from pure Rust/Slint)
RULE: Shortcuts window is a Slint PopupWindow or Dialog — opened by Ctrl+?
RULE: Register Ctrl+? and F1 as Slint key handlers — no muda needed on Linux
BANNED: Native GTK menubar — GNOME HIG explicitly forbids traditional menubars
BANNED: Putting Quit in the hamburger menu — Ctrl+Q is sufficient, Quit belongs nowhere in GNOME UI

## GNOME Menu Structure (HeaderBar)

```
┌─────────────────────────────────────────────┐
│  [Back] [Forward]   MyApp      [+] [Search] [≡] │
└─────────────────────────────────────────────┘
                                              │
                                    ┌─────────┴──────┐
                                    │ Keyboard Shortcuts │
                                    │ Preferences        │
                                    │ ─────────────────  │
                                    │ Help               │
                                    │ About MyApp        │
                                    └────────────────────┘
```

## Slint HeaderBar with Hamburger

```slint
// HeaderBar.slint
import { Button, PopupWindow } from "std-widgets.slint";

component HeaderBar inherits Rectangle {
    height: 48px;
    background: #2d2d2d;

    callback show-shortcuts();
    callback show-preferences();
    callback show-about();

    HorizontalLayout {
        padding: 8px;
        spacing: 4px;

        // Left: navigation actions
        Button { text: "‹"; }
        Button { text: "›"; }

        // Center: title
        Rectangle { horizontal-stretch: 1; }
        Text {
            text: "MyApp";
            font-size: 16px;
            font-weight: 700;
        }
        Rectangle { horizontal-stretch: 1; }

        // Right: primary action + hamburger
        Button { text: "+"; }
        Button {
            text: "≡";
            clicked => { hamburger-menu.show(); }
        }
    }

    hamburger-menu := PopupWindow {
        x: parent.width - 220px;
        y: 48px;
        width: 220px;

        Rectangle {
            background: #3d3d3d;
            border-radius: 8px;

            VerticalLayout {
                padding: 4px;

                MenuItem { text: "Keyboard Shortcuts   Ctrl+?";
                    clicked => { hamburger-menu.close(); root.show-shortcuts(); } }
                MenuItem { text: "Preferences   Ctrl+,";
                    clicked => { hamburger-menu.close(); root.show-preferences(); } }
                MenuSeparator {}
                MenuItem { text: "Help   F1";
                    clicked => { hamburger-menu.close(); root.show-shortcuts(); } }
                MenuItem { text: "About MyApp";
                    clicked => { hamburger-menu.close(); root.show-about(); } }
            }
        }
    }
}
```

## Keyboard Shortcuts (Ctrl+? and F1)

```rust
// Register in Slint — no muda on Linux
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
```

## About Dialog (Slint)

```slint
// AboutDialog.slint
component AboutDialog inherits Dialog {
    title: "About MyApp";

    VerticalLayout {
        spacing: 12px;
        padding: 24px;
        alignment: center;

        Image { source: @image-url("icons/app-icon.png"); width: 64px; height: 64px; }
        Text { text: "MyApp"; font-size: 22px; font-weight: 700; horizontal-alignment: center; }
        Text { text: AppGlobals.version; color: #888; horizontal-alignment: center; }
        Text { text: "Short description of what the app does."; wrap: word-wrap; }
        Text { text: "© 2024–2026 Your Name"; color: #888; }

        HorizontalLayout {
            spacing: 8px;
            Button { text: "yoursite.example";
                clicked => { open-url("https://yoursite.example"); } }
            Button { text: "GPL-3.0 License";
                clicked => { open-url(AppGlobals.license-url); } }
        }

        Button { text: "Close"; clicked => { self.close(); } }
    }
}
```

## Shortcuts Window (Slint)

```slint
// ShortcutsWindow.slint
component ShortcutsWindow inherits Dialog {
    title: "Keyboard Shortcuts";
    width: 500px;

    VerticalLayout {
        padding: 16px;
        spacing: 16px;

        ShortcutGroup {
            title: "Navigation";
            shortcuts: [
                { key: "Alt+←", action: "Go Back" },
                { key: "Alt+→", action: "Go Forward" },
            ];
        }
        ShortcutGroup {
            title: "General";
            shortcuts: [
                { key: "Ctrl+,", action: "Preferences" },
                { key: "Ctrl+?", action: "Keyboard Shortcuts" },
                { key: "Ctrl+Q", action: "Quit" },
            ];
        }
        // Add app-specific groups here
    }
}
```
