---
tags: [css, naming, conventions, bem]
concepts: [naming-conventions, readability]
requires: [global/consistency.md]
related: [python/naming.md, rust/naming.md, global/naming-suffix.md]
layer: 3
---
# Naming Convention

> BEM-inspired — block-element--modifier

---

FORMAT: `.block-element`
FORMAT: `.block-element--modifier`

## Example

```css
.nav              /* Block */
.nav-link         /* Element */
.nav-link--active /* Modifier */
.nav-icon         /* Element */
.nav-icon--theme  /* Modifier */
```

RULE: Hyphen separates block-element
RULE: Double hyphen for modifiers (`--active`, `--disabled`)
RULE: No nesting beyond block-element-modifier

## File Header

```css
/**
 * Project Name - Component Name
 * Brief description of what this file contains
 */
```

## Comments

```css
/* Navigation container */
/* Actions container (theme + language) */
/* Mobile: Bottom bar */
/* Desktop: Top bar */
```

## Property Order Within Rulesets

1. Positioning (position, top, right, z-index)
2. Display & Box Model (display, flex, width, padding, margin)
3. Typography (font-size, line-height, color)
4. Visual (background, border, shadow)
5. Misc (cursor, transition)

## What NOT To Do

BANNED: `!important` (except for utility overrides)
BANNED: ID selectors for styling (`#header`)
BANNED: Deep nesting (`.nav .list .item .link`)
BANNED: Color values in layout files
BANNED: Magic numbers without comments
BANNED: `px` units for font-size (use rem)
BANNED: CSS frameworks (Tailwind, Bootstrap)
