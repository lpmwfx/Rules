---
tags: [laravel, init, install, composer, npm, vite, tailwind]
concepts: [installation, dependencies, stack-setup]
requires: [php/laravel/init.md, php/laravel/stacks.md, global/tools-and-scripts.md]
feeds: [php/laravel/init-proj.md, php/laravel/architecture.md]
related: [php/laravel/stack-blade.md, php/laravel/stack-svelte.md]
keywords: [composer, npm, vite, tailwind, inertia, svelte, livewire, pest, larastan, pint]
layer: 2
---
# Laravel Install

> Create project and install stack components

---

## 1. Create Project

```bash
composer create-project laravel/laravel project-name
cd project-name
```

## 2. Tailwind CSS 4 (both stacks)

```bash
npm install -D tailwindcss @tailwindcss/vite
```

`vite.config.js`:
```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [
        laravel({ input: ['resources/css/app.css', 'resources/js/app.ts'] }),
        tailwindcss(),
    ],
});
```

`resources/css/app.css`:
```css
@import "tailwindcss";
```

## 3a. Stack 1 — Blade Only

No extra frontend install needed. Livewire optional:

```bash
composer require livewire/livewire
```

RULE: Pick Livewire OR Inertia — not both for the same feature

## 3b. Stack 2 — Inertia + Svelte 5 + TypeScript

```bash
# Server-side
composer require inertiajs/inertia-laravel
php artisan inertia:middleware

# Client-side
npm install @inertiajs/svelte
npm install -D svelte @sveltejs/vite-plugin-svelte typescript
```

Register middleware in `bootstrap/app.php`:
```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        \App\Http\Middleware\HandleInertiaRequests::class,
    ]);
})
```

`resources/js/app.ts`:
```typescript
import { createInertiaApp } from '@inertiajs/svelte';
import { mount } from 'svelte';

createInertiaApp({
    resolve: (name: string) => {
        const pages = import.meta.glob('./Pages/**/*.svelte', { eager: true });
        return pages[`./Pages/${name}.svelte`];
    },
    setup({ el, App, props }) {
        mount(App, { target: el!, props });
    },
});
```

Add Svelte plugin to `vite.config.js`:
```js
import { svelte } from '@sveltejs/vite-plugin-svelte';
// add svelte() to plugins array
```

`tsconfig.json`:
```json
{
    "compilerOptions": {
        "target": "ESNext",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "strict": true,
        "types": ["vite/client"],
        "paths": { "@/*": ["./resources/js/*"] }
    },
    "include": ["resources/js/**/*.ts", "resources/js/**/*.svelte"]
}
```

## 4. Dev Tools (both stacks)

```bash
composer require --dev laravel/pint
composer require --dev larastan/larastan
composer require --dev pestphp/pest pestphp/pest-plugin-laravel
./vendor/bin/pest --init
```

`phpstan.neon`:
```neon
includes:
    - vendor/larastan/larastan/extension.neon
parameters:
    level: 8
    paths:
        - app/
```

## 5. Directory Structure

```bash
mkdir -p app/Actions app/Data app/Enums
mkdir -p app/Http/Controllers/Api app/Http/Controllers/Web
mkdir -p app/Http/Requests/Api
mkdir -p app/Services app/ViewModels app/Support
```

Stack 2 adds:
```bash
mkdir -p resources/js/Pages resources/js/Components resources/js/Layouts
```
