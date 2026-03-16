---
tags: [uiux, tokens, design-tokens, no-hardcoding, theming, declarative, slintscanners, create-before-use]
concepts: [design-tokens, declarative-ui, theme-config, slint-build-scan, create-before-use, workflow]
requires: [global/config-driven.md, global/data-driven-ui.md]
feeds: [uiux/theming.md, uiux/components.md, slint/init.md, slint/states.md, rust/constants.md]
related: [css/custom-properties.md, css/themes.md, global/file-limits.md, global/module-tree.md, slint/init.md, slint/states.md, rust/constants.md]
keywords: [design-tokens, magic-values, px, hex, color, spacing, typography, slint-global, css-variables, theme-config, modular-tokens, declarative, slintscanners, build-scan, create-before-use, workflow, create-token]
layer: 2
---
# Design Tokens — No Magic Values in UI

> All values are named tokens. UI components contain zero literals.

---

VITAL: UI component files MUST NOT contain literal values — no hex colors, no px sizes, no font names
VITAL: Every value that appears in a UI component is a token reference — a name, not a number
RULE: Tokens live in dedicated token files — one file per concern (colors, spacing, typography, radius, elevation)
RULE: A single central theme file imports and re-exports all token files
RULE: Changing a token value propagates to every component that uses it — zero search-and-replace
RULE: Token files are the ONLY place literal values appear in the UI layer
BANNED: Hardcoded hex values (`#3d3d3d`, `rgba(0,0,0,0.5)`) anywhere outside token files
BANNED: Hardcoded pixel values (`48px`, `16px`, `1.5rem`) inside component files
BANNED: Hardcoded font names or sizes in component files
BANNED: 800 scattered magic values — if you are writing numbers in a component, stop and create a token

## Create-Before-Use Workflow

VITAL: Tokens do not exist until YOU create them. The global files start empty.
VITAL: When you need a value, you MUST create the token first, then reference it.

```
Before writing ANY literal value in a UI component:

1. IDENTIFY the value type:
   - Color, spacing, typography, radius, shadow → token file (globals/theme/)
   - Size, duration, divisor                   → state file (state/)
   - Text label, state discriminator           → strings file (globals/strings)

2. SEARCH the appropriate global/state file for an existing token
   - e.g. need 100% → search Sizes for "full"
   - e.g. need 240px → search Sizes for "sidebar" or similar

3. Token EXISTS → reference it in your component

4. Token does NOT EXIST →
   a. OPEN the token/state file
   b. ADD the new token with a descriptive name
   c. SAVE the token file
   d. THEN reference the new token in your component

5. NEVER write the literal in the component — not even temporarily
```

RULE: The developer creates tokens — they are not pre-populated
RULE: Every new value means a new token — create it in the definition file first
RULE: If you cannot find a token, that means it has not been created yet — create it

## Why — Declarative Architecture

This is NOT a design system like Bootstrap. It is the opposite.

The idea: **move every real value down into state/token files**. The code above becomes purely declarative — it references names, never numbers. The state files are the data layer; the components are just structure.

```
WITHOUT tokens (imperative):
  Button { background: #4a90d9; padding: 12px 24px; font-size: 14px; }
  → Values are scattered. Changing one means hunting through every file.
  → The component describes HOW it looks — coupled to specific numbers.

WITH tokens (declarative):
  Button { background: Colors.accent; padding: Spacing.md; font-size: Type.body; }
  → Values live in ONE place (token files). Components are pure structure.
  → The component describes WHAT it is — decoupled from any specific value.
  → Change Colors.accent → every component updates. Zero search-and-replace.
```

The same principle applies to Rust code: move durations, limits, paths, URLs into `state/` modules → function bodies become declarative expressions with zero literals. See [rust/constants.md](../rust/constants.md).

This makes the system **dynamic** — the concrete values are data, not code. Swap the data layer (different theme, different config) and the entire application changes without touching a single component or function.

## Token File Structure

One file per concern. Never merge concerns into one giant file.

```
src/ui/tokens/
├── colors.{css,slint,toml}      # all color values
├── spacing.{css,slint,toml}     # margins, padding, gaps
├── typography.{css,slint,toml}  # font families, sizes, weights, line-heights
├── radius.{css,slint,toml}      # border radii
├── elevation.{css,slint,toml}   # shadows and z-index levels
└── theme.{css,slint,toml}       # imports all token files — single entry point
```

