---
tags: [combo, cpp]
concepts: [quick-ref, project-type]
keywords: [cpp, cmake, c++20, c++23]
requires: [global/quick-ref.md, cpp/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: C++ Project

> C++ CLI, library, or system tool. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | C++: 350 lines max. Split into new translation unit | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## C++-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Standard | C++20 minimum, C++23 preferred | [cpp/types.md](../cpp/types.md) |
| Platform | Linux/BSD, POSIX first | [cpp/modules.md](../cpp/modules.md) |
| Memory | `unique_ptr` default, NEVER raw `new/delete` | [cpp/memory.md](../cpp/memory.md) |
| Threads | `std::jthread`, `std::scoped_lock`, `std::atomic` | [cpp/types.md](../cpp/types.md) |
| Errors | `Result<T>` or `std::expected`, no exceptions | [cpp/errors.md](../cpp/errors.md) |
| Modules | One class per .hpp/.cpp, pImpl for privacy | [cpp/modules.md](../cpp/modules.md) |
| Types | `enum class`, `optional`, `string_view`, `span` | [cpp/types.md](../cpp/types.md) |
| Build | CMake, `-fno-exceptions`, sanitizers in debug | [cpp/modules.md](../cpp/modules.md) |
| Testing | Catch2/doctest, real resources | [cpp/testing.md](../cpp/testing.md) |

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

## Verification

| Gate | Tools |
|------|-------|
| Local | `cmake --build`, sanitizers (ASan, UBSan, TSan) |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all C++ checks |

## BANNED

- `new`/`delete` — use smart pointers
- Exceptions — use `Result<T>` or `std::expected`
- Raw owning pointers
- Deep inheritance hierarchies
- Multiple inheritance (except interfaces)
- Windows-specific APIs in portable code
- Files over 350 lines
- Deep nesting (4+ levels)
- `utils/`, `helpers/`, `common/` folders
- Non-English code, comments, or identifiers

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`
