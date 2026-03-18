---
tags: [cpp, documentation, doxygen, api-docs]
concepts: [documentation, api-surface, self-documenting]
requires: [cpp/types.md]
feeds: []
related: [rust/docs.md, python/docs.md, js/docs.md, kotlin/docs.md, csharp/docs.md]
keywords: [doxygen, param, return, throws, brief, comment, header, public-api]
layer: 4
---
# C++ Documentation Rules

> Every public symbol has a Doxygen comment — brief, params, return, throws

---

RULE: `///` or `/** */` Doxygen comments on all public API
RULE: `@brief` one-line summary required on every documented symbol
RULE: `@param` for each parameter, `@return` for return value, `@throws` for exceptions

```cpp
/// @brief Load user by ID from the database.
/// @param id Unique user identifier.
/// @return The user if found, std::nullopt otherwise.
/// @throws DatabaseError on connection failure.
std::optional<User> load_user(int id);
```

BANNED: Undocumented public headers — every `.h` export needs Doxygen
BANNED: Comments that restate the code (`// increment i` above `i++`)
