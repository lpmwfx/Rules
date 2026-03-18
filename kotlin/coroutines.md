---
tags: [coroutines, concurrency, flow]
concepts: [concurrency, async]
keywords: [coroutine-scope, flow, suspend, dispatcher]
layer: 4
---
# Coroutines

> Dispatchers, never block main thread

---

RULE: `Dispatchers.IO` for I/O operations
RULE: `Dispatchers.Default` for CPU-intensive work
RULE: `Dispatchers.Main` only for emitting results to the UI layer — logic stays on IO/Default
RULE: Never block main thread — no `runBlocking` in production code
RULE: Use `SupervisorJob()` in long-lived scopes so one child failure does not cancel siblings

```kotlin
// Adapter layer — I/O on Dispatchers.IO, result emitted to state flow
class ProductAdapter(private val repository: ProductRepository) {
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    fun loadProducts() {
        scope.launch {
            val result = repository.getProducts()          // IO dispatcher
            withContext(Dispatchers.Main) {
                _state.update { it.copy(products = result) } // emit to state
            }
        }
    }
}
```
