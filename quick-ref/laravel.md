---
tags: [combo, laravel, php, svelte, inertia, livewire]
concepts: [quick-ref, project-type]
keywords: [laravel, php, inertia, livewire, svelte, tailwind, vite, typescript]
requires: [global/quick-ref.md, php/quick-ref.md, php/laravel/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: Laravel Project

> Laravel web application — Inertia/Svelte or Livewire, Tailwind, Vite. All rules at a glance.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| File limits | PHP: 350 lines max. Split into focused classes | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — config files + .env | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |

## PHP rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Strict types | `declare(strict_types=1)` in every file | [php/types.md](../php/types.md) |
| Naming | PSR-12: PascalCase classes, camelCase methods | [php/naming.md](../php/naming.md) |
| Modules | One class per file, PSR-4 autoloading | [php/modules.md](../php/modules.md) |
| Errors | Custom exceptions, specific catches | [php/error-handling.md](../php/error-handling.md) |
| Safety | No eval, parameterized SQL, escape output | [php/safety.md](../php/safety.md) |
| Testing | PHPUnit/Pest, real databases, no mocks | [php/testing.md](../php/testing.md) |
| Linting | Pint (PSR-12) + Larastan level 8 | [php/quick-ref.md](../php/quick-ref.md) |

## Laravel rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | Keep Laravel standard, boring, explicit | [php/laravel/README.md](../php/laravel/README.md) |
| Controllers | Thin — receive, validate, call action, return | [php/laravel/architecture.md](../php/laravel/architecture.md) |
| Actions | One use case per class, explicit naming | [php/laravel/architecture.md](../php/laravel/architecture.md) |
| Models | Data shape + relations + scopes only | [php/laravel/eloquent.md](../php/laravel/eloquent.md) |
| State | Explicit enums, transitions in Actions | [php/laravel/state-flow.md](../php/laravel/state-flow.md) |
| Validation | FormRequest always, DTOs across layers | [php/laravel/validation.md](../php/laravel/validation.md) |
| Views | No business logic, sanitized output | [php/laravel/blade.md](../php/laravel/blade.md) |
| Migrations | All schema changes, immutable revisions | [php/laravel/migrations.md](../php/laravel/migrations.md) |
| Services | Technical helpers via DI, not facades | [php/laravel/services.md](../php/laravel/services.md) |
| Jobs | Idempotent, single responsibility | [php/laravel/artisan.md](../php/laravel/artisan.md) |
| Setup | Full init sequence + proj/ templates | [php/laravel/init.md](../php/laravel/init.md) |

## Stack options

| Component | Install | When |
|-----------|---------|------|
| Tailwind 4 | `npm install -D tailwindcss @tailwindcss/vite` | Almost always |
| Inertia | `composer require inertiajs/inertia-laravel` + `npm install @inertiajs/svelte` | SPA feel, server routing |
| Svelte 5 | `npm install -D svelte @sveltejs/vite-plugin-svelte` | Rich interactive UI via Inertia |
| TypeScript | `npm install -D typescript` | Type-safe frontend |
| Livewire 3 | `composer require livewire/livewire` | Server-side reactivity |

## Verification

| Gate | Tools |
|------|-------|
| Code style | `./vendor/bin/pint --test` |
| Static analysis | `./vendor/bin/phpstan analyse` (level 8) |
| Tests | `./vendor/bin/pest` |
| Frontend | `npm run build` |
| Pre-commit | `rulestools check .` |

## BANNED

- Fat models — business logic belongs in Actions
- Repository pattern by default — Eloquent is the data layer
- Business logic in controllers or Blade
- Unsanitized HTML output
- Hidden state transitions — state must be explicit enum
- God classes — one responsibility per class
- Helper sprawl — no random helpers.php
- Custom framework on top of Laravel
- `env()` outside config files — config mediates env
- Facades in domain logic — use DI
- Files over 350 lines
- Hardcoded values in business logic
- `TODO`/`FIXME`/`HACK` in committed code

## Project files

Every project has `proj/` — see [php/laravel/init.md](../php/laravel/init.md) for complete
templates: PROJECT, RULES, PHASES, TODO, FIXES, UIUX, INSTALL.
