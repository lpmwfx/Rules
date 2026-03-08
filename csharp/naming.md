---
tags: [csharp, naming, conventions, layer-tag]
concepts: [naming-conventions, readability]
requires: [global/consistency.md, global/topology.md]
related: [rust/naming.md, python/naming.md, global/naming-suffix.md]
keywords: [pascal-case, camel-case, interface, layer-tag]
layer: 3
---
# Naming Rules

> Anti-variable-noise + layer-tag convention

---

## Overriding Principle

RULE: A name must explain WHY the variable exists — not just WHAT it contains

## Forbidden Names (without domain suffix)

BANNED: `data`, `info`, `value`, `item`, `object`, `temp`, `state`, `ctx`, `result`, `res`, `var`, `obj`

ALLOWED with domain: `paymentState`, `parseResult`, `requestContext`

## Lifecycle Names

RULE: Names must reflect phase:
- `*Input` — raw external input
- `*Parsed` — structured but unvalidated
- `*Validated` — semantically valid
- `*Resolved` — all references resolved
- `*Final` — ready for side-effects

## Scope Rules

RULE: Scope < 5 lines: short names ok (`i`, `id`, `len`)
RULE: Scope >= 5 lines: semantic names REQUIRED

## Collections

RULE: Plural MANDATORY for collections: `users`, `tokens`
RULE: Iterator uses role, not type: `foreach (var user in users)`

## Booleans

RULE: Must start with `is`, `has`, `can`, `should`

## Methods

RULE: Verbs first
RULE: No type-leak in name
BANNED: `GetUserData()` → GOOD: `LoadUser()`

## Layer-Tag Suffix

RULE: All types use a layer-tag suffix matching their architectural role
RULE: Tag = folder the type lives in — see [global/topology.md](../global/topology.md) for the canonical tag list
NOT: Computed codes, project-brand codes, or arbitrary suffixes
SCOPE: All types (classes, records, interfaces, enums) — local variables and private helpers excluded

## Standard Conventions

```csharp
namespace MyApp.Config;          // PascalCase namespaces

public record ConfigLoader_cfg;  // PascalCase types + layer-tag suffix
public interface IRepository_adp; // I-prefix for interfaces + layer-tag suffix

public void LoadConfig() { }     // PascalCase methods
public const int MaxRetries = 3; // PascalCase constants (NOT SCREAMING_SNAKE)

private readonly string _filePath; // _camelCase private fields
private string filePath;           // camelCase local variables and parameters
```

## Interface Prefix

RULE: Interfaces use `I` prefix: `IUserRepository_adp`, `IEventBus_x`
RULE: The layer-tag comes AFTER the I-prefixed name

BANNED: Concrete class named `ISomething` — that prefix is reserved for interfaces
