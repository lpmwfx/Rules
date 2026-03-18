---
tags: [csharp, constants, configuration, magic-numbers]
concepts: [compile-time-constants, runtime-constants, config-records]
requires: [global/config-driven.md]
feeds: [csharp/types.md]
related: [rust/constants.md, python/constants.md, js/constants.md, cpp/constants.md]
keywords: [const, static-readonly, magic-number, configuration, hardcoded]
layer: 3
---
# Constants

> `const` for compile-time, `static readonly` for runtime — no magic numbers

---

RULE: `const` for compile-time constants — primitives and strings known at build time
RULE: `static readonly` for runtime constants — `DateTime`, `TimeSpan`, complex objects
RULE: Constants grouped in dedicated `_cfg` record types — not scattered across classes
RULE: No magic numbers in method bodies — extract to named constant

```csharp
// GOOD: Config record with named constants
public static class Http_cfg
{
    public const int MaxRetries = 3;
    public const string DefaultMediaType = "application/json";
    public static readonly TimeSpan RequestTimeout = TimeSpan.FromSeconds(30);
    public static readonly TimeSpan RetryDelay = TimeSpan.FromMilliseconds(500);
}

// GOOD: Usage with named constant
var client = new HttpClient { Timeout = Http_cfg.RequestTimeout };

// BAD: Magic number in method body
var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };

// GOOD: Enum-like constants via static readonly
public static class StatusCodes_cfg
{
    public static readonly IReadOnlySet<int> Retryable =
        new HashSet<int> { 429, 502, 503, 504 };
}
```

BANNED: Hardcoded connection strings, paths, URLs, or timeouts in source code
BANNED: Magic numbers without named constant — every literal needs a name
BANNED: `const` for values that change between environments — use configuration
BANNED: Constants spread across unrelated classes — centralize in `_cfg` types
