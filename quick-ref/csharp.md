---
tags: [combo, csharp]
concepts: [quick-ref, project-type]
keywords: [csharp, dotnet, uno, c#]
requires: [global/quick-ref.md, csharp/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: C# Project

> C# CLI, library, or service. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | C#: 300 lines max. Split into partial class or child file | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Guard clauses. Early returns | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## C#-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Runtime | .NET 9 (LTS: .NET 8), C# 13 | [csharp/types.md](../csharp/types.md) |
| Nullable | `<Nullable>enable</Nullable>` in every project | [csharp/types.md](../csharp/types.md) |
| Types | `record` for data, `struct` for value types, newtype via `readonly record struct` | [csharp/types.md](../csharp/types.md) |
| Errors | `Result<T>` in domain, exceptions only at system boundaries | [csharp/errors.md](../csharp/errors.md) |
| Modules | One type per file, `internal` by default, `public` at assembly boundary | [csharp/modules.md](../csharp/modules.md) |
| Namespaces | File-scoped, matches folder path | [csharp/modules.md](../csharp/modules.md) |
| Async | `async Task` everywhere, `CancellationToken` on all public async methods | [csharp/threading.md](../csharp/threading.md) |
| LINQ | Method syntax, deferred — materialise only when needed | [csharp/types.md](../csharp/types.md) |
| Naming | PascalCase types/methods, `_camelCase` fields, `I`-prefix interfaces + layer-tag | [csharp/naming.md](../csharp/naming.md) |
| Verification | Level 0 (local) → Level 1 (merge) → Level 2 (release) | [csharp/verification.md](../csharp/verification.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | `dotnet build -warnaserror`, `dotnet test` |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all C# checks |

## BANNED

- `.Result`/`.Wait()` in async code — use `await`
- `dynamic` type
- `catch (Exception) {}` — empty catch blocks
- Sentinel values — use `Option<T>` or `Result<T>`
- Files over 300 lines
- Deep nesting (4+ levels)
- `utils/`, `helpers/`, `common/` folders
- Non-English code, comments, or identifiers

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`
