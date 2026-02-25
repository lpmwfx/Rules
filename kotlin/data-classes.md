---
tags: [kotlin, data-classes, immutable, copy]
concepts: [data-modeling, immutability]
related: [python/types.md, rust/types.md]
keywords: [data-class, copy, destructuring]
layer: 4
---
# Immutable Data Classes

> val only, default values, copy for modifications

---

RULE: Immutable data classes — `val` only
RULE: Default values for optional fields
RULE: `copy()` for modifications
RULE: No logic in data classes

```kotlin
data class Product(
    val id: String,
    val name: String,
    val price: Double,
    val description: String = "",
    val imageUrl: String? = null
)

// Usage
val updated = product.copy(price = 19.99)
```

BANNED: Mutable public properties
BANNED: `var` for state (use MutableStateFlow)