RULE: `theme.*` is the only file components import — they never import individual token files directly
RULE: Max 80 lines per token file — if it grows beyond that, split by subcategory

## Per-Toolkit Implementation

### Slint

```slint
// tokens/colors.slint
export global Colors {
    out property <color> bg-primary:   #1a1a1a;
    out property <color> bg-surface:   #2d2d2d;
    out property <color> text-primary: #f0f0f0;
    out property <color> text-muted:   #888888;
    out property <color> accent:       #4a90d9;
}

// tokens/spacing.slint
export global Spacing {
    out property <length> xs:  4px;
    out property <length> sm:  8px;
    out property <length> md:  16px;
    out property <length> lg:  24px;
    out property <length> xl:  48px;
}

// tokens/typography.slint
export global Type {
    out property <length>  body-size:    14px;
    out property <length>  heading-size: 22px;
    out property <int>     body-weight:  400;
    out property <int>     bold-weight:  700;
}

// tokens/theme.slint — re-exports everything
export { Colors, Spacing, Type } from "colors.slint";
// (import from spacing.slint, typography.slint, etc.)
```

```slint
// Component uses tokens — ZERO literal values
import { Colors, Spacing, Type } from "../tokens/theme.slint";

component PrimaryButton inherits Rectangle {
    background: Colors.accent;             // ✓ token
    border-radius: Spacing.xs;            // ✓ token

    Text {
        font-size: Type.body-size;         // ✓ token
        color: Colors.bg-primary;          // ✓ token
        padding: Spacing.sm;               // ✓ token
    }
}

// ❌ BANNED — literals scattered in component
component PrimaryButton inherits Rectangle {
    background: #4a90d9;     // BANNED
    border-radius: 4px;      // BANNED
    Text { font-size: 14px; color: #1a1a1a; padding: 8px; }  // BANNED
}
```

### CSS

```css
/* tokens/colors.css */
:root {
    --color-bg-primary:   #1a1a1a;
    --color-bg-surface:   #2d2d2d;
    --color-text-primary: #f0f0f0;
    --color-text-muted:   #888888;
    --color-accent:       #4a90d9;
}

/* tokens/spacing.css */
:root {
    --space-xs:  4px;
    --space-sm:  8px;
    --space-md:  16px;
    --space-lg:  24px;
    --space-xl:  48px;
}

/* tokens/theme.css — imports all token files */
@import "./colors.css";
@import "./spacing.css";
@import "./typography.css";
@import "./radius.css";
@import "./elevation.css";
```

```css
/* Component uses tokens — zero literal values */
.button-primary {
    background: var(--color-accent);          /* ✓ token */
    padding: var(--space-sm) var(--space-md); /* ✓ token */
    border-radius: var(--radius-sm);          /* ✓ token */
    font-size: var(--type-body-size);         /* ✓ token */
}

/* ❌ BANNED */
.button-primary {
    background: #4a90d9;    /* BANNED */
    padding: 8px 16px;      /* BANNED */
    border-radius: 4px;     /* BANNED */
    font-size: 14px;        /* BANNED */
}
```

### Kotlin / Compose

```kotlin
// tokens/AppTheme.kt — central theme entry point
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme,
        typography = AppTypography,
        content = content
    )
}

// Component uses MaterialTheme — zero literals
@Composable
fun PrimaryButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary  // ✓ token
        )
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium         // ✓ token
        )
    }
}
```

### GTK / Adwaita (CSS)

```css
/* tokens/colors.css — uses Adwaita system color variables */
:root {
    --app-accent: var(--accent-bg-color);    /* maps to Adwaita system token */
    --app-surface: var(--card-bg-color);
    --app-text: var(--view-fg-color);
}

/* Component */
.my-button {
    background: var(--app-accent);           /* ✓ token */
    color: var(--app-text);                  /* ✓ token */
}
```

## Token Naming Convention

```
--<type>-<role>-<variant>

--color-bg-primary      color / background / primary variant
--color-text-muted      color / text / muted variant
--space-md              spacing / medium
--type-body-size        typography / body / size
--radius-sm             border-radius / small
--elevation-card        shadow / card level
```

RULE: Names describe purpose, not appearance — `--color-accent` not `--color-blue`
RULE: Dark mode values use the SAME token names — tokens switch values, components stay identical

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

RESULT: Changing one token file updates every component that references it — zero hunting for scattered values
REASON: 800 hardcoded values in one component is a bug, not a style choice
