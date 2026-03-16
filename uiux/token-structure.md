---
tags: [uiux, tokens, design-tokens, file-structure, naming-convention]
concepts: [token-file-structure, token-naming]
requires: [uiux/tokens.md]
related: [global/file-limits.md, global/module-tree.md]
keywords: [token-file, colors, spacing, typography, radius, elevation, theme, naming, convention, purpose-not-appearance]
layer: 3
---
# Token File Structure and Naming

> One file per concern. Names describe purpose, not appearance.

---

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

RESULT: One import point, consistent naming — AI can find and create tokens without guessing
REASON: Scattered file imports and inconsistent names cause duplication and lookup failures
