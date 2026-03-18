---
tags: [cpp, validation, static-assert, concepts, nodiscard]
concepts: [compile-time-validation, boundary-validation, type-constraints]
requires: [cpp/types.md, global/validation.md]
feeds: [cpp/safety.md]
related: [rust/validation.md, python/validation.md, js/validation.md, csharp/validation.md]
keywords: [static_assert, concepts, nodiscard, narrowing, cast, boundary, invariant]
layer: 4
---
# C++ Validation Rules

> Catch errors at compile time — static_assert, concepts, nodiscard — validate at boundaries

---

RULE: `static_assert` for compile-time invariants
RULE: Concepts (C++20) for template parameter validation
RULE: `[[nodiscard]]` on functions returning error or status values
RULE: Validate at system boundaries — internal code trusts typed inputs

```cpp
// GOOD — compile-time constraint
static_assert(sizeof(Header) == 16, "Header must be 16 bytes for wire format");

// GOOD — concept constraint
template<std::integral T>
T safe_add(T a, T b);

// GOOD — nodiscard on status
[[nodiscard]] ErrorCode send_message(std::string_view msg);
```

BANNED: Unchecked casts — use `static_cast` with validation
BANNED: Implicit narrowing conversions — use `gsl::narrow` or explicit check
