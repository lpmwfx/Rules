---
tags: [constants, magic-numbers, config]
concepts: [named-constants, configuration, compile-time-values]
requires: [global/config-driven.md]
feeds: [kotlin/tokens.md]
keywords: [const-val, companion-object, magic-number, config-class]
layer: 3
---
# Constants

> Named constants everywhere — no magic values in code

---

RULE: `const val` for compile-time constants
RULE: `companion object` constants for class-scoped values
RULE: No magic numbers in function bodies
RULE: Config loaded from `_cfg` data classes or resource files

```kotlin
// Top-level constants for shared values
const val API_VERSION = "v2"

// Class-scoped constants
class RetryPolicy_core {
    companion object {
        const val MAX_ATTEMPTS = 3
        const val BASE_DELAY_MS = 1000L
        const val BACKOFF_FACTOR = 2.0
    }

    fun nextDelay(attempt: Int): Long =
        (BASE_DELAY_MS * BACKOFF_FACTOR.pow(attempt)).toLong()
}

// Config as typed data class
data class ServerConfig_cfg(
    val host: String,
    val port: Int,
    val timeoutMs: Long
)
```

BANNED: Hardcoded URLs, paths, timeouts, port numbers
BANNED: Numeric literals without named constant
