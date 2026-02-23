# Module System

> ESM only, closed modules, encapsulation-first

---

## ESM

RULE: ESM only — `"type": "module"` in package.json
RULE: `import/export` syntax (never `require/module.exports`)
RULE: File extensions required: `import './module.js'`
RULE: Node.js 18+ required

## Modular Architecture (Encapsulation)

RULE: One module per file — single responsibility
RULE: Modules are CLOSED — internal state not shared
RULE: Only exported functions/classes are public API
RULE: All internal variables stay private to module
RULE: Call modules from outside — never reach into their internals

## Patterns

### Module exposes functions, hides implementation

```javascript
// counter.js - CLOSED module
let count = 0;  // Private - not exported

export function increment() { count++; }
export function decrement() { count--; }
export function getCount() { return count; }
// count variable is NEVER accessible from outside
```

### Class with private fields

```javascript
// store.js - Encapsulated state
export class Store {
  #state = {};  // Private field - inaccessible from outside

  get(key) { return this.#state[key]; }
  set(key, value) { this.#state[key] = value; }
}
```

### Factory function

```javascript
// logger.js - Factory pattern
export function createLogger(prefix) {
  const logs = [];

  return {
    log(msg) { logs.push(`${prefix}: ${msg}`); },
    getLogs() { return [...logs]; }  // Return copy, not reference
  };
}
```

## Private Fields

RULE: Use `#` for private class fields (ES2022)
RULE: `#privateField` instead of `_privateField` convention

BANNED: Exporting mutable variables (`export let x`)
BANNED: Modifying imported values
BANNED: Reaching into module internals
BANNED: Global state outside modules
BANNED: Side effects on import (except initialization)
