---
tags: [javascript, documentation, jsdoc, exports]
concepts: [documentation, public-api, maintainability]
requires: [js/jsdoc.md]
feeds: [js/modules.md]
related: [python/docs.md, rust/docs.md, cpp/docs.md, kotlin/docs.md, csharp/docs.md]
keywords: [jsdoc, param, returns, throws, example, module-doc, exported]
layer: 4
---
# Documentation Requirements

> Every export documented — types, intent, and examples

---

RULE: JSDoc `/** */` on all exported functions
RULE: `@param`, `@returns`, `@throws` for public API
RULE: `@example` for non-obvious usage
RULE: Module-level JSDoc at top of each file explaining purpose

## Examples

```javascript
/**
 * Rate limiter — tracks request counts per key with sliding window.
 * @module rate-limiter
 */

/**
 * Check if a key has exceeded its rate limit.
 *
 * @param {string} key - Identifier (IP, user ID, API key)
 * @param {number} maxRequests - Allowed requests per window
 * @param {number} windowMs - Window size in milliseconds
 * @returns {boolean} True if the key is rate-limited
 * @throws {RangeError} If maxRequests <= 0 or windowMs <= 0
 *
 * @example
 * if (isRateLimited(clientIp, 100, 60_000)) {
 *   return res.status(429).json({ error: "Too many requests" });
 * }
 */
export function isRateLimited(key, maxRequests, windowMs) {
  // ...
}
```

BANNED: Undocumented exports — every `export` needs a JSDoc block
BANNED: Comments that restate the code (`// increment i` above `i++`)
