---
tags: [uiux, tokens, design-tokens, no-hardcoding, theming, declarative, slintscanners, create-before-use]
concepts: [design-tokens, declarative-ui, theme-config, slint-build-scan, create-before-use, workflow]
requires: [global/config-driven.md, global/data-driven-ui.md]
feeds: [uiux/theming.md, uiux/components.md, slint/init.md, slint/states.md, rust/constants.md, uiux/token-structure.md, uiux/token-switching.md, slint/tokens.md, css/tokens.md, kotlin/tokens.md, css/gtk-tokens.md]
related: [css/tokens.md, css/themes.md, global/file-limits.md, global/module-tree.md, slint/init.md, slint/states.md, rust/constants.md]
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

Per-toolkit implementations: [slint/tokens.md](../slint/tokens.md) | [css/tokens.md](../css/tokens.md) | [kotlin/tokens.md](../kotlin/tokens.md) | [css/gtk-tokens.md](../css/gtk-tokens.md)
Token file structure and naming: [uiux/token-structure.md](token-structure.md)
Light/dark switching and config: [uiux/token-switching.md](token-switching.md)

RESULT: Changing one token file updates every component that references it — zero hunting for scattered values
REASON: 800 hardcoded values in one component is a bug, not a style choice
