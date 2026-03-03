---
tags: [css, validation, tokens, custom-properties]
concepts: [validation, design-tokens, boundaries]
requires: [global/validation.md, css/custom-properties.md]
related: [uiux/tokens.md]
keywords: [css-variables, hardcoded, token-enforcement]
layer: 4
---
# CSS Validation

> No hardcoded values — every style value comes from a custom property

---

RULE: All color values must reference a `--color-*` custom property
RULE: All spacing, sizing, and typography values must reference tokens
RULE: No `!important` — it overrides the token cascade
BANNED: Hardcoded hex colors (`#fff`, `#1a2b3c`)
BANNED: Hardcoded `rgb()` or `rgba()` color literals
BANNED: Font sizes in `px` — use `--font-size-*` tokens or `rem`

## CSS as a Validation Layer

CSS custom properties are CSS's form of boundary validation:
the token system is the schema, and using a token asserts that
the value is valid and consistent across the design system.

```css
/* BANNED — hardcoded value bypasses the token schema */
.button { background: #3a7ff6; }

/* CORRECT — value comes from the validated token catalog */
.button { background: var(--color-accent-1); }
```

## Enforcement

The `css/checks/tokens.py` scanner (rulestools) flags:
- Hardcoded hex colors, rgb/rgba literals
- Font-size in px
- `!important` declarations

See `css/custom-properties.md` for the full token catalog.
