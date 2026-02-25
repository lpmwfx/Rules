---
tags: [kotlin, encapsulation, visibility, internal]
concepts: [architecture, privacy, encapsulation]
requires: [global/consistency.md]
related: [rust/modules.md, js/modules.md]
layer: 3
---
# Encapsulation

> Private by default — platform layer hides Java imports

---

RULE: Private by default — only expose what's needed
RULE: Internal for module-level visibility
RULE: Use interfaces for abstraction
RULE: No public mutable state

## Repository Pattern

```kotlin
interface ProductRepository {
    suspend fun getProducts(): List<Product>
    suspend fun getProduct(id: String): Product?
}

internal class ProductRepositoryImpl(
    private val api: ApiClient,
    private val cache: ProductCache
) : ProductRepository {

    override suspend fun getProducts(): List<Product> {
        return cache.get() ?: api.fetchProducts().also { cache.set(it) }
    }

    override suspend fun getProduct(id: String): Product? {
        return getProducts().find { it.id == id }
    }
}
```

## Platform Encapsulation (Desktop JVM)

NOTE: On JVM, some Java imports are unavoidable (file system, native dialogs).
NOTE: The solution is ENCAPSULATION — hide Java behind Kotlin interfaces.

RULE: ALL `java.*` and `javax.*` imports MUST be in `platform/` layer
RULE: `domain/` and `ui/` MUST NOT import `java.*` or `javax.*` directly
RULE: Platform layer exposes ONLY Kotlin types
RULE: Platform components initialize ONCE at app start

## Layer Structure

```
platform/               ← ENCAPSULATES all Java/Swing/AWT
│   ├── FileSystem.kt       ← Hides java.io.File
│   └── Dialogs.kt          ← Hides javax.swing
domain/                 ← Pure Kotlin, uses platform interfaces
│   └── models/
ui/                     ← Pure Compose, uses domain types
│   └── components/
```

## Encapsulated File System

```kotlin
// platform/FileSystem.kt - ONLY file with java.io imports
interface FileSystem {
    fun readText(path: String): String
    fun listFiles(path: String): List<String>
    fun isDirectory(path: String): Boolean
}

internal class JvmFileSystem : FileSystem {
    override fun readText(path: String): String = java.io.File(path).readText()
    override fun listFiles(path: String): List<String> =
        java.io.File(path).listFiles()?.map { it.absolutePath } ?: emptyList()
    override fun isDirectory(path: String): Boolean = java.io.File(path).isDirectory
}
```

BANNED: `java.io.*` imports in domain/ or ui/
BANNED: `javax.swing.*` imports outside platform/
BANNED: `java.awt.*` imports outside platform/
BANNED: Passing `java.io.File` across layer boundaries (use String paths)
BANNED: Initializing Swing LookAndFeel per-call (causes state corruption)
