---
tags: [errors, exceptions, result-pattern, error-reporting, multi-channel]
concepts: [error-handling, result-types, validation, error-reporting, debug-notifications]
requires: [csharp/types.md, global/error-flow.md]
keywords: [exception, result, oneOf, validation, try-catch, when-filter, apperror, stdio, mcp, gui, appdomain, unhandled]
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

## AppError_x — Typed Error Hierarchy

RULE: One `AppError_x` hierarchy per assembly boundary — variants map to taxonomy classes
RULE: Use `when`-filters in catch blocks to route to the correct variant — no nested if/else

```csharp
// AppError_x — sealed record hierarchy, one per assembly
public abstract record AppError_x(string Message, Exception? Inner = null)
{
    public sealed record Transient(string Message, Exception? Inner = null)
        : AppError_x(Message, Inner);        // Retry with backoff

    public sealed record UserError(string Message, Exception? Inner = null)
        : AppError_x(Message, Inner);        // Show actionable feedback

    public sealed record SystemError(string Message, Exception? Inner = null)
        : AppError_x(Message, Inner);        // Disable feature, keep app running

    public sealed record Bug(string Message, string Context, Exception? Inner = null)
        : AppError_x(Message, Inner);        // Log + crash reporter + exit
}
```

```csharp
// GOOD: when-filter routes exception to correct taxonomy class — no nested ifs
try
{
    await CallApiAsync(ct);
}
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests)
{
    sink.Report(new AppError_x.Transient("Rate limited — retry shortly", ex));
}
catch (HttpRequestException ex) when ((int?)ex.StatusCode >= 500)
{
    sink.Report(new AppError_x.SystemError("API unavailable", ex));
}
catch (HttpRequestException ex)
{
    sink.Report(new AppError_x.UserError($"Request failed: {ex.Message}", ex));
}
finally
{
    // Cleanup always runs — close connections, release resources
    connection.Dispose();
}
```

## Multi-Channel Error Reporting

RULE: One `IErrorSink_adp` per output channel — injected, never hardcoded
RULE: Select sink at startup: stdio for CLI/MCP tools, GUI sink for Uno Platform

```csharp
// IErrorSink_adp — route errors to the right output channel
public interface IErrorSink_adp
{
    void Report(AppError_x error);
}

// StdioSink_adp — CLI / MCP tool context
public sealed class StdioSink_adp : IErrorSink_adp
{
    public void Report(AppError_x error)
    {
        var prefix = error switch
        {
            AppError_x.Transient   => "WARN",
            AppError_x.UserError   => "ERROR",
            AppError_x.SystemError => "ERROR",
            AppError_x.Bug         => "BUG",
        };
        Console.Error.WriteLine($"[{prefix}] {error.Message}");
        if (error.Inner is not null)
            Console.Error.WriteLine($"  caused by: {error.Inner.Message}");
    }
}

// McpSink_adp — structured MCP response (OK:/WARN:/ERROR: prefix per global/error-flow.md)
public sealed class McpSink_adp(Action<string> write) : IErrorSink_adp
{
    public void Report(AppError_x error)
    {
        var msg = error switch
        {
            AppError_x.Transient e   => $"WARN: {e.Message} — retry may help",
            AppError_x.UserError e   => $"ERROR: {e.Message} — fix input and retry",
            AppError_x.SystemError e => $"ERROR: {e.Message} — subsystem unavailable",
            AppError_x.Bug e         => $"ERROR: Internal error — {e.Context}",
        };
        write(msg);
    }
}

// GuiSink_adp — Uno Platform: DispatcherQueue → InfoBar notification
public sealed class GuiSink_adp(
    DispatcherQueue queue,
    Action<string, InfoBarSeverity> showNotification) : IErrorSink_adp
{
    public void Report(AppError_x error)
    {
        var (msg, severity) = error switch
        {
            AppError_x.Transient e   => (e.Message,                               InfoBarSeverity.Informational),
            AppError_x.UserError e   => (e.Message,                               InfoBarSeverity.Warning),
            AppError_x.SystemError e => (e.Message,                               InfoBarSeverity.Error),
            AppError_x.Bug e         => ($"Internal error — restart. ({e.Message})", InfoBarSeverity.Error),
        };
        queue.TryEnqueue(() => showNotification(msg, severity));
    }
}
```

## Global Exception Hooks

RULE: Wire global hooks in `Program.cs` / `App.xaml.cs` before any `await`
RULE: Both hooks report as `AppError_x.Bug` — these are always invariant violations

```csharp
// Program.cs — before app.Run() / Application.Start()
AppDomain.CurrentDomain.UnhandledException += (_, e) =>
{
    var ex = e.ExceptionObject as Exception;
    sink.Report(new AppError_x.Bug(
        "Unhandled exception",
        ex?.ToString() ?? e.ExceptionObject.ToString(),
        ex));
};

TaskScheduler.UnobservedTaskException += (_, e) =>
{
    sink.Report(new AppError_x.Bug(
        "Unobserved task exception",
        e.Exception.ToString(),
        e.Exception));
    e.SetObserved();   // prevents process termination — still reported as Bug
};
```
