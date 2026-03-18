---
tags: [csharp, docs, xml-comments, api-documentation]
concepts: [xml-doc-comments, public-api-documentation, summary-param-returns]
requires: [csharp/types.md]
feeds: [csharp/verification.md]
related: [rust/docs.md, python/docs.md, cpp/docs.md]
keywords: [summary, param, returns, exception, cref, xml-doc, triple-slash]
layer: 4
---
# Documentation

> `///` XML doc comments on every public member — summary, params, returns, exceptions

---

RULE: `/// <summary>` on every public type and member — no undocumented public API
RULE: `<param name="">` for all parameters — describe constraints and valid ranges
RULE: `<returns>` for non-void methods — describe what the caller receives
RULE: `<exception cref="">` for every exception the method can throw
RULE: Summary describes *why* and *what*, not restating the member name

```csharp
// GOOD: Complete XML doc
/// <summary>
/// Loads configuration from a TOML file and validates all required fields.
/// Returns a fail result if the file is missing or malformed.
/// </summary>
/// <param name="path">Absolute path to the TOML configuration file.</param>
/// <param name="ct">Cancellation token for async I/O.</param>
/// <returns>Parsed configuration or a fail result with error details.</returns>
/// <exception cref="StorageException">Thrown when disk I/O fails unexpectedly.</exception>
public async Task<Result<Config_cfg>> LoadAsync(string path, CancellationToken ct)

// BAD: Restates the name — adds no value
/// <summary>Loads the config.</summary>
public async Task<Result<Config_cfg>> LoadAsync(string path, CancellationToken ct)
```

BANNED: Undocumented public API — every `public` type, method, and property needs `<summary>`
BANNED: `<summary>` that restates the member name — "Gets the name" on `GetName()`
BANNED: Missing `<param>` tags when parameters exist
BANNED: `// TODO: add docs` as a substitute for actual documentation
