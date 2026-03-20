---
tags: [eslint, linting, code-quality]
concepts: [linting, code-quality]
related: [js/typescript-cli.md]
keywords: [eslint, flat-config]
layer: 4
---
# ESLint Flat Config

> Type-aware linting with typescript-eslint v9+

---

RULE: Use typescript-eslint for type-aware rules
RULE: `strictTypeChecked` preset
RULE: Point `parserOptions.project` to jsconfig.json

## Critical Rules

- `@typescript-eslint/no-unsafe-assignment`: error
- `@typescript-eslint/no-unsafe-call`: error
- `@typescript-eslint/no-unsafe-member-access`: error
- `@typescript-eslint/no-unsafe-return`: error
- `@typescript-eslint/no-floating-promises`: error
- `@typescript-eslint/await-thenable`: error
- `@typescript-eslint/no-misused-promises`: error
- `eqeqeq`: always (`===` only, never `==`)
- `no-var`: error (`const/let` only)
- `prefer-const`: error


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
