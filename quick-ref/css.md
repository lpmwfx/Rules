---
tags: [combo, css]
concepts: [quick-ref, project-type]
keywords: [css, tokens, themes, cascade]
requires: [global/quick-ref.md, css/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: CSS

> CSS rules for any project with stylesheets. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| File limits | CSS: 150 lines max. Split by component | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Flat selectors preferred | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## CSS-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | Vanilla CSS, no frameworks | [css/cascade.md](../css/cascade.md) |
| Separation | Layout files: ZERO colors. Theme files: ONLY colors | [css/cascade.md](../css/cascade.md) |
| Cascade | Each file ADDS, none OVERWRITES — separate domains | [css/cascade.md](../css/cascade.md) |
| Modules | One file per component, self-contained | [css/modules.md](../css/modules.md) |
| Tokens | `--color-bg-1/2/3`, `--color-text-1/2/3`, `--shadow-1/2/3` | [css/tokens.md](../css/tokens.md) |
| Themes | Light on `:root`, dark on `[data-theme="dark"]` | [css/themes.md](../css/themes.md) |
| Naming | BEM-inspired: `.block-element--modifier` | [css/naming.md](../css/naming.md) |
| Responsive | Mobile-first, single breakpoint: 768px, `min-width` | [css/modules.md](../css/modules.md) |
| Typography | System fonts, `rem` units, unitless line-height | [css/tokens.md](../css/tokens.md) |
| Layout | Flexbox for 1D, Grid for 2D | [css/modules.md](../css/modules.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | Stylelint, browser devtools |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — CSS zero-literal check |

## BANNED

- `!important`
- ID selectors for styling
- Deep nesting (4+ levels)
- Tailwind, Bootstrap, or other utility frameworks
- Hardcoded color values outside theme files
- Files over 150 lines
- Non-English comments or class names
