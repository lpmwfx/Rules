---
tags: [global, error-handling, error-flow, recovery, crash-safety, graceful-degradation]
concepts: [error-taxonomy, recovery-strategy, graceful-degradation, user-feedback]
requires: [global/validation.md]
feeds: [rust/errors.md, js/safety.md, python/ack-pattern.md, kotlin/result-pattern.md, csharp/errors.md, global/error-messages.md, rust/error-handling.md, js/error-handling.md]
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

## Full Pipeline — Validation → Classification → Recovery

Validation (see global/validation.md) **prevents** errors. Error flow **handles** what gets through.
They are sequential stages in the same pipeline:

```
Input arrives
  │
  ▼
VALIDATE (global/validation.md)
  ├── Type check (design/build-time)    → catches shape errors before runtime
  ├── Lint check (build-time)           → catches pattern violations
  ├── Runtime validation (boundaries)   → catches invalid data at system edges
  │     └── Validation failure?         → UserError (bad input) or Bug (invariant broken)
  │
  ▼
CLASSIFY (this file)
  ├── Transient?    → retry with backoff → if still failing → SystemError path
  ├── UserError?    → show actionable message, stay valid
  ├── SystemError?  → disable subsystem, keep app running
  └── Bug?          → capture context, crash reporter, exit
  │
  ▼
RECOVER at Adapter boundary
  └── Translate to user-facing message (what failed + what to do)
```

RULE: Validation catches errors at boundaries BEFORE they enter the system — error flow handles what validation missed
RULE: When a third-party exception reaches your code, classify it: retryable? → Transient. User's fault? → UserError. Infrastructure down? → SystemError. Should never happen? → Bug

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

Per-language implementations: [rust/error-handling.md](../rust/error-handling.md) | [js/error-handling.md](../js/error-handling.md) | [csharp/errors.md](../csharp/errors.md)
User-facing and MCP messaging: [global/error-messages.md](error-messages.md)

BANNED: Wildcard `_ => {}` or `default: {}` error arm that does nothing
BANNED: `catch(e) {}` empty catch block
BANNED: `catch(e) { log(e) }` — logging without recovery is silent swallow
BANNED: Showing stack traces, internal paths, or raw error types to the user
BANNED: `unwrap()`/`expect()` in application code outside tests
BANNED: `throw new Error("something failed")` without a typed discriminated error
BANNED: Single catch-all error type — variants must be distinguishable for recovery
