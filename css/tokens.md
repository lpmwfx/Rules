---
tags: [tokens, design-tokens, custom-properties, variables, no-hardcoding]
concepts: [css-design-tokens, css-custom-properties, token-hierarchy]
requires: [uiux/tokens.md, uiux/token-structure.md]
related: [css/themes.md, css/cascade.md, uiux/token-switching.md]
keywords: [css-variables, custom-properties, design-tokens, root, color, spacing, shadow, surface, border, accent]
layer: 3
---
# CSS Token Implementation

> CSS custom properties as design tokens — all values in `:root`, zero literals in components

---

## Token Files

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

## Component Usage

```css
/* Component uses tokens — zero literal values */
.button-primary {
    background: var(--color-accent);          /* token */
    padding: var(--space-sm) var(--space-md); /* token */
    border-radius: var(--radius-sm);          /* token */
    font-size: var(--type-body-size);         /* token */
}

/* BANNED */
.button-primary {
    background: #4a90d9;    /* BANNED */
    padding: 8px 16px;      /* BANNED */
    border-radius: 4px;     /* BANNED */
    font-size: 14px;        /* BANNED */
}
```

## Token Hierarchy Reference

```css
/* Background */
--color-bg-1         /* Primary background (body) */
--color-bg-2         /* Secondary background (hover states) */
--color-bg-3         /* Tertiary background (nested elements) */

/* Surface (Cards, Panels) */
--color-surface-1    /* Primary surface */
--color-surface-2    /* Secondary surface */

/* Text */
--color-text-1       /* Primary text (headings, body) */
--color-text-2       /* Secondary text (labels, nav) */
--color-text-3       /* Tertiary text (muted, footer) */

/* Border */
--color-border-1     /* Light borders */
--color-border-2     /* Emphasized borders */

/* Accent */
--color-accent-1     /* Links, primary buttons */
--color-accent-2     /* Hover states */

/* Shadows */
--shadow-1           /* Subtle (inputs, small elements) */
--shadow-2           /* Medium (cards, dropdowns) */
--shadow-3           /* Strong (modals, popovers) */
```

RESULT: All CSS values live in `:root` custom properties — components are pure structure
REASON: Scattered hex values and px sizes make theming and consistency impossible


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
