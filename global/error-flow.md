---
tags: [global, error-handling, error-flow, recovery, crash-safety, graceful-degradation]
concepts: [error-taxonomy, recovery-strategy, graceful-degradation, user-feedback]
requires: [global/validation.md]
feeds: [rust/errors.md, js/safety.md, python/ack-pattern.md, kotlin/result-pattern.md, csharp/errors.md]
related: [uiux/issue-reporter.md, global/persistent-state.md]
layer: 2
---
# Error Flow

> Classify -> match exhaustively -> recover or report — never crash silently

---

VITAL: Every error has a class — class determines the recovery strategy
VITAL: Match exhaustively — no wildcard arm that silently discards errors
VITAL: User-facing message at Adapter boundary — never a stack trace, never silence
RULE: Transient errors retry with backoff before escalating to SystemError path
RULE: UserErrors show actionable feedback — app stays in valid state
RULE: SystemErrors disable the affected feature — keep the app running
RULE: Bugs capture full context, invoke crash reporter, then exit cleanly

## Error Taxonomy

| Class | Cause | Recovery |
|-------|-------|----------|
| **Transient** | Network timeout, lock contention, rate-limit | Retry with backoff -> degrade |
| **UserError** | Invalid input, not found, permission denied | Show actionable message, stay valid |
| **SystemError** | Disk full, service down, resource exhausted | Disable feature, show degraded state |
| **Bug** | Invariant violated, assertion failed | Log full context -> crash reporter -> exit |

## App = Supervisor + Isolated Processes

RULE: Every subsystem (feature, background task, connection) runs inside its own error boundary
RULE: A failed subsystem is stopped and reported — it does not crash the app
RULE: The app is the supervisor — it keeps running and shows which subsystems are available
RULE: Subsystems expose a state: Running / Degraded / Failed — UI reflects this state

```
App (supervisor)
  |- FileWatcher     [Running]   -> wrapped in error boundary
  |- NetworkSync     [Failed]    -> caught, reported, disabled — app still runs
  |- RenderPipeline  [Running]   -> wrapped in error boundary
```

A subsystem that cannot run leaves the rest of the app intact. The user sees a degraded state for
that feature, not a crash.

## Recovery Flow

```
try operation
  Ok/success  -> use result
  Transient   -> retry N times (exponential backoff) -> if still failing -> SystemError path
  UserError   -> show message to user, return to valid state
  SystemError -> stop subsystem, mark as Failed, notify user, keep app running
  Bug         -> log full context, send to crash reporter, request restart
```

## Rust

Define one `AppError_x` enum per crate boundary. Each variant belongs to exactly one class.

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError_x {
    #[error("Network timeout")]
    NetworkTimeout,                          // Transient

    #[error("Not found: {0}")]
    NotFound(String),                        // UserError

    #[error("Storage unavailable")]
    StorageFull,                             // SystemError

    #[error("Internal error: {context}")]
    Invariant { context: String },           // Bug
}

// Adapter layer — exhaustive match, no _ wildcard
fn handle_result(result: Result<Data, AppError_x>, ui: &mut UIState) {
    match result {
        Ok(data)                               => ui.update(data),
        Err(AppError_x::NetworkTimeout)        => retry_or_degrade(ui),
        Err(AppError_x::NotFound(r))           => ui.show_empty(&r),
        Err(AppError_x::StorageFull)           => ui.show_degraded("Storage unavailable"),
        Err(AppError_x::Invariant { context }) => crash_reporter::report(&context),
        // No _ arm — compiler enforces all variants are handled
    }
}
```

## TypeScript

Use a discriminated union. TypeScript's exhaustiveness check via `never` catches unhandled cases at compile time.

```typescript
type AppError =
    | { kind: "network_timeout"; retryAfterMs: number }
    | { kind: "not_found";       resource: string }
    | { kind: "storage_full" }
    | { kind: "invariant";       context: string };

function recover(error: AppError, ui: UIAdapter): void {
    switch (error.kind) {
        case "network_timeout": scheduleRetry(error.retryAfterMs); return;
        case "not_found":       ui.showEmpty(error.resource);      return;
        case "storage_full":    ui.showDegraded("Storage full");   return;
        case "invariant":       crashReporter.send(error.context); return;
        default: {
            const _exhaustive: never = error; // compile error if a case is missing
            crashReporter.send(`Unhandled: ${JSON.stringify(_exhaustive)}`);
        }
    }
}
```

## C#

Sealed record hierarchy — one per assembly boundary. `when`-filters route exceptions to the correct
variant. Three output sinks: stdio (CLI/MCP), MCP string response, Uno Platform GUI.
See [csharp/errors.md](../csharp/errors.md) for full implementation.

```csharp
public abstract record AppError_x(string Message, Exception? Inner = null)
{
    public sealed record Transient(string Message, Exception? Inner = null)  : AppError_x(Message, Inner);
    public sealed record UserError(string Message, Exception? Inner = null)  : AppError_x(Message, Inner);
    public sealed record SystemError(string Message, Exception? Inner = null): AppError_x(Message, Inner);
    public sealed record Bug(string Message, string Context, Exception? Inner = null): AppError_x(Message, Inner);
}

// Adapter layer — exhaustive switch, no _ discard
void Handle(AppError_x error, IErrorSink_adp sink) =>
    sink.Report(error);   // sink routes to stdio / MCP / Uno GUI based on context

// Exception filter — routes to correct variant without nested ifs
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests)
    => sink.Report(new AppError_x.Transient("Rate limited", ex));
catch (HttpRequestException ex) when ((int?)ex.StatusCode >= 500)
    => sink.Report(new AppError_x.SystemError("API unavailable", ex));
```

## User-Facing Messages

Errors are internal types — translate to human-readable strings at the Adapter boundary.

```
internal:  AppError::NotFound("config.toml")
user sees: "Configuration file not found. Check Settings -> File Path."
```

Never show: stack traces, internal paths, raw error codes, or variant names.
Always show: what failed + what the user can do about it.

## MCP Tool Error Messaging

MCP tools return plain strings — structure the response so the AI agent can classify and act on it.

RULE: Prefix MCP error responses with `ERROR:`, `WARN:`, or `OK:` so callers can parse intent
RULE: Include what failed + what to do next — not just the exception message
RULE: `ERROR:` blocks the action (fix required); `WARN:` informs but does not block

```python
# MCP tool — structured error response
@mcp.tool()
def load_config(path: str) -> str:
    try:
        return f"OK: {read_config(path)}"
    except FileNotFoundError:
        return f"ERROR: Config not found at {path} — create the file or fix the path"
    except PermissionError:
        return f"ERROR: No read access to {path} — check file permissions"
    except ValueError as e:
        return f"ERROR: Config invalid — {e} — fix the syntax and retry"
```

The calling AI agent maps the prefix to the error taxonomy:
- `ERROR:` -> UserError or SystemError -> show to user, do not continue
- `WARN:`  -> Transient or advisory -> continue, note the warning
- `OK:`    -> success -> use the result

BANNED: Wildcard `_ => {}` or `default: {}` error arm that does nothing
BANNED: `catch(e) {}` empty catch block
BANNED: `catch(e) { log(e) }` — logging without recovery is silent swallow
BANNED: Showing stack traces, internal paths, or raw error types to the user
BANNED: `unwrap()`/`expect()` in application code outside tests
BANNED: `throw new Error("something failed")` without a typed discriminated error
BANNED: Single catch-all error type — variants must be distinguishable for recovery
