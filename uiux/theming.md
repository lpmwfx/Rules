---
tags: [theming, dark-mode, light-mode, system-appearance, uiux, slint]
concepts: [theming, system-appearance, accessibility]
requires: [uiux/tokens.md]
feeds: [slint/theming.md, css/theming.md]
related: [css/themes.md, css/tokens.md, global/config-driven.md, slint/globals.md]
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
    updateColors()
}

// Resolve colors against current appearance
let resolved = NSColor.labelColor.resolvedColor(with: effectiveAppearance)
```

RULE: Use semantic system colors (`NSColor.labelColor`, `NSColor.controlBackgroundColor`) — they adapt automatically
RULE: On macOS, do NOT call `NSApp.appearance = ...` at startup unless the user has set an explicit override
BANNED: Hardcoded `NSColor(red:green:blue:)` values for UI surfaces — use semantic colors

## GTK4 (Linux + macOS)

```rust
// GTK4 / Rust — automatic via libadwaita
app.style_manager().set_color_scheme(adw::ColorScheme::PreferDark);
let dark = app.style_manager().is_dark();
```

```python
# GTK4 / Python — libadwaita
style_manager = Adw.StyleManager.get_default()
style_manager.connect("notify::dark", self.on_appearance_changed)
```

RULE: Use `Adw.StyleManager` — it wires the portal automatically
RULE: Use `@define-color` tokens in CSS that map to `--adw-*` variables
BANNED: `gtk-application-prefer-dark-theme = true` in settings — this hardcodes dark mode

## Qt (Linux / macOS / Windows)

```cpp
connect(QGuiApplication::styleHints(), &QStyleHints::colorSchemeChanged,
        this, [this](Qt::ColorScheme scheme) {
    updatePalette(scheme == Qt::ColorScheme::Dark);
});
bool isDark = QGuiApplication::styleHints()->colorScheme() == Qt::ColorScheme::Dark;
```

```qml
Rectangle {
    color: palette.window        // adapts to system theme
    Text { color: palette.text }
}
```

RULE: Use `palette.window`, `palette.text`, `palette.button` — they follow the system palette
BANNED: Setting a fixed `QPalette` at startup that does not respond to system changes

## Compose / Android

```kotlin
@Composable
fun AppTheme(content: @Composable () -> Unit) {
    val darkTheme = isSystemInDarkTheme()
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme,
        content = content
    )
}
```

RULE: `isSystemInDarkTheme()` is the source — no manual preference needed at first launch
RULE: Store user override in persistent state (`_sta`) only if they explicitly choose one

Toolkit-specific implementations: [slint/theming.md](../slint/theming.md) | [css/theming.md](../css/theming.md)

## Pre-Ship Checklist

Add to [checklist.md](checklist.md):

- [ ] App appearance changes immediately when OS light/dark setting is toggled
- [ ] No hardcoded color values outside theme/token layer
- [ ] Both light and dark appearances tested on all target platforms
- [ ] App does NOT reset to light/dark on restart when system preference is dark/light

RESULT: Users get the appearance they expect without configuring the app
REASON: Respecting system appearance is a platform citizenship requirement, not a feature
