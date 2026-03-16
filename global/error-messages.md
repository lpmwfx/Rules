---
tags: [global, error-messages, user-facing, mcp, error-reporting]
concepts: [user-facing-messages, mcp-error-messaging, error-translation]
requires: [global/error-flow.md]
related: [uiux/issue-reporter.md, global/adapter-layer.md]
keywords: [user-message, error-message, MCP, OK, WARN, ERROR, prefix, actionable, stack-trace, adapter-boundary]
layer: 2
---
# User-Facing and MCP Error Messages

> Translate internal errors to human-readable strings at the Adapter boundary

---

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

RESULT: Every error message tells the user what failed and what to do — never raw internals
REASON: An error the user cannot act on is worse than no message at all
