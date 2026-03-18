---
tags: [validation, require, check, precondition]
concepts: [input-validation, preconditions, state-invariants, boundary-validation]
requires: [kotlin/types.md, global/validation.md]
keywords: [require, check, precondition, invariant, boundary, IllegalArgumentException]
layer: 4
---
# Validation

> require() for preconditions, check() for invariants — validate at boundaries

---

RULE: `require()` for function preconditions (throws IllegalArgumentException)
RULE: `check()` for state invariants (throws IllegalStateException)
RULE: Validate at Gateway/Adapter boundary — domain code trusts typed inputs
RULE: Use sealed Result for validation errors — not exceptions

```kotlin
// Gateway boundary — validate raw input once
class OrderGateway_gtw(private val api: OrderApi) {

    fun submitOrder(rawItems: List<String>, rawTotal: String): OrderResult {
        // Preconditions at boundary
        require(rawItems.isNotEmpty()) { "Order must have at least one item" }
        val total = rawTotal.toBigDecimalOrNull()
            ?: return OrderResult.Invalid("Total is not a number: $rawTotal")
        require(total > BigDecimal.ZERO) { "Total must be positive" }

        // Domain code receives validated types
        return processOrder(OrderInput(items = rawItems, total = total))
    }
}

// State invariant inside a stateful component
class ConnectionPool_pal {
    fun acquire(): Connection {
        check(isInitialized) { "Pool not initialized — call init() first" }
        // ...
    }
}
```

BANNED: Manual null-check chains — use safe calls `?.` or `require()`
BANNED: Validation logic scattered through business methods
