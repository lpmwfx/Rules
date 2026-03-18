---
tags: [modules, namespaces, project-structure]
concepts: [encapsulation, architecture, project-layout]
requires: [global/consistency.md]
keywords: [namespace, assembly, project, solution, internal, global-using, implicit-usings, alias]
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
├── Directory.Build.props          # <ImplicitUsings>enable</ImplicitUsings> here
├── MyApp.Core/
│   ├── GlobalUsings.cs            # One per project — project-specific global usings
│   ├── Config/
│   │   ├── Config_cfg.cs
│   │   └── ConfigLoader_core.cs
│   └── Users/
│       ├── User_core.cs
│       └── IUserRepository_adp.cs
├── MyApp.Infrastructure/
│   ├── GlobalUsings.cs
│   └── Users/
│       └── SqlUserRepository_adp.cs
├── MyApp.UI/
│   ├── GlobalUsings.cs
│   └── Pages/
│       └── MainPage.xaml
└── MyApp.Tests/
    ├── GlobalUsings.cs
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

## Global Usings

RULE: Enable `<ImplicitUsings>enable</ImplicitUsings>` in `Directory.Build.props` — once for all projects
RULE: One `GlobalUsings.cs` per project — all project-specific `global using` directives live here
RULE: Never scatter `global using` across random source files
RULE: Never duplicate SDK-implicit usings (`System`, `System.Linq`, `System.Threading.Tasks`, etc.)
RULE: Use namespace aliases to resolve name collisions

SDK implicit usings already include — do NOT re-declare these:
- **Microsoft.NET.Sdk**: `System`, `System.Collections.Generic`, `System.IO`, `System.Linq`,
  `System.Net.Http`, `System.Threading`, `System.Threading.Tasks`
- **Uno.Sdk**: WinUI namespaces (`Microsoft.UI.Xaml`, `Windows.UI.Xaml`, etc.) — check
  generated `obj/**/*.GlobalUsings.g.cs` to see what Uno.Sdk provides

```csharp
// GlobalUsings.cs — project root (e.g. MyApp.Core/)
// Only add namespaces used in 3+ files within this project

global using MyApp.Core.Users;
global using MyApp.Core.Config;

// Alias: resolves name collision
global using HttpClient = System.Net.Http.HttpClient;
```

```csharp
// BAD: scattered across source files
// UserService.cs
global using MyApp.Core.Users;   // ← belongs in GlobalUsings.cs

// BAD: duplicating SDK-provided usings
global using System.Linq;        // ← already implicit via SDK
global using Microsoft.UI.Xaml;  // ← already implicit via Uno.Sdk
```

NOTE: Uno Platform projects include a `GlobalUsings.cs` by default — use it, do not create a second one.

## Split Trigger

Split file when:
- More than one concept explained at file top
- Multiple lifecycles mixed (init, runtime, shutdown)
- File exceeds 300 LOC
