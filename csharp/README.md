---
tags: [dotnet]
concepts: [csharp-rules]
related: [csharp/types.md, csharp/modules.md, csharp/errors.md, csharp/naming.md, csharp/threading.md, csharp/nesting.md, csharp/linq.md, csharp/verification.md, uiux/components.md, uiux/state-flow.md, global/module-tree.md]
layer: 6
---
# C# / .NET Rules

> .NET 9, C# 13, nullable-on — cross-platform first

---

## Target

PLATFORM: Windows, macOS, Linux, Android, iOS (Uno Platform for GUI)
RUNTIME: .NET 9 (LTS: .NET 8)
LANGUAGE: C# 13
BUILD: `dotnet` CLI / MSBuild
GUI: Uno Platform

## Philosophy

RULE: Modern C# 13 idioms — nullable reference types always enabled
RULE: Cross-platform first — no Windows-only APIs unless platform-gated
RULE: Records for data, classes for behavior — immutability by default
RULE: Async/await everywhere — no blocking calls on UI or async paths
RULE: Result-typed errors in domain code — exceptions only at system boundaries
RULE: One class per file — nesting = namespace of files, not nested classes
RULE: Stateless logic — all app state in a central `AppState_sta` type; functions transform, never store state
RULE: Internal by default — `public` only at assembly boundary

Same topology tags as all other languages — see [global/topology.md](../global/topology.md)

See: [global/module-tree.md](../global/module-tree.md) | [uiux/state-flow.md](../uiux/state-flow.md)

## Files

| File | Topic |
|------|-------|
| [types.md](types.md) | Records, nullable, value types, generics |
| [errors.md](errors.md) | Exceptions vs Result, validation |
| [modules.md](modules.md) | Namespaces, project structure, assemblies |
| [naming.md](naming.md) | PascalCase, camelCase, layer-tag suffix |
| [threading.md](threading.md) | async/await, Task, CancellationToken |
| [nesting.md](nesting.md) | Flat code, guard clauses |
| [linq.md](linq.md) | LINQ idioms and anti-patterns |
| [verification.md](verification.md) | Analyzers, format, test gates |
| [quick-ref.md](quick-ref.md) | Quick reference |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
