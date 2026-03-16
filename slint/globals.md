---
tags: [slint, globals, singletons, tokens, app-bridge, strings, theming]
concepts: [slint-globals, design-tokens, event-routing-global, localization]
requires: [slint/component-model.md, uiux/tokens.md]
feeds: [uiux/theming.md, slint/app-bridge.md, slint/strings-global.md]
related: [slint/rust-bridge.md, global/config-driven.md, uiux/mother-child.md]
keywords: [global, singleton, Colors, Spacing, Type, Strings, AppBridge, in-property, ui-global, set-dark-mode, localization, per-instance, Theme, state-separation]
layer: 3
---
# Slint Globals

> One global per concern — tokens, strings, and bridge callbacks live in globals

---

RULE: Use globals for design tokens (`Theme`), localization strings (`Strings`), and shared event routing (`AppBridge`)
RULE: Each global is accessed from Rust via `ui.global::<GlobalName>()`
RULE: Globals are per-component-instance — re-register callbacks and re-inject values for each new window
RULE: Token globals use `out property` for computed values that read a single `in property` (e.g. `dark-mode`)
RULE: A consolidated `Theme` global is valid when it holds only design tokens — the test is "does it contain domain logic?"
BANNED: Domain state or business logic in globals — globals hold tokens, strings, and routing only

## Design token globals

See uiux/tokens.md for the full token system and slint/themes.md for multi-theme support.

Token globals live in `ui/globals/theme/` with one file per theme variant (solid, mica, acrylic).
Shared tokens (spacing, typography) live alongside theme variants. The entry point `ui/globals/theme.slint`
re-exports from the active theme — components import only `theme.slint`.

```
ui/globals/
├── theme.slint              ← entry point (re-exports active theme)
└── theme/
    ├── solid.slint          ← Solid theme: Colors + Effects (light + dark)
    ├── mica.slint           ← Mica theme: Colors + Effects (light + dark)
    ├── acrylic.slint        ← Acrylic theme: Colors + Effects (light + dark)
    ├── spacing.slint        ← shared across all themes
    └── typography.slint     ← shared across all themes
```

```slint
// ui/globals/theme.slint — switch theme by changing this import
export { Colors, Effects } from "theme/solid.slint";
export { Spacing } from "theme/spacing.slint";
export { Type } from "theme/typography.slint";
```

```rust
// Adapter injects dark-mode on startup (PAL reads OS preference)
let is_dark = pal::appearance::is_dark_mode();
ui.global::<Colors>().set_dark_mode(is_dark);
ui.global::<Effects>().set_dark_mode(is_dark);
```

RULE: Only token globals branch on `dark-mode` — components use `Colors.bg-primary`, never `if dark-mode`
RULE: Token files are the ONLY place literal hex/px values appear in `.slint` source
RULE: Each theme file contains both light AND dark values — no separate files per mode

## Globals and Mother-Child State Separation

Globals complement the mother-child pattern (see uiux/mother-child.md). The mother Window component owns state via `in-out property`, and the `Theme` global separates design tokens from layout — like CSS is separate from HTML.

```
ui/
├── globals/
│   ├── theme.slint            ← entry point (re-exports active theme)
│   ├── theme/
│   │   ├── solid.slint        ← Solid: Colors + Effects (light + dark)
│   │   ├── mica.slint         ← Mica: Colors + Effects (light + dark)
│   │   ├── spacing.slint      ← shared spacing tokens
│   │   └── typography.slint   ← shared type tokens
│   ├── app-bridge.slint       ← centralised event routing
│   └── strings.slint          ← localization strings
├── views/
│   ├── navbar.slint           ← stateless child (in property + callback)
│   └── workspace-view.slint
└── app-window.slint           ← mother (inherits Window, in-out property = state)
```

RULE: State (`in-out property`) lives only in the mother Window component
RULE: Design tokens (`out property`) live in globals — children reference `Theme.xyz`
RULE: Children never own state — they use `in property` to receive and `callback` to emit

AppBridge details: [slint/app-bridge.md](app-bridge.md)
Strings/localization: [slint/strings-global.md](strings-global.md)

RESULT: AI can edit a child file by reading only that file + the Theme global — no hidden state
REASON: Separating state (mother) from tokens (global) keeps both files small and focused
