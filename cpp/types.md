---
tags: [cpp, types, strong-types, concepts]
concepts: [type-safety, type-checking]
requires: [global/validation.md]
related: [python/types.md, rust/types.md]
keywords: [strong-typedef, concepts, constexpr]
layer: 3
---
# Type Safety

> Strong typing — enum class, optional, string_view, span

---

RULE: Strong typing — no implicit conversions
RULE: `enum class` (not plain enum)
RULE: `std::optional<T>` for nullable values
RULE: `std::string_view` for non-owning string references
RULE: `std::span<T>` for non-owning array views

```cpp
// GOOD: Strong types
enum class Status { pending, active, done };  // scoped enum

std::optional<User> find_user(int id);  // explicit nullable

void process(std::string_view text);     // non-owning, no copy
void process(std::span<const int> data); // non-owning array view

// BAD: Weak types
enum Status { PENDING, ACTIVE };  // pollutes namespace
User* find_user(int id);          // nullptr ambiguous
void process(const std::string&); // forces copy or temp
```

BANNED: Macros for constants (use `constexpr`)
BANNED: `std::endl` (use `'\n'`)
BANNED: `using namespace std` (in headers)
