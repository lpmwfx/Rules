---
tags: [naming, conventions, layer-tag]
concepts: [naming-conventions, readability, consistency]
requires: [global/naming-suffix.md]
feeds: [cpp/docs.md]
keywords: [snake_case, PascalCase, UPPER_SNAKE_CASE, hungarian, naming, prefix, suffix]
layer: 3
---
# C++ Naming Rules

> Consistent casing per element kind — snake, Pascal, UPPER — plus layer-tag suffixes

---

RULE: `snake_case` for functions and variables
RULE: `PascalCase` for classes, structs, enums, and type aliases
RULE: `UPPER_SNAKE_CASE` for constants and macros
RULE: `_` prefix for private member variables (`_count`, `_buffer`)
RULE: Layer-tag suffix on types: `_adp`, `_core`, `_pal`, `_gtw` — matches folder role

```cpp
// GOOD
class ConfigLoader_core {};
constexpr int MAX_RETRIES = 5;
void load_config();
int _retry_count;

// BAD
class configLoader {};   // wrong case
int iCount;              // Hungarian
#define MAXRETRIES 5     // no separator
```

BANNED: Hungarian notation (`strName`, `iCount`, `bFlag`, `pNode`)
BANNED: Single-letter names outside loop indices (`i`, `j`, `k` allowed in `for`)
