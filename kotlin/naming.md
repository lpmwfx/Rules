---
tags: [naming, conventions, suffix]
concepts: [naming-conventions, readability, layer-tags]
requires: [global/naming-suffix.md]
keywords: [camelCase, PascalCase, UPPER_SNAKE_CASE, suffix, boolean-prefix]
layer: 3
---
# Naming

> Consistent names — camelCase functions, PascalCase types, layer suffixes

---

RULE: `camelCase` for functions, properties, variables
RULE: `PascalCase` for classes, interfaces, objects, enums
RULE: `UPPER_SNAKE_CASE` for `const val`
RULE: Layer-tag suffix on types: `_adp`, `_core`, `_pal`, `_gtw`
RULE: Boolean properties prefixed with `is`, `has`, `can`

```kotlin
// Correct naming
class ProductRepository_adp(
    private val apiClient: ApiClient_gtw
) {
    val isConnected: Boolean = false
    val hasProducts: Boolean get() = productCount > 0

    fun fetchProducts(): List<Product_core> { ... }

    companion object {
        const val MAX_RETRY_COUNT = 3
        const val DEFAULT_TIMEOUT_MS = 5000L
    }
}
```

BANNED: Abbreviations (`mgr`, `ctx`, `btn`) — write full words
BANNED: Hungarian notation (`strName`, `iCount`)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
