---
tags: [cpp, memory, raii, smart-pointers]
concepts: [memory-management, lifecycle, raii]
requires: [cpp/types.md]
related: [rust/ownership.md]
keywords: [unique-ptr, shared-ptr, raii]
layer: 3
---
# Memory Management

> Automatic via RAII — never manual new/delete

---

RULE: `std::unique_ptr` as DEFAULT — single ownership
RULE: `std::shared_ptr` only when explicitly needed (document why)
RULE: NEVER raw `new/delete`
RULE: NEVER raw pointers for ownership (only for views)
RULE: Stack allocation when size is known and small

```cpp
// GOOD: Automatic cleanup
auto buffer = std::make_unique<char[]>(1024);
auto config = std::make_unique<Config>(load_config());

// GOOD: Non-owning view (raw pointer OK)
void process(const Config* config);  // doesn't own

// BANNED: Manual memory
auto* ptr = new Thing();  // NO
delete ptr;               // NO
```

BANNED: `new/delete` (use smart pointers)
BANNED: Raw owning pointers
BANNED: C-style casts (use `static_cast` etc.)
