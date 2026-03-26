---
tags: []
concepts: []
related: [php/types.md, php/modules.md, php/naming.md, php/testing.md, php/safety.md]
layer: 6
---
# PHP Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Strict types | `declare(strict_types=1)` in every file |
| PHP version | 8.2+ required |
| Naming | PSR-12: `PascalCase` classes, `camelCase` methods |
| Files | One class per file, PSR-4 autoloading |
| Nesting | Max 3 levels, early returns |
| Types | Full type declarations, enums for value sets |
| Errors | Custom exceptions, specific catches |
| Testing | PHPUnit/Pest, real databases, no mocks |
| Validation | DTOs at boundaries, value objects for primitives |
| Docs | PHPDoc on public API, skip when types suffice |
| Safety | No eval, parameterized SQL, escape output |
| Deps | Composer, PSR packages preferred |
| Linting | PHPStan level 8+, PHP CS Fixer (PSR-12) |
