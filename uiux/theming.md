---
tags: [theming, dark-mode, light-mode, system-appearance, uiux, slint]
concepts: [theming, system-appearance, accessibility]
requires: [uiux/tokens.md]
related: [css/themes.md, css/custom-properties.md, global/config-driven.md, slint/globals.md]
keywords: [dark-mode, light-mode, system, appearance, NSAppearance, prefers-color-scheme, color-scheme, gtk, qt, swiftui, compose, slint, invoke-from-event-loop, Colors-global]
layer: 3
---
# System Appearance — Auto Light/Dark Theming

> Follow the OS — never hardcode light or dark, always respect system preference

---

VITAL: Every GUI app MUST follow the system light/dark preference automatically
VITAL: No manual theme toggle is needed unless the user explicitly requests override
VITAL: ALL values (colors, spacing, sizes, fonts) live in token files — never in component files (see [tokens.md](tokens.md))
RULE: Default appearance = system preference — zero configuration by the user
RULE: Switching OS appearance (System Preferences / Settings) updates the app immediately
RULE: App restart is NOT acceptable — appearance change must be live
RULE: CSS design tokens (colors, surfaces) come from the theme layer, never hardcoded
RULE: Token files switch values for light/dark — component code never branches on dark-mode to pick colors
BANNED: Hardcoded color values that do not adapt to system appearance
BANNED: Hardcoded pixel or font values in component files — those are tokens
BANNED: Shipping with only light mode — dark mode is not optional
BANNED: Requiring the user to set appearance inside the app when the OS already expresses it

## macOS — NSAppearance

macOS communicates appearance via `NSAppearance`. Toolkits that wrap AppKit/SwiftUI
pick this up automatically if you do not override it.

```swift
// SwiftUI — automatic, no code needed
// System appearance is inherited by default.
// Only add this if the user explicitly overrides:
.preferredColorScheme(.dark)  // user override — not default behavior
```

```swift
// AppKit — observe appearance changes
override func viewDidChangeEffectiveAppearance() {
    super.viewDidChangeEffectiveAppearance()
    // re-apply any manual color resolving here
    updateColors()
}

// Resolve colors against current appearance
let resolved = NSColor.labelColor.resolvedColor(with: effectiveAppearance)
```

RULE: Use semantic system colors (`NSColor.labelColor`, `NSColor.controlBackgroundColor`) — they adapt automatically
RULE: On macOS, do NOT call `NSApp.appearance = ...` at startup unless the user has set an explicit override in your preferences
BANNED: Hardcoded `NSColor(red:green:blue:)` values for UI surfaces — use semantic colors

## GTK4 (Linux + macOS)

GTK4 reads the system color scheme via the desktop portal (`org.freedesktop.portal.Settings`).
On GNOME, this is set by `gsettings org.gnome.desktop.interface color-scheme`.

```rust
// GTK4 / Rust — automatic via libadwaita
// AdwApplication respects system appearance by default.
// Explicit override (only if user chose it):
app.style_manager().set_color_scheme(adw::ColorScheme::PreferDark);

// Read current scheme for conditional logic:
let dark = app.style_manager().is_dark();
```

```python
# GTK4 / Python — libadwaita
style_manager = Adw.StyleManager.get_default()
# system scheme is applied automatically — no action needed

# Listen for changes:
style_manager.connect("notify::dark", self.on_appearance_changed)
```

RULE: Use `Adw.StyleManager` — it wires the portal automatically
RULE: Use `@define-color` tokens in CSS that map to `--adw-*` variables — they switch with the theme
BANNED: `gtk-application-prefer-dark-theme = true` in settings — this hardcodes dark mode

## Qt (Linux / macOS / Windows)

Qt 6.5+ introduces `QGuiApplication::styleHints()->colorScheme()` for system appearance.

```cpp
// Qt6 — automatic on supported platforms
// Qt follows the platform color scheme by default in Qt 6.5+.

// Listen for changes:
connect(QGuiApplication::styleHints(), &QStyleHints::colorSchemeChanged,
        this, [this](Qt::ColorScheme scheme) {
    updatePalette(scheme == Qt::ColorScheme::Dark);
});

// Query current scheme:
bool isDark = QGuiApplication::styleHints()->colorScheme() == Qt::ColorScheme::Dark;
```

```qml
// QML — use system palette (automatic)
Rectangle {
    color: palette.window        // adapts to system theme
    Text { color: palette.text } // adapts to system theme
}
```

RULE: Use `palette.window`, `palette.text`, `palette.button` — they follow the system palette
RULE: Never hardcode colors in QML — always use `palette.*` or CSS custom properties
BANNED: Setting a fixed `QPalette` at startup that does not respond to system changes

## Slint — Rust + cross-platform

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

## CSS / Web (WA / PWA)

```css
/* Always define both — browser picks based on OS */
:root {
    --bg:   #ffffff;
    --text: #1a1a1a;
    --surface: #f5f5f5;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg:   #1a1a1a;
        --text: #f0f0f0;
        --surface: #2a2a2a;
    }
}
```

```js
// Detect and react to changes
const mq = window.matchMedia('(prefers-color-scheme: dark)');
mq.addEventListener('change', e => updateTheme(e.matches ? 'dark' : 'light'));
```

RULE: Define `prefers-color-scheme: dark` media query alongside `:root` — never one without the other
RULE: All color values must be CSS custom properties — never inline hex values
BANNED: `localStorage` theme toggle as the ONLY mechanism — system preference is the default

## Compose / Android

```kotlin
// Jetpack Compose — automatic via MaterialTheme
@Composable
fun AppTheme(content: @Composable () -> Unit) {
    val darkTheme = isSystemInDarkTheme()  // reads system preference
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme,
        content = content
    )
}
```

RULE: `isSystemInDarkTheme()` is the source — no manual preference needed at first launch
RULE: Store user override in persistent state (`_sta`) only if they explicitly choose one

## Pre-Ship Checklist

Add to [checklist.md](checklist.md):

- [ ] App appearance changes immediately when OS light/dark setting is toggled
- [ ] No hardcoded color values outside theme/token layer
- [ ] Both light and dark appearances tested on all target platforms
- [ ] App does NOT reset to light/dark on restart when system preference is dark/light

RESULT: Users get the appearance they expect without configuring the app
REASON: Respecting system appearance is a platform citizenship requirement, not a feature
