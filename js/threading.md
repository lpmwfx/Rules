---
tags: [async, promises, workers, concurrency]
concepts: [async-patterns, error-handling, parallelism, cancellation]
requires: [js/safety.md, global/error-flow.md]
keywords: [async, await, Promise, Worker, AbortController, then, catch, concurrency]
layer: 4
---
# Async Patterns

> async/await everywhere — Promises handled, work cancellable

---

RULE: `async/await` over `.then()` chains
RULE: `Promise.all()` for parallel independent operations
RULE: Web Workers for CPU-intensive work — never block main thread
RULE: Every async operation has error handling (`try/catch` or `.catch()`)
RULE: `AbortController` for cancellable operations

## Examples

```javascript
// Parallel independent fetches
const [users, products] = await Promise.all([
  fetchUsers(),
  fetchProducts(),
]);

// Cancellable operation
const controller = new AbortController();
try {
  const response = await fetch(url, { signal: controller.signal });
  return await response.json();
} catch (error) {
  if (error.name === "AbortError") return null;
  throw error;
}

// Timeout wrapper
async function withTimeout(promise, ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try { return await promise; }
  finally { clearTimeout(timer); }
}
```

BANNED: Callback pyramids — use `async/await`
BANNED: Unhandled Promise rejections — every async path must catch
BANNED: Fire-and-forget — always `await`, handle, or track async operations


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
