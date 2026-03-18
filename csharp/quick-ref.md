---
tags: []
concepts: []
related: [csharp/types.md, csharp/modules.md, csharp/errors.md, csharp/naming.md, csharp/threading.md, csharp/verification.md]
layer: 6
---
# C# Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Runtime | .NET 9 (LTS: .NET 8), C# 13 |
| Platform | Cross-platform — Windows, macOS, Linux, Android, iOS (Uno Platform) |
| Nullable | `<Nullable>enable</Nullable>` in every project — no exceptions |
| Types | `record` for data, `struct` for value types, newtype via `readonly record struct` |
| Errors | `Result<T>` in domain, exceptions only at system boundaries |
| Modules | One type per file, `internal` by default, `public` at assembly boundary |
| Namespaces | File-scoped, matches folder path — `namespace MyApp.Core.Users;` |
| Global Usings | `<ImplicitUsings>enable</ImplicitUsings>` in `Directory.Build.props`; project-specific in `GlobalUsings.cs` per project; Uno.Sdk adds WinUI namespaces automatically |
| Nesting | Max 3 levels, guard clauses, early returns |
| Async | `async Task` everywhere, `CancellationToken` on all public async methods |
| LINQ | Method syntax, deferred — materialise only when needed |
| Naming | PascalCase types/methods, `_camelCase` fields, `I`-prefix interfaces + layer-tag |
| Layer-tag | Same topology as Rust — see `global/topology.md` |
| GUI | Uno Platform — UI updates via `DispatcherQueue.TryEnqueue()` |
| Verification | Level 0 (local) → Level 1 (merge) → Level 2 (release) |
| BANNED | `.Result`/`.Wait()` in async, `dynamic`, `catch (Exception) {}`, sentinel values |

## Contract

This ruleset is:
- Binding for humans
- Binding for AI agents
- Not subject to "interpretation"

Rule violations → output rejection.
