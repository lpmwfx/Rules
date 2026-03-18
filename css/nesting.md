---
tags: [nesting, specificity, selectors, layers]
concepts: [selector-nesting, specificity-management, cascade-layers]
requires: [css/cascade.md]
feeds: [css/modules.md]
related: [global/nesting.md]
keywords: [nesting, ampersand, parent-selector, at-layer, important, specificity, id-selector, hover, focus, modifier, flat-selector]
layer: 4
---
# Selector Nesting & Specificity

> Max 3 levels, flat selectors preferred, `@layer` over `!important`

---

RULE: Max 3 levels of selector nesting
RULE: Use `&` parent selector for state variants (`:hover`, `:focus`, `.--modifier`)
RULE: `@layer` for specificity management over `!important`
RULE: Flat selectors preferred — nesting only for genuine parent-child

```css
/* GOOD: shallow nesting with & for states */
.card {
  border: 1px solid var(--border);

  &:hover { border-color: var(--accent); }
  &.--featured { background: var(--highlight); }

  .card__title {
    font-weight: 600;
  }
}

/* GOOD: @layer for specificity control */
@layer base, components, overrides;

/* BAD: deep nesting — hard to read, high specificity */
.page .main .section .card .title { ... }
```

BANNED: `!important` — restructure cascade instead
BANNED: Nesting deeper than 3 levels
BANNED: ID selectors for styling (`#myId`)
BANNED: Overqualified selectors (`div.card`, `ul.nav-list`) — class alone is sufficient
