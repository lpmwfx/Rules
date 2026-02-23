# JSDoc Type Annotations

> Static types via JSDoc — no .ts files needed

---

FORMAT: `/** @type {Type} */` for variables
FORMAT: `/** @param {Type} name */` for parameters
FORMAT: `/** @returns {Type} */` for return types
FORMAT: `/** @typedef {object} Name */` for custom types

## Example

```javascript
/** @typedef {{ id: number, email: string, role: 'admin' | 'user' }} User */

/**
 * @param {string} greeting
 * @param {string} name
 * @returns {string}
 */
function greet(greeting, name) {
  return `${greeting}, ${name}!`;
}
```

## Advanced Patterns

PATTERN: `/** @type {z.infer<typeof Schema>} */` for Zod inference
PATTERN: `/** @returns {value is Type} */` for type predicates
PATTERN: `/** @template T */` for generics
PATTERN: `/** @type {Type} */ (value)` for inline casts
