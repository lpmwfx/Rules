---
tags: [constants, configuration, magic-values]
concepts: [named-constants, configuration, immutability]
requires: [global/config-driven.md]
feeds: [js/safety.md]
keywords: [const, freeze, magic-number, hardcoded, environment, config]
layer: 3
---
# Named Constants

> Every value has a name — no magic numbers, no hardcoded strings

---

RULE: All configurable values as `const` in a dedicated constants module
RULE: `Object.freeze()` for constant objects
RULE: No magic numbers or strings in function bodies
RULE: Configuration loaded from environment or config file — never hardcoded

## Examples

```javascript
// constants.js — single source of truth
export const MAX_RETRIES = 3;
export const DEFAULT_TIMEOUT_MS = 5000;
export const API_VERSION = "v2";

export const HTTP_STATUS = Object.freeze({
  OK: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
});

// config.js — environment-driven
export const config = Object.freeze({
  apiUrl: process.env.API_URL ?? "http://localhost:3000",
  port: Number(process.env.PORT ?? 8080),
  logLevel: process.env.LOG_LEVEL ?? "info",
});
```

BANNED: Hardcoded URLs, ports, paths, timeouts in function bodies
BANNED: Magic numbers without a named constant (`if (retries > 3)` — use `MAX_RETRIES`)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
