---
tags: [types, null-safety, sealed, inline-class]
concepts: [type-safety, null-safety, sealed-types, value-classes]
requires: [global/validation.md]
feeds: [kotlin/result-pattern.md, kotlin/data-classes.md]
keywords: [nullable, sealed-interface, value-class, smart-cast, platform-type]
layer: 3
---
# Types

> Null safety, sealed hierarchies, value classes — the type system is your guard

---

RULE: Nullable types explicit — `String?` only when null is a valid state
RULE: `sealed interface` for closed type hierarchies
RULE: `value class` (inline) for type-safe wrappers (IDs, units)
RULE: Smart casts over explicit casts — `is` check then direct use

```kotlin
// Value class — zero-cost type safety
@JvmInline
value class UserId(val value: String)

@JvmInline
value class Pixels(val value: Int)

// Sealed interface — compiler-checked exhaustiveness
sealed interface LoadState<out T> {
    data object Loading : LoadState<Nothing>
    data class Ready<T>(val data: T) : LoadState<T>
    data class Failed(val reason: String) : LoadState<Nothing>
}

// Smart cast — no explicit cast needed after is-check
fun describe(state: LoadState<String>): String = when (state) {
    is LoadState.Loading -> "Loading..."
    is LoadState.Ready   -> state.data     // smart cast to Ready<String>
    is LoadState.Failed  -> state.reason
}
```

BANNED: Platform types (`!`) — annotate nullability explicitly
BANNED: Unchecked casts (`as`) without `is` guard
BANNED: `Any` as parameter type — use sealed interface or generics


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
