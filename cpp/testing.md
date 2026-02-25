---
tags: [cpp, testing, tdd, catch2]
concepts: [tdd, quality, testing]
requires: [cpp/types.md, cpp/errors.md]
related: [python/testing.md, rust/verification.md]
keywords: [catch2, ctest, real-data]
layer: 4
---
# Testing

> Catch2 or doctest — real resources, same structure as Python

---

RULE: Catch2 or doctest for unit tests
RULE: Same structure as Python — test class per module
RULE: Real resources when possible (tmpfiles, localhost sockets)

```cpp
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest/doctest.h>
#include "config.hpp"

TEST_CASE("Config::load") {
    SUBCASE("loads valid file") {
        auto result = Config::load("test_fixtures/valid.conf");
        CHECK(result.success);
        CHECK(result.data.get("key") == "value");
    }

    SUBCASE("fails on missing file") {
        auto result = Config::load("nonexistent.conf");
        CHECK_FALSE(result.success);
        CHECK(result.error.find("not found") != std::string::npos);
    }
}
```
