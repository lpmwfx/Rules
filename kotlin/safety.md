---
tags: [safety, lateinit, reflection, suppress]
concepts: [unsafe-patterns, reflection, lateinit, null-assertion]
requires: [kotlin/types.md, kotlin/encapsulation.md]
keywords: [lateinit, suppress, reflection, not-null-assertion, unsafe, lazy]
layer: 4
---
# Safety

> lateinit only for frameworks — reflection only in tests — suppress needs proof

---

RULE: `lateinit` only for framework-injected properties (Android lifecycle, DI)
RULE: `@Suppress` requires explaining comment
RULE: Reflection only in test/infrastructure — never in domain code
RULE: `!!` (not-null assertion) requires comment explaining why null is impossible

```kotlin
// OK — framework injection
class MainActivity : AppCompatActivity() {
    lateinit var binding: ActivityMainBinding   // set by onCreate
}

// OK — lazy instead of lateinit for regular properties
class AppConfig_cfg {
    val database: DatabaseConfig by lazy { loadFromFile("db.toml") }
}

// OK — suppress with proof
@Suppress("UNCHECKED_CAST")  // safe: type checked by deserializer contract
val items = raw as List<String>

// OK — !! with explanation
val user = cache[userId]!!  // guaranteed present: checked in require() above
```

BANNED: `lateinit` for regular properties — use `lazy` or nullable
BANNED: `@Suppress("UNCHECKED_CAST")` without type proof
BANNED: Reflection in domain/core layer


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
