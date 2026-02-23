# C++ Rules

> C++20/23 modern subset — Linux/BSD, RAII, jthread, Result types

---

## Target

PLATFORM: Linux (Ubuntu, Debian), BSD (FreeBSD, OpenBSD)
STANDARD: C++20 minimum, C++23 preferred
COMPILER: GCC 12+, Clang 15+
BUILD: CMake or Meson (no Makefiles)

## Philosophy

RULE: C++20/23 modern subset — not "all of C++"
RULE: Pro-Linux/BSD — POSIX first, no Windows abstractions
RULE: Automatic memory via RAII — never manual new/delete
RULE: Automatic threads via std::jthread — auto-join
RULE: Result types for errors — no exceptions
RULE: Same patterns as Python/JS — flat, explicit, validated

## Files

| File | Topic |
|------|-------|
| [memory.md](memory.md) | RAII, smart pointers |
| [threading.md](threading.md) | jthread, mutex, atomic |
| [errors.md](errors.md) | Result types, no exceptions |
| [posix.md](posix.md) | POSIX first (epoll, mmap, systemd) |
| [modules.md](modules.md) | Closed modules, pImpl |
| [nesting.md](nesting.md) | Flat code |
| [types.md](types.md) | Strong typing (enum class, optional) |
| [build.md](build.md) | CMake configuration |
| [testing.md](testing.md) | Catch2/doctest |
| [quick-ref.md](quick-ref.md) | Quick reference |
