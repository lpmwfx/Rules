# Result Pattern

> Sealed class Result — no exceptions for expected failures

---

RULE: No exceptions for expected failures
RULE: Sealed class Result for operations that can fail
RULE: Handle all cases explicitly

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String, val cause: Throwable? = null) : Result<Nothing>()
}

// Usage
suspend fun fetchProducts(): Result<List<Product>> {
    return try {
        Result.Success(api.getProducts())
    } catch (e: Exception) {
        Result.Error("Failed to fetch products", e)
    }
}

// Handling
when (val result = repository.fetchProducts()) {
    is Result.Success -> showProducts(result.data)
    is Result.Error -> showError(result.message)
}
```
