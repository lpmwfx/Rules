---
tags: [laravel, blade, stack, server-rendered, admin, dashboard]
concepts: [server-rendering, thin-views, internal-tools]
requires: [php/laravel/stacks.md, php/laravel/blade.md]
feeds: [php/laravel/routing.md]
keywords: [blade, admin, dashboard, crud, server-rendered, internal]
layer: 3
---
# Stack 1 — Laravel + Blade

> Pure PHP stack — server-rendered views for internal tools and admin backends

---

## When to Use

Projects where the UI is secondary to the server logic: admin panels, internal dashboards, status pages, simple CRUD interfaces. No JavaScript framework needed.

RULE: Blade stack is for projects where UI complexity does not justify a frontend framework

## Architecture

```
Browser
  ↓ HTTP (full page loads)
Laravel
  ├── Routes → Controllers → Views (Blade)
  ├── Actions (business logic)
  ├── Models (Eloquent)
  └── FormRequests (validation)
```

All rendering is server-side. Blade templates receive prepared data — no logic in views.

RULE: Views render already-decided data — all logic resolved before the template
RULE: Use ViewModels when view data preparation becomes complex

## Scope

- Server-rendered HTML via Blade
- Laravel auth, middleware, queues, jobs — full ecosystem
- Minimal JS only where strictly needed (e.g., Alpine.js for small interactions)
- No build step required for frontend

BANNED: Business logic in Blade templates
BANNED: Building user-facing products with this stack — use Stack 2
BANNED: Heavy JavaScript in Blade projects — if you need it, switch to Stack 2
