---
tags: [csharp, errors, exceptions, result-pattern]
concepts: [error-handling, result-types, validation]
requires: [csharp/types.md, global/error-flow.md]
related: [rust/errors.md, kotlin/result-pattern.md]
keywords: [exception, result, oneOf, validation, try-catch]
layer: 3
---
# Error Handling

> Result types in domain code — exceptions only at system boundaries

---

RULE: Domain code returns `Result<T>` (or `OneOf<T, TError>`) — not exceptions
RULE: Exceptions for truly unexpected system failures only (I/O, DB unavailable)
RULE: Never catch-and-swallow — every catch has a named recovery action
RULE: See `global/error-flow.md` for taxonomy (Transient/UserError/SystemError/Bug)
RULE: Validation errors are domain results, not exceptions

```csharp
// GOOD: Result type in domain
public sealed record Result<T>
{
    public static Result<T> Ok(T value) => new OkResult(value);
    public static Result<T> Fail(string error) => new FailResult(error);

    public sealed record OkResult(T Value) : Result<T>;
    public sealed record FailResult(string Error) : Result<T>;
}

// GOOD: Domain operation returns Result
public Result<Config_cfg> LoadConfig(string path)
{
    if (!File.Exists(path))
        return Result<Config_cfg>.Fail($"Config not found: {path}");

    // parse ...
    return Result<Config_cfg>.Ok(parsed);
}

// GOOD: Exhaustive match at call site (no _ discard)
var display = LoadConfig(path) switch
{
    Result<Config_cfg>.OkResult ok   => Apply(ok.Value),
    Result<Config_cfg>.FailResult err => ShowError(err.Error),
};
```

## Exceptions — Allowed Patterns

```csharp
// GOOD: System boundary — let it propagate with context
public async Task<byte[]> ReadFileAsync(string path, CancellationToken ct)
{
    try
    {
        return await File.ReadAllBytesAsync(path, ct);
    }
    catch (IOException ex)
    {
        throw new StorageException($"Failed to read {path}", ex);
    }
}
```

BANNED: `catch (Exception ex) { }` — swallowing without recovery
BANNED: Exceptions for control flow (validation failures, not-found)
BANNED: `throw new Exception(...)` — use typed exception subclasses
BANNED: `NullReferenceException` as intentional design — use nullable types properly
BANNED: Wildcard catch that logs but does not recover or rethrow
