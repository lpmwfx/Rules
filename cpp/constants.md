---
tags: [constants, no-hardcoding, zero-literals, constexpr]
concepts: [zero-literals, named-values, state-files, compile-time-constants]
requires: [global/config-driven.md]
feeds: [cpp/naming.md]
keywords: [constexpr, const, magic-number, define, literal, timeout, state-folder]
layer: 3
---
# C++ Constants — All Values Named

> All hard values live in `state/` headers or config structs. Function bodies contain zero literals.

---

RULE: `constexpr` for compile-time constants
RULE: `const` for runtime constants that cannot be `constexpr`
RULE: Named constants in a dedicated `state/` directory — one header per concern
RULE: No magic numbers in function bodies — extract to named `constexpr`

```cpp
// GOOD — state/limits.h
constexpr int MAX_RETRIES = 3;
constexpr auto CONNECT_TIMEOUT = std::chrono::seconds(30);

// GOOD — usage
retry(MAX_RETRIES, CONNECT_TIMEOUT);

// BAD — magic numbers in function body
retry(3, std::chrono::seconds(30));
```

BANNED: `#define` for numeric constants — use `constexpr`
BANNED: Hardcoded paths, URLs, timeouts in function bodies — extract to `state/`
