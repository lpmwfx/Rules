---
tags: [topology, laravel, blade, svelte, inertia, layers]
concepts: [laravel-topology, layer-mapping-laravel]
requires: [global/topology.md, global/topology-profiles.md, php/laravel/stacks.md]
related: [php/laravel/architecture.md, core/design.md, gateway/io.md]
keywords: [topology, layers, app, resources, controllers, actions, models, services, blade, svelte, inertia]
layer: 2
---
# Laravel Topology

> 6-layer mapping for Laravel projects — both Blade and Svelte stacks

---

## Stack 1 — Blade (admin/internal)

| Layer | Tag | Laravel mapping |
|---|---|---|
| ui | `_ui` | `resources/views/` — Blade templates (thin) |
| adapter | `_adp` | `app/Http/Controllers/` — receive, validate, call action, return |
| core | `_core` | `app/Actions/`, `app/Enums/`, `app/Data/` — business logic |
| gateway | `_gtw` | `app/Models/` (Eloquent), `app/Services/` (external APIs) |
| pal | — | Not needed — Laravel IS the platform |
| shared | `_x` | `app/Support/` — cross-layer types, error enums |

## Stack 2 — Svelte (user-facing)

| Layer | Tag | Laravel + Svelte mapping |
|---|---|---|
| ui | `_ui` | `resources/js/Pages/`, `resources/js/Components/`, `resources/js/Layouts/` |
| adapter | `_adp` | Inertia bridge: controllers return props → Svelte receives them |
| core | `_core` | `app/Actions/`, `app/Enums/`, `app/Data/` — same as Stack 1 |
| gateway | `_gtw` | `app/Models/` (Eloquent), `app/Services/` (external APIs) |
| pal | — | Not needed — Laravel IS the platform |
| shared | `_x` | `app/Support/` — cross-layer types, error enums |

## Key Difference

In Stack 1, adapter (controllers) returns HTML via Blade. In Stack 2, adapter (controllers) returns JSON props via Inertia — Svelte renders.

RULE: Controllers are adapter — they transform, not decide
RULE: Actions are core — business logic lives here, not in controllers or models
RULE: Eloquent models are gateway — they touch the database
RULE: Laravel itself is the platform — no separate PAL layer needed
