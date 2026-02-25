---
tags: [css, custom-properties, variables, design-tokens]
concepts: [design-tokens, variables]
related: [css/themes.md, css/cascade.md]
keywords: [css-variables, design-tokens]
layer: 4
---
# CSS Custom Properties

> Design tokens for colors, surfaces, and shadows

---

## Background Hierarchy

```css
--color-bg-1    /* Primary background (body) */
--color-bg-2    /* Secondary background (hover states) */
--color-bg-3    /* Tertiary background (nested elements) */
```

## Surface (Cards, Panels)

```css
--color-surface-1    /* Primary surface */
--color-surface-2    /* Secondary surface */
```

## Text Hierarchy

```css
--color-text-1    /* Primary text (headings, body) */
--color-text-2    /* Secondary text (labels, nav) */
--color-text-3    /* Tertiary text (muted, footer) */
```

## Border

```css
--color-border-1    /* Light borders */
--color-border-2    /* Emphasized borders */
```

## Accent (Interactive)

```css
--color-accent-1    /* Links, primary buttons */
--color-accent-2    /* Hover states */
```

## Shadows

```css
--shadow-1    /* Subtle (inputs, small elements) */
--shadow-2    /* Medium (cards, dropdowns) */
--shadow-3    /* Strong (modals, popovers) */
```
