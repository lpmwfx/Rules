---
tags: []
concepts: []
related: [php/laravel/architecture.md, php/laravel/eloquent.md, php/laravel/state-flow.md, php/laravel/validation.md, php/laravel/blade.md]
layer: 6
---
# Laravel Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Philosophy | Keep Laravel standard, boring, explicit |
| Controllers | Thin — receive, validate, call action, return |
| Actions | One use case per class, explicit naming |
| Models | Data shape + relations + scopes only |
| State | Explicit enums, transitions in Actions |
| Validation | FormRequest always, DTOs across layers |
| Views | No business logic, sanitized output |
| Migrations | All schema changes, immutable revisions |
| Services | Technical helpers via DI, not facades |
| Jobs | Idempotent, single responsibility |
| Testing | Feature + unit, real database, factories |
| Structure | Monolith first, Actions/Services/Models split |

## Banned

| Pattern | Why |
|---------|-----|
| Fat models | Business logic belongs in Actions |
| Repository pattern (default) | Eloquent is the data layer |
| Business logic in controllers | Controllers are HTTP adapters |
| Logic in Blade | Views render decided data |
| Unsanitized HTML output | XSS risk |
| Hidden state transitions | State must be explicit |
| God classes | One responsibility per class |
| Helper sprawl | No random helpers.php |
| Custom framework on Laravel | Use the framework as-is |
| `env()` outside config | Config files mediate env access |
| Facades in domain logic | Use DI |
| Articles rendered from disk | Render from database state |
