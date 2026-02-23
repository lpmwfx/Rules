# Testing

> Node.js built-in test runner — no external dependencies

---

RULE: Node.js built-in test runner (`node:test`)
RULE: `assert` from `node:assert/strict`
RULE: Test files: `*.test.js` alongside source
PATTERN: `describe()` for grouping, `it()` for cases

## Example

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

describe('myFunction', () => {
  it('does something', () => {
    assert.equal(myFunction('input'), 'expected');
  });
});
```
