---
tags: [cpp, build, cmake, configuration]
concepts: [build-system, configuration]
related: [cpp/errors.md, cpp/threading.md]
keywords: [cmake, presets, vcpkg, conan]
layer: 4
---
# Build Configuration

> CMake with strict warnings, sanitizers, no exceptions

---

```cmake
cmake_minimum_required(VERSION 3.20)
project(myapp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Strict warnings
add_compile_options(
    -Wall -Wextra -Wpedantic
    -Werror
    -fno-exceptions        # No exceptions
    -fno-rtti              # No RTTI (optional)
)

# Sanitizers for debug
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-fsanitize=address,undefined)
    add_link_options(-fsanitize=address,undefined)
endif()

# Link pthread
find_package(Threads REQUIRED)
target_link_libraries(myapp PRIVATE Threads::Threads)

# Systemd (optional)
find_package(PkgConfig)
pkg_check_modules(SYSTEMD libsystemd)
if(SYSTEMD_FOUND)
    target_link_libraries(myapp PRIVATE ${SYSTEMD_LIBRARIES})
endif()
```

## Recommended Dependencies

PREFER: Header-only libraries when small
PREFER: System packages (apt/pkg) over vendoring
PREFER: vcpkg or Conan for complex dependencies

- fmt (formatting, until std::format widespread)
- spdlog (logging)
- nlohmann/json (JSON)
- Catch2 or doctest (testing)
- systemd (service integration)
