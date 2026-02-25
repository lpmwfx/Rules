---
tags: [rust, types, enums, newtype]
concepts: [type-safety, type-checking]
requires: [global/validation.md]
related: [python/types.md, cpp/types.md]
keywords: [newtype, enum, derive, serde]
layer: 3
---
# Type Safety

> Newtype pattern, Option, slices — strong typing everywhere

---

RULE: Strong typing — newtype pattern for distinct IDs
RULE: `Option<T>` for nullable values (never sentinel values)
RULE: `&str` for string slices, `String` for owned strings
RULE: `&[T]` for slices, `Vec<T>` for owned arrays

```rust
// GOOD: Newtype for type safety
struct UserId(u64);
struct ProjectId(u64);

// Can't accidentally mix them
fn get_user(id: UserId) -> Option<User> { ... }

// GOOD: Explicit option
fn find_user(name: &str) -> Option<User> { ... }

// BAD: Sentinel value
fn find_user(name: &str) -> User { ... }  // returns "empty" user if not found
```

BANNED: `String` for paths (use `PathBuf`)
BANNED: `println!` for logging (use tracing)
BANNED: Global mutable state (use dependency injection)
