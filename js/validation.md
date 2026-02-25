---
tags: [javascript, validation, zod, runtime]
concepts: [runtime-checking, boundaries, validation]
requires: [global/validation.md]
related: [js/safety.md, python/types.md]
keywords: [zod, schema, parse, boundary]
layer: 4
---
# Runtime Validation

> Zod/Valibot at system boundaries

---

RULE: Validate at system boundaries (API, user input, file I/O)
RULE: Use `z.infer<typeof Schema>` for type extraction
PATTERN: `Schema.parse(data)` — throws on invalid
PATTERN: `Schema.safeParse(data)` — returns `{success, data/error}`

## Example

```javascript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

/** @typedef {z.infer<typeof UserSchema>} User */

/** @param {unknown} data @returns {User} */
function parseUser(data) {
  return UserSchema.parse(data);
}
```

PREFER: Valibot for smaller bundle size in browser

## Result Types

FORMAT: `{ success: true, data: result }`
FORMAT: `{ success: false, error: "message" }`
RULE: All functions returning results use this pattern
