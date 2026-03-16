---
tags: [uiux, tokens, dark-mode, light-mode, theming, config-driven]
concepts: [token-switching, theme-selection, config-driven-theme]
requires: [uiux/tokens.md, uiux/token-structure.md]
related: [uiux/theming.md, global/config-driven.md, slint/tokens.md, css/tokens.md]
keywords: [dark-mode, light-mode, prefers-color-scheme, token-switch, theme-config, font-scale, UiConfig]
layer: 3
---
# Light/Dark Token Switching and Theme Config

> Token names stay the same — values switch per scheme. Config drives which theme loads.

---

## Light/Dark Token Switching

```css
/* Single token name — value changes per scheme */
:root { --color-bg-primary: #ffffff; }

@media (prefers-color-scheme: dark) {
    :root { --color-bg-primary: #1a1a1a; }
}
```

```slint
// Slint — switch token globals based on system dark/light
export global Colors {
    in-out property <bool> dark-mode: false;
    out property <color> bg-primary: dark-mode ? #1a1a1a : #ffffff;
    out property <color> text-primary: dark-mode ? #f0f0f0 : #1a1a1a;
}
```

RULE: Components never branch on `dark-mode` — only token files do
RULE: A component that checks `dark-mode` directly to pick a color is BANNED — use tokens

## Config-Driven Theme Selection

Token files give the values, but WHICH theme to load comes from `UiConfig_cfg`:

```toml
# ~/.config/<app>/config/ui.toml
[theme]
name = "default"          # loads tokens/themes/default/
dark_mode = "system"      # "system" | "light" | "dark"
font_scale = 1.0
```

RULE: Theme name in `UiConfig_cfg.theme` — Gateway loads the right token set on startup
RULE: Font scale multiplied against all `--type-*` tokens — one setting, global effect
RULE: Never read theme config inside a component — Gateway passes `UiConfig_cfg` to the Adapter

RESULT: Theme changes propagate from one config entry to every component
REASON: Scattering theme logic across components makes switching impossible
