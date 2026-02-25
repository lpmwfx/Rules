---
tags: [kotlin, coroutines, concurrency, flow]
concepts: [concurrency, async]
related: [rust/threading.md, cpp/threading.md]
keywords: [coroutine-scope, flow, suspend, dispatcher]
layer: 4
---
# Coroutines

> viewModelScope, Dispatchers, never block main thread

---

RULE: `viewModelScope` for ViewModels
RULE: `Dispatchers.IO` for I/O operations
RULE: `Dispatchers.Default` for CPU-intensive work
RULE: Never block main thread

```kotlin
class ProductViewModel(
    private val repository: ProductRepository
) {
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    fun loadProducts() {
        scope.launch {
            _state.update { it.copy(isLoading = true) }

            val result = withContext(Dispatchers.IO) {
                repository.getProducts()
            }

            _state.update { state ->
                when (result) {
                    is Result.Success -> state.copy(
                        items = result.data,
                        isLoading = false
                    )
                    is Result.Error -> state.copy(
                        error = result.message,
                        isLoading = false
                    )
                }
            }
        }
    }
}
```
