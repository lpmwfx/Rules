---
tags: [themes, theming, multi-theme, material, solid, mica, acrylic]
concepts: [multi-theme, theme-file, material-theme, theme-switching]
requires: [uiux/tokens.md, slint/globals.md]
feeds: [uiux/theming.md]
related: [slint/states.md, slint/rust-bridge.md, global/config-driven.md]
keywords: [theme, solid, mica, acrylic, dark-mode, Colors, Effects, globals-theme]
layer: 3
---
# Slint Theme System — Multi-Theme with Built-in Light/Dark

> Each theme is one file with light + dark built in. Components import only `theme.slint`.

---

VITAL: All theme files live under `ui/globals/theme/` — never scattered across state files
VITAL: Each theme file contains both light AND dark values — no separate light/dark files
RULE: `ui/globals/theme.slint` is the single entry point — components import only this file
RULE: One `.slint` file per theme variant under `ui/globals/theme/`
RULE: All theme files export the SAME globals with the SAME property names — only values differ
RULE: Theme-specific effects (blur, opacity, tint) live in an `Effects` global
RULE: Adding a new theme = adding one file in `theme/` — no other files change
RULE: Max 80 lines per theme file — split by concern if it grows
RULE: Switching theme = changing one import line in `theme.slint`
RULE: Spacing and typography are shared — they live outside individual theme files
BANNED: Theme values scattered across multiple state files
BANNED: Separate light and dark files for the same theme
BANNED: Components importing from `globals/theme/solid.slint` directly — only via `theme.slint`
BANNED: Components checking which theme is active — `if theme == "mica"` is BANNED

## Folder Structure

```
ui/globals/
├── theme.slint              ← entry point (re-exports active theme)
└── theme/
    ├── solid.slint          ← standard flat surfaces (light + dark)
    ├── mica.slint           ← translucent layered material (light + dark)
    ├── acrylic.slint        ← blur-behind material (light + dark)
    ├── spacing.slint        ← shared across all themes
    └── typography.slint     ← shared across all themes
```

## Theme File Contract

Each theme file exports `Colors` and `Effects` globals. Every color branches on `dark-mode`:

```slint
// ui/globals/theme/solid.slint
export global Colors {
    in property <bool> dark-mode: false;
    out property <color> bg-primary:   dark-mode ? #1a1a1a : #ffffff;
    out property <color> accent:       #4a90d9;
}

export global Effects {
    in property <bool> dark-mode: false;
    out property <float> surface-opacity: 1.0;
    out property <length> blur-radius:    0px;
}
```

## Entry Point

```slint
// ui/globals/theme.slint — change this import to switch theme
export { Colors, Effects } from "theme/solid.slint";
export { Spacing } from "theme/spacing.slint";
export { Type } from "theme/typography.slint";
```

Dark/light is runtime (Adapter injects `set_dark_mode()`) — see slint/rust-bridge.md.
Theme selection is compile-time or config-driven (`UiConfig_cfg.theme`) — see global/config-driven.md.

RESULT: Themes are isolated, self-contained files — no values leak across state files
REASON: One file per theme with built-in light/dark eliminates scattered ternaries
