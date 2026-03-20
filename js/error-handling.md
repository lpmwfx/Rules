---
tags: [typescript, error-handling, discriminated-union, exhaustive]
concepts: [typescript-error-union, exhaustive-check, error-recovery]
requires: [global/error-flow.md]
feeds: [js/safety.md]
related: [js/philosophy.md]
keywords: [AppError, discriminated-union, never, switch, exhaustive, kind, network_timeout, not_found, storage_full, invariant]
layer: 3
---
# TypeScript Error Handling Implementation

> Discriminated union with `never` exhaustiveness check — no unhandled cases

---

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

RULE: One `AppError` discriminated union per package boundary
RULE: `never` check in default arm — compile-time guarantee of exhaustive handling
RULE: Each variant's `kind` maps to a taxonomy class (Transient/UserError/SystemError/Bug)

RESULT: TypeScript compiler catches missing error cases before runtime
REASON: A `default: break` without `never` silently swallows new error variants


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
