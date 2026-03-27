---
tags: [laravel, stacks, architecture, blade, svelte, inertia]
concepts: [stack-selection, server-client-separation, project-type]
requires: [php/laravel/architecture.md]
feeds: [php/laravel/stack-blade.md, php/laravel/stack-svelte.md]
keywords: [stack, blade, svelte, inertia, pwa, admin, dashboard, fullstack]
layer: 2
---
# Stacks

> Two stacks, never mixed — project type determines the stack

---

## Stack 1 — Laravel + Blade

Server-rendered. For internal tools, admin panels, status dashboards, simple CRUD backends where a full frontend framework is overkill.

RULE: Stack 1 is for server-side tools and internal dashboards — not user-facing products

See [stack-blade.md](stack-blade.md).

## Stack 2 — Laravel + Inertia + Svelte

Full-stack with client-side UI. For all user-facing products: PWAs, websites, apps. Svelte owns the UI, Laravel owns the server, Inertia is the bridge.

RULE: Stack 2 is for all user-facing products — PWA, websites, apps

See [stack-svelte.md](stack-svelte.md).

## Selection

| Signal | Stack |
|--------|-------|
| Internal tool / admin panel | 1 — Blade |
| Simple CRUD backend | 1 — Blade |
| User-facing website | 2 — Svelte |
| PWA / offline-capable | 2 — Svelte |
| Rich interactive UI | 2 — Svelte |

RULE: A project uses exactly one stack — never mix Blade UI and Svelte UI in the same project
BANNED: Mixing Stack 1 and Stack 2 in the same project
