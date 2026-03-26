---
tags: [laravel, framework]
concepts: [laravel-rules]
requires: [php/README.md]
related: [php/laravel/architecture.md, php/laravel/eloquent.md, php/laravel/state-flow.md, php/laravel/validation.md, php/laravel/routing.md, php/laravel/blade.md, php/laravel/migrations.md, php/laravel/testing.md, php/laravel/services.md, php/laravel/artisan.md]
layer: 6
---
# Laravel Rules

> Keep Laravel standard, boring, explicit, and use-case-driven — 11+

---

## Philosophy

RULE: Follow standard Laravel directory structure — don't fight the framework
RULE: Keep Laravel boring — standard is better than clever
RULE: Thin controllers — receive, validate, call action, return response
RULE: Business logic in dedicated Action classes — one use case per class
RULE: Models are data shape — relations, casts, simple scopes, nothing more
RULE: Dependency injection over facades in application code
RULE: Config via `.env` and config files — never hardcode environment-specific values
RULE: Monolith first — single Laravel project, one database, clear layers
RULE: All PHP rules from [php/](../README.md) apply — Laravel adds framework-specific conventions

## Files

| File | Topic |
|------|-------|
| [init.md](init.md) | Full setup sequence — install, stack, proj/ templates |
| [architecture.md](architecture.md) | Project structure, Actions, Services, thin controllers |
| [eloquent.md](eloquent.md) | Models, relationships, scopes — no fat models |
| [state-flow.md](state-flow.md) | Explicit state, enums, transitions |
| [validation.md](validation.md) | FormRequest, typed data objects |
| [routing.md](routing.md) | Route model binding, API vs Web, middleware |
| [blade.md](blade.md) | Server-rendered, no logic in views, sanitized output |
| [migrations.md](migrations.md) | Schema changes, immutable revisions, constraints |
| [testing.md](testing.md) | Laravel-specific testing |
| [services.md](services.md) | DI over facades, service classes |
| [artisan.md](artisan.md) | Jobs, scheduler, custom commands |
| [quick-ref.md](quick-ref.md) | Quick reference table |
