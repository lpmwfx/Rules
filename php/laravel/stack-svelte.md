---
tags: [laravel, svelte, inertia, stack, pwa, fullstack, js, ts]
concepts: [client-server-separation, inertia-bridge, pwa, frontend-backend-boundary]
requires: [php/laravel/stacks.md, php/laravel/architecture.md, global/tools-and-scripts.md]
feeds: [php/laravel/init-install.md]
related: [js/modules.md, js/project-structure.md, php/laravel/routing.md, global/topology.md, devops/dev-environment.md]
keywords: [svelte, inertia, pwa, webassembly, typescript, javascript, node, bun, deno, ssr, spa]
layer: 3
---
# Stack 2 — Laravel + Inertia + Svelte

> Svelte owns the UI, Laravel owns the server, Inertia is the bridge

---

## When to Use

All user-facing products: PWAs, websites, web apps. Svelte delivers the UI with full reactivity, offline capability, and modern web platform features. Laravel handles server-side logic, database, auth, queues.

RULE: All user-facing products use this stack

## Architecture

```
Browser (Svelte PWA)
  ↓ Inertia protocol (JSON props, no REST API needed)
Laravel
  ├── Routes → Controllers → Inertia::render()
  ├── Actions (business logic)
  ├── Models (Eloquent)
  └── FormRequests (validation)
```

## The Boundary

Svelte and Laravel are separated by a clean boundary. Inertia eliminates the need to build a manual API — controllers return props, Svelte pages receive them.

RULE: Svelte owns all UI rendering — PHP never generates user-facing HTML in this stack
RULE: Laravel owns all server logic — data, auth, validation, jobs, queues
RULE: Inertia is the only bridge between Svelte and Laravel — no separate REST API for the frontend
RULE: Server-side logic stays in PHP — do not duplicate validation or business rules in JS

```php
// Laravel controller — returns props, not views
public function show(Article $article): \Inertia\Response
{
    return Inertia::render('Articles/Show', [
        'article' => $article->only('id', 'title', 'content', 'published_at'),
    ]);
}
```

```svelte
<!-- Svelte page — receives props from Inertia -->
<script>
    let { article } = $props();
</script>

<article>
    <h1>{article.title}</h1>
    {@html article.content}
</article>
```

## JS/TS Runtime

The frontend build uses Node, Bun, or Deno — none are excluded. Pick what fits the project. TypeScript is preferred for type safety across the Svelte codebase.

RULE: JS/TS runtime (Node, Bun, Deno) is a project choice — none are excluded

## PWA & Web Platform

Svelte delivers PWA capabilities: service workers, offline-first, installable apps, Web APIs. This is why Svelte wins over Blade for user-facing products.

RULE: User-facing products should target PWA where applicable

BANNED: PHP-rendered HTML for user-facing pages — Svelte handles all UI
BANNED: Building a separate REST API for Svelte when Inertia handles the data flow
BANNED: Duplicating server validation in the frontend
