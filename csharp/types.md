---
tags: [types, records, nullable, generics]
concepts: [type-safety, immutability, nullable-reference-types]
requires: [global/validation.md]
keywords: [record, struct, nullable, generic, value-type]
layer: 3
---
# Type Safety

> Records for data, nullable always on, strong typing everywhere

---

RULE: Enable nullable reference types globally — `<Nullable>enable</Nullable>` in every `.csproj`
RULE: `record` for immutable data transfer objects and value objects
RULE: `struct` / `readonly struct` for small value types with no identity
RULE: Newtype pattern via `record struct` for distinct IDs
RULE: `T?` for nullable values — never sentinel values (`-1`, `""`, `null` object patterns)
RULE: Generics with constraints instead of `object`

```csharp
// GOOD: Newtype for type safety
public readonly record struct UserId(Guid Value);
public readonly record struct ProjectId(Guid Value);

// Can't accidentally mix them
public Task<User?> GetUser(UserId id) { ... }

// GOOD: Explicit nullable
public User? FindUser(string name) { ... }

// BAD: Sentinel value
public User FindUser(string name) { ... }  // returns "empty" user if not found

// GOOD: Record for immutable data
public record Config(string Host, int Port, TimeSpan Timeout);

// GOOD: Generic constraint
public T Load<T>(string path) where T : class, new() { ... }
```

BANNED: Nullable reference types disabled (`#nullable disable` without explicit reason)
BANNED: `dynamic` — use proper generics or interfaces
BANNED: Sentinel values (`-1`, `""`, `new User()` as "not found")
BANNED: `object` as function parameter or return type — use generics or interfaces
BANNED: Mutable public properties on records used as value objects
BANNED: `var` when the type is not obvious from the right-hand side

## Null Safety Pattern

```csharp
// GOOD: Null-conditional + null-coalescing
var name = user?.Profile?.DisplayName ?? "Anonymous";

// GOOD: Pattern matching
if (result is { IsSuccess: true, Value: var config })
    Apply(config);
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
