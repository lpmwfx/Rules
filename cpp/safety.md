---
tags: [safety, memory-safety, smart-pointers, sanitizers]
concepts: [memory-safety, ownership, undefined-behavior, safe-casts]
requires: [cpp/memory.md, cpp/types.md]
feeds: []
keywords: [unique_ptr, shared_ptr, span, sanitizer, asan, ubsan, new, delete, reinterpret_cast, void-pointer]
layer: 4
---
# C++ Safety Rules

> No raw new/delete, no C-style casts, sanitizers in debug — eliminate undefined behavior

---

RULE: No raw `new`/`delete` — use `std::make_unique` / `std::make_shared`
RULE: `std::span` or `gsl::span` over raw pointer+length pairs
RULE: `-fsanitize=address,undefined` in debug builds
RULE: Every C-style cast replaced with `static_cast` / `dynamic_cast`

```cpp
// GOOD
auto config = std::make_unique<Config>();
void process(std::span<const std::byte> buffer);

// BAD
Config* config = new Config();    // raw new
delete config;                     // raw delete
int x = (int)some_float;          // C-style cast
```

BANNED: Raw `new` / `delete`
BANNED: C-style casts `(int)x` — use `static_cast<int>(x)`
BANNED: `reinterpret_cast` without `// SAFETY:` comment explaining invariant
BANNED: `void*` without documented invariant describing the pointed-to type


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
