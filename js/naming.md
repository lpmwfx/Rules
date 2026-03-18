---
tags: [naming, conventions, camelcase]
concepts: [naming-conventions, readability, consistency]
requires: [global/naming-suffix.md]
feeds: [js/modules.md]
keywords: [camelCase, PascalCase, UPPER_SNAKE, boolean-prefix, event-handler]
layer: 3
---
# Naming Conventions

> Predictable names make code searchable and intent obvious

---

RULE: `camelCase` for variables and functions
RULE: `PascalCase` for classes and constructors
RULE: `UPPER_SNAKE_CASE` for constants
RULE: Boolean variables prefixed with `is`, `has`, `can`, `should`
RULE: Event handlers prefixed with `on` or `handle`

## Examples

```javascript
// Variables and functions — camelCase
const userCount = getActiveUsers().length;
function validateEmail(address) { /* ... */ }

// Classes — PascalCase
class PaymentGateway { /* ... */ }

// Constants — UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const DEFAULT_TIMEOUT_MS = 5000;

// Booleans — intent prefix
const isAuthenticated = token !== null;
const hasPermission = roles.includes("admin");
const canRetry = attemptCount < MAX_RETRY_COUNT;

// Event handlers — on/handle prefix
button.addEventListener("click", handleSubmit);
function onConnectionLost(event) { /* ... */ }
```

BANNED: Single-letter variables outside loop indices (`i`, `j`, `k` are fine in `for`)
BANNED: Abbreviations that obscure meaning (`mgr`, `ctx`, `btn`, `val`, `tmp`)
