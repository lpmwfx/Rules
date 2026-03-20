---
tags: [docs, kdoc, documentation, api]
concepts: [documentation, api-surface, kdoc]
requires: [kotlin/types.md]
keywords: [kdoc, param, return, throws, public-api, documentation]
layer: 4
---
# Documentation

> KDoc on all public API — summary first, parameters documented

---

RULE: KDoc `/** */` on all public functions, classes, properties
RULE: `@param` for all parameters
RULE: `@return` for non-Unit functions
RULE: `@throws` for functions that throw
RULE: First line is a summary — no empty KDoc blocks

```kotlin
/**
 * Fetches products matching the given query from the remote catalog.
 *
 * Results are sorted by relevance. Returns an empty list when the
 * catalog is unreachable rather than throwing.
 *
 * @param query Search string, minimum 2 characters
 * @param limit Maximum results to return (1..100)
 * @return Matching products, newest first
 * @throws IllegalArgumentException if [query] is blank or [limit] < 1
 */
fun searchProducts(query: String, limit: Int = 20): List<Product> {
    require(query.isNotBlank()) { "query must not be blank" }
    require(limit >= 1) { "limit must be >= 1" }
    // ...
}
```

BANNED: Undocumented public API
BANNED: KDoc that restates the function name (`/** Gets products. */` on `getProducts`)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
