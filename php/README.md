---
tags: []
concepts: [php-rules]
related: [php/types.md, php/modules.md, php/naming.md, php/nesting.md, php/testing.md, php/safety.md, php/validation.md, global/module-tree.md]
layer: 6
---
# PHP Rules

> Strict-typed, PSR-compliant, tested PHP — 8.2+

---

## Philosophy

RULE: One class per file — PSR-4 autoloading, namespace maps to directory
RULE: Strict types declared — `declare(strict_types=1)` in every file
RULE: Stateless services — dependencies injected, no global state or singletons
RULE: Encapsulate behind visibility — nothing public unless part of the API contract

See: [global/module-tree.md](../global/module-tree.md)

## Files

| File | Topic |
|------|-------|
| [types.md](types.md) | Strict types, union types, enums |
| [modules.md](modules.md) | Namespaces, PSR-4 autoloading |
| [naming.md](naming.md) | PSR-12 naming conventions |
| [nesting.md](nesting.md) | Flat code, early returns |
| [error-handling.md](error-handling.md) | Exceptions, try-catch |
| [testing.md](testing.md) | PHPUnit, Pest, real databases |
| [validation.md](validation.md) | Input validation at boundaries |
| [safety.md](safety.md) | SQL injection, XSS, eval |
| [constants.md](constants.md) | Named constants, enums |
| [docs.md](docs.md) | PHPDoc conventions |
| [threading.md](threading.md) | Async, queues, Fibers |
| [quick-ref.md](quick-ref.md) | Quick reference table |

## Frameworks

| Directory | Topic |
|-----------|-------|
| [laravel/](laravel/README.md) | Laravel framework rules |
