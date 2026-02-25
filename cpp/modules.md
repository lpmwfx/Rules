---
tags: [cpp, modules, c++20, encapsulation]
concepts: [encapsulation, architecture]
requires: [global/consistency.md]
related: [rust/modules.md, python/structure.md]
keywords: [module, export, import, partition]
layer: 3
---
# Module Structure

> One class/module per file pair — closed modules with pImpl

---

RULE: One class/module per file pair (.hpp/.cpp)
RULE: Header declares interface, source implements
RULE: Private implementation via pImpl or anonymous namespace
RULE: No circular dependencies

## File Layout

```
src/
├── config/
│   ├── config.hpp      # Public interface
│   └── config.cpp      # Implementation (private helpers in anon namespace)
├── network/
│   ├── socket.hpp
│   └── socket.cpp
└── main.cpp
```

## Example

```cpp
// config.hpp - PUBLIC interface only
#pragma once
#include <string>
#include "result.hpp"

class Config {
public:
    static Result<Config> load(const std::string& path);
    std::string get(const std::string& key) const;
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;  // pImpl hides internals
};

// config.cpp - PRIVATE implementation
#include "config.hpp"

namespace {  // Anonymous namespace = private to this file
    bool validate_key(const std::string& key) { /*...*/ }
}

struct Config::Impl {
    std::unordered_map<std::string, std::string> data;
};

Result<Config> Config::load(const std::string& path) {
    // implementation
}
```
