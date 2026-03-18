---
tags: [modules, packages, visibility, structure]
concepts: [package-structure, visibility, encapsulation, topology]
requires: [global/module-tree.md, global/topology.md, kotlin/encapsulation.md]
keywords: [package, internal, import, file-structure, circular-dependency]
layer: 3
---
# Modules

> One type per file — internal by default — packages mirror layer topology

---

RULE: One class/interface per file — file name matches type name
RULE: `internal` visibility by default — `public` only for API surface
RULE: Package structure mirrors layer topology (core/, adapter/, gateway/, pal/)
RULE: No circular package dependencies

```
com.example.app/
├── core/                  ← Domain models, pure logic
│   ├── Product.kt
│   └── PricingService.kt
├── adapter/               ← Orchestration, use cases
│   └── ProductAdapter.kt
├── gateway/               ← External APIs, databases
│   └── ProductApi.kt
└── pal/                   ← Platform abstractions
    └── FileSystem.kt
```

```kotlin
// gateway/ProductApi.kt — internal by default
internal class ProductApi(
    private val httpClient: HttpClient
) {
    suspend fun fetchProducts(): List<ProductDto> { ... }
}
```

BANNED: Multiple public types in one file
BANNED: Wildcard imports (`import com.example.*`)
