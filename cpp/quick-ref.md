---
tags: [cpp, quick-ref, reference, summary]
concepts: [reference, summary]
related: [cpp/types.md, cpp/modules.md, cpp/errors.md, cpp/memory.md, cpp/testing.md]
layer: 6
---
# C++ Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Standard | C++20 minimum, C++23 preferred |
| Platform | Linux/BSD, POSIX first |
| Memory | `unique_ptr` default, NEVER raw `new/delete` |
| Threads | `std::jthread`, `std::scoped_lock`, `std::atomic` |
| Errors | `Result<T>` or `std::expected`, no exceptions |
| Modules | One class per .hpp/.cpp, pImpl for privacy |
| Nesting | Max 3 levels, early returns |
| Types | `enum class`, `optional`, `string_view`, `span` |
| Build | CMake, `-fno-exceptions`, sanitizers in debug |
| Testing | Catch2/doctest, real resources |
| BANNED | `new/delete`, exceptions, raw owning ptrs, Windows APIs |

## Naming

```cpp
namespace my_app {           // snake_case namespaces
class ConfigLoader {         // PascalCase classes
    Result<Config> load();   // snake_case methods
    std::string path_;       // trailing underscore for members
};
constexpr int kMaxRetries = 3;  // k prefix for constants
static int s_instance_count;    // s_ prefix for static
}  // namespace my_app
```

BANNED: Deep inheritance hierarchies
BANNED: Multiple inheritance (except interfaces)
