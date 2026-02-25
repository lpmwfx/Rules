---
tags: [css, responsive, mobile-first, breakpoints]
concepts: [mobile-first, breakpoints]
related: [css/typography.md, css/themes.md]
keywords: [media-query, container-query, mobile-first]
layer: 4
---
# Responsive Design

> Mobile-first, single breakpoint at 768px

---

RULE: Mobile-first (base styles for mobile)
RULE: Single breakpoint: 768px (mobile/desktop)
RULE: Use `min-width` for desktop overrides

## Pattern

```css
/* Mobile (default) */
.nav-bar {
  position: fixed;
  bottom: 0;
}

/* Desktop */
@media (min-width: 768px) {
  .nav-bar {
    position: sticky;
    top: 0;
  }
}
```

## Reset

```css
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

## Safe Area (Mobile)

```css
padding-bottom: calc(0.5rem + env(safe-area-inset-bottom));
```

## Transitions

RULE: Short duration (0.2s) for interactive elements
RULE: Only transition specific properties

```css
transition: background 0.2s;
```

BANNED: `transition: all` (performance issue)

## Icons

RULE: Fixed size (1.25rem or 1.5rem)
RULE: Use `filter: invert(1)` for dark mode if needed
RULE: `display: block` to remove inline spacing
