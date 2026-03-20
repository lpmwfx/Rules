---
tags: [errors, exception, sealed, error-handling]
concepts: [error-handling, error-taxonomy, exception-boundaries]
requires: [kotlin/result-pattern.md, global/error-flow.md]
feeds: [kotlin/coroutines.md]
keywords: [throw, catch, runCatching, sealed-result, exception, error-taxonomy]
layer: 3
---
# Error Handling

> Exceptions for the unexpected — sealed Results for domain errors

---

RULE: Exceptions only for truly unexpected failures (I/O, network, OOM)
RULE: Domain errors as sealed Result — never exceptions
RULE: `runCatching` at system boundaries only — not for control flow
RULE: See `global/error-flow.md` for taxonomy

```kotlin
// System boundary — runCatching is appropriate here
suspend fun fetchUser(id: UserId): UserResult {
    return runCatching { api.getUser(id.value) }
        .fold(
            onSuccess = { UserResult.Found(it.toDomain()) },
            onFailure = { UserResult.NetworkError(it.message ?: "unknown") }
        )
}

// Domain — sealed result, no exceptions
sealed interface UserResult {
    data class Found(val user: User) : UserResult
    data class NotFound(val id: UserId) : UserResult
    data class NetworkError(val reason: String) : UserResult
}
```

BANNED: `throw` for expected failures — use sealed Result
BANNED: Empty catch blocks — always log or propagate
BANNED: `catch (e: Exception)` without recovery action


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
