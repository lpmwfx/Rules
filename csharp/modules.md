---
tags: [csharp, modules, namespaces, project-structure]
concepts: [encapsulation, architecture, project-layout]
requires: [global/consistency.md]
related: [rust/modules.md, kotlin/encapsulation.md, js/modules.md]
keywords: [namespace, assembly, project, solution, internal]
layer: 3
---
# Module Structure

> One class per file — internal by default, public only at assembly boundary

---

RULE: One top-level type per file (class, record, interface, enum)
RULE: File name matches type name exactly
RULE: `internal` for intra-assembly types — `public` only at assembly boundary
RULE: No circular dependencies between projects
RULE: Max ~300 LOC per file
RULE: Max ~10 public types per assembly
RULE: No `Utilities`, `Helpers`, `Common` namespaces without explicit domain

## Layout

```
MyApp/
├── MyApp.sln
├── MyApp.Core/           # Domain logic — no UI, no infra dependencies
│   ├── Config/
│   │   ├── Config_cfg.cs
│   │   └── ConfigLoader_core.cs
│   └── Users/
│       ├── User_core.cs
│       └── IUserRepository_adp.cs
├── MyApp.Infrastructure/ # Adapters, DB, file I/O
│   └── Users/
│       └── SqlUserRepository_adp.cs
├── MyApp.UI/             # Uno Platform UI layer
│   └── Pages/
│       └── MainPage.xaml
└── MyApp.Tests/
    └── Users/
        └── UserTests.cs
```

## Namespace Convention

RULE: Namespace matches folder path: `MyApp.Core.Users`
RULE: Use file-scoped namespaces (`namespace MyApp.Core.Users;`) — not block-scoped

```csharp
// GOOD: File-scoped namespace
namespace MyApp.Core.Users;

public record User_core(UserId Id, string Name);
```

## Split Trigger

Split file when:
- More than one concept explained at file top
- Multiple lifecycles mixed (init, runtime, shutdown)
- File exceeds 300 LOC
