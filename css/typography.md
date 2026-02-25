---
tags: [css, typography, fonts, spacing]
concepts: [fonts, spacing]
keywords: [system-fonts, line-height, modular-scale]
layer: 4
---
# Typography, Spacing, and Layout

> System fonts, rem units, flexbox/grid

---

## Typography

RULE: System font stack (no web fonts by default)
RULE: `rem` units for font-size
RULE: Unitless line-height
RULE: Consistent heading scale

```css
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
}

h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.25rem; }
```

## Spacing

RULE: `rem` units for spacing (margin, padding)
RULE: Consistent spacing scale: 0.25, 0.5, 0.75, 1, 1.5, 2, 3rem

## Layout

RULE: Flexbox for 1D layouts (nav, toolbars)
RULE: Grid for 2D layouts (page structure, cards)
RULE: `max-width` + `margin: 0 auto` for containers

```css
.container {
  max-width: 720px;
  margin: 0 auto;
}

.site {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
```
