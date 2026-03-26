---
tags: [laravel, init, setup, scaffold, installation]
concepts: [project-initialization, project-setup, bootstrap]
requires: [php/laravel/README.md, global/initialize.md]
feeds: [php/laravel/architecture.md, php/laravel/services.md]
keywords: [laravel, inertia, livewire, svelte, tailwind, vite, typescript, composer, npm, setup]
layer: 2
---
# Laravel Project Initialization

> Full setup sequence — from `laravel new` to first commit with proj/ files

---

VITAL: Run this ONCE per project — not every session (that is startup.md)
VITAL: Do not skip steps — each step feeds the next

## Stack Options

Pick what you need — all are compatible but independent:

| Component | Purpose | When to use |
|-----------|---------|-------------|
| **Laravel 11+** | PHP framework | Always |
| **Inertia.js** | SPA without API — server-driven, client-rendered | When you want SPA feel with Laravel routing |
| **Livewire 3** | Server-side reactivity — no JS needed | When you want interactive Blade without JS |
| **Svelte 5** | Frontend framework via Inertia adapter | When using Inertia + prefer Svelte over React/Vue |
| **TypeScript** | Type-safe frontend | When using Inertia + Svelte/React/Vue |
| **Tailwind CSS 4** | Utility-first CSS | Almost always |
| **Vite** | Build tool | Always (Laravel default since v9) |

RULE: Pick Inertia OR Livewire as primary — not both for the same feature
RULE: Livewire for server-heavy pages, Inertia+Svelte for rich interactive UI
RULE: Vite is always present — it ships with Laravel

---

## 1. Create Laravel Project

```bash
composer create-project laravel/laravel project-name
cd project-name
```

Or with the Laravel installer:

```bash
laravel new project-name
cd project-name
```

## 2. Install Stack Components

### Tailwind CSS 4 (recommended — almost always)

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

### Inertia.js + Svelte 5 + TypeScript

```bash
# Server-side
composer require inertiajs/inertia-laravel

# Client-side — Svelte 5 adapter
npm install @inertiajs/svelte
npm install -D svelte @sveltejs/vite-plugin-svelte typescript
```

Publish Inertia middleware:
```bash
php artisan inertia:middleware
```

Register in `bootstrap/app.php`:
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

`vite.config.js` (add Svelte plugin):
```js
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
    plugins: [
        laravel({ input: ['resources/css/app.css', 'resources/js/app.ts'] }),
        tailwindcss(),
        svelte(),
    ],
});
```

`tsconfig.json`:
```json
{
    "compilerOptions": {
        "target": "ESNext",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "strict": true,
        "jsx": "preserve",
        "types": ["vite/client"],
        "paths": { "@/*": ["./resources/js/*"] },
        "baseUrl": "."
    },
    "include": ["resources/js/**/*.ts", "resources/js/**/*.svelte"]
}
```

### Livewire 3 (alternative/complement to Inertia)

```bash
composer require livewire/livewire
```

No extra JS setup — Livewire injects its scripts automatically.

```bash
# Create a component
php artisan make:livewire Counter
```

### Additional Recommended Packages

```bash
# Dev tools
composer require --dev laravel/pint          # PHP CS Fixer (PSR-12)
composer require --dev larastan/larastan     # PHPStan for Laravel
composer require --dev pestphp/pest          # Modern testing
composer require --dev pestphp/pest-plugin-laravel

# Initialize Pest
./vendor/bin/pest --init

# Production
composer require laravel/sanctum             # API auth (if API needed)
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

---

## 3. Directory Structure

After installation, create the project structure from architecture.md:

```bash
mkdir -p app/Actions/Articles
mkdir -p app/Actions/Domains
mkdir -p app/Actions/Rendering
mkdir -p app/Data
mkdir -p app/Enums
mkdir -p app/Http/Controllers/Api
mkdir -p app/Http/Controllers/Web
mkdir -p app/Http/Requests/Api
mkdir -p app/Services/Markdown
mkdir -p app/Services/Sanitization
mkdir -p app/ViewModels
mkdir -p app/Support
```

Svelte pages (if using Inertia):
```bash
mkdir -p resources/js/Pages
mkdir -p resources/js/Components
mkdir -p resources/js/Layouts
```

---

## 4. Create proj/ Files

Run these in order — each step feeds the next.

### Step 0: Install hooks

```
mcp__rulestools__setup(".")
```

### Step 1: Create proj/PROJECT

```markdown
# PROJECT: project-name

## Goal
[2-5 sentences — what we want to achieve]

## Stack
- Language: PHP 8.2+, TypeScript 5
- Framework: Laravel 11
- Frontend: Inertia.js + Svelte 5 / Livewire 3
- CSS: Tailwind CSS 4
- Build: Vite
- DB: MySQL 8 / PostgreSQL 16 / SQLite
- Testing: Pest (PHP), Vitest (JS)
- Linting: Laravel Pint (PSR-12), Larastan level 8
- Server: [webhotel / VPS / Docker]

## Structure
- src: app/
- frontend: resources/js/
- views: resources/views/
- config: config/
- routes: routes/
- migrations: database/migrations/
- proj: proj/

## Method
- Workflow: PROJECT → FIXES → TODO → code → test → DONE
- Branching: feature branches, never commit to main
- Testing: pest, real database
- Deploy: [method]

## Patterns
- thin-controllers: Controllers do 4 things — receive, validate, call action, return
- actions-pattern: One Action class per business use case
- explicit-state: All state via enums, transitions in Actions
- dto-boundaries: FormRequest at edge, DTOs across layers

## Current
- phase: 1
- id: foundation
- status: development

## History
(empty — first phase)
```

### Step 2: Create proj/RULES

```markdown
# RULES: project-name

## Active Rules

### Always
- global/topology.md
- global/module-tree.md
- global/file-limits.md
- global/config-driven.md
- global/error-flow.md
- global/nesting.md

### Language: PHP
- php/README.md
- php/types.md
- php/naming.md
- php/error-handling.md
- php/safety.md
- php/modules.md

### Framework: Laravel
- php/laravel/README.md
- php/laravel/architecture.md
- php/laravel/eloquent.md
- php/laravel/state-flow.md
- php/laravel/validation.md
- php/laravel/routing.md
- php/laravel/blade.md
- php/laravel/migrations.md
- php/laravel/services.md
- php/laravel/artisan.md

### UI (Web)
- css/README.md
- js/README.md
- uiux/tokens.md
- uiux/components.md
- uiux/state-flow.md
- uiux/checklist.md

## Project Rules
(empty — AI adds conventions as discovered)

## Derived from FIXES
(empty — populated as bugs are fixed)
```

### Step 3: Create proj/PHASES

```markdown
# PHASES: project-name

## Active

- phase: 1
  id: foundation
  title: "Project foundation"
  milestone: "Core architecture in place, database seeded, one page renders"
  delivers:
    - Laravel project with stack installed
    - Database schema (migrations)
    - Authentication setup
    - First working page/endpoint
    - Pest test suite running
  status: active

## Planned

- phase: 2
  id: core-features
  title: "Core features"
  milestone: "Primary user workflow functional end-to-end"
  delivers:
    - CRUD operations
    - Business logic in Actions
    - Form validation via FormRequests
    - State management with enums
  status: planned

- phase: 3
  id: polish
  title: "Polish and deploy"
  milestone: "Production-ready and deployed"
  delivers:
    - Error handling
    - Performance (caching, eager loading)
    - Deploy pipeline
    - Documentation
  status: planned

# --- DONES ---
```

### Step 4: Create proj/TODO

```markdown
# TODO: Project foundation

phase: 1
id: foundation

## Setup

- id: 1
  task: Create Laravel project and install stack components
  pass: `php artisan serve` works, Vite compiles, Tailwind renders
  status: pending

- id: 2
  task: Create database migrations for core models
  pass: `php artisan migrate` runs clean, schema matches design
  status: pending

- id: 3
  task: Create Eloquent models with relationships, casts, and enums
  pass: Models have correct relations, ArticleState enum works
  status: pending

- id: 4
  task: Create first Action class and test
  pass: Pest test passes with real database
  status: pending

- id: 5
  task: Create first controller + route + page
  pass: Browser shows rendered page at correct URL
  status: pending

## Quality

- id: 6
  task: Configure Pint (PSR-12) and Larastan (level 8)
  pass: `./vendor/bin/pint --test` and `./vendor/bin/phpstan` pass clean
  status: pending

## Blockers
(none)
```

### Step 5: Create proj/FIXES

```markdown
# FIXES: project-name

(empty — populated as issues are resolved)
```

### Step 6: Create proj/UIUX

```markdown
# UIUX: project-name

## Goal
[What the user experience should feel like — 2-4 sentences]

## Platform
- OS: Web (all browsers)
- Frontend: Inertia.js + Svelte 5 / Livewire 3
- CSS: Tailwind CSS 4
- Icons: Heroicons / Lucide

## UI Foundation Rules

| Rule | What it enforces |
|------|-----------------|
| uiux/tokens.md | Named design tokens — no literal values |
| uiux/components.md | One component per file |
| uiux/state-flow.md | Props down, events up |
| uiux/checklist.md | Pre-ship verification |
| css/README.md | Tailwind utility-first |

## UI Architecture
- Entry: resources/js/app.ts (Inertia) / resources/views/ (Blade+Livewire)
- Pages: resources/js/Pages/ (Svelte — one per route)
- Components: resources/js/Components/ (reusable Svelte components)
- Layouts: resources/js/Layouts/ (page shells)
- Blade: resources/views/ (Livewire components, layout, email)

## Component Conventions
(empty — AI adds as patterns emerge)

## User Flows

### Primary Flow: [Name]
1. User does X → sees Y
2. ...

## Layout

### Main Layout
- Nav: top bar with navigation
- Content: centered max-width container
- Footer: minimal

## Interaction Patterns
- Loading: skeleton / spinner — never block the whole view
- Errors: toast for transient, inline for validation, full page for 404/500
- Forms: validate on blur, submit on Enter, disable button while loading
- Modals: confirm before destructive actions

## Accessibility
- All interactive elements reachable by keyboard
- Tab order follows visual order
- Focus ring always visible
- Minimum contrast: 4.5:1 text, 3:1 UI
```

### Step 7: Create proj/INSTALL

```markdown
# INSTALL: project-name

## Requirements
- PHP 8.2+
- Composer 2
- Node.js 20+ / npm 10+
- MySQL 8 / PostgreSQL 16 / SQLite

## Setup

```bash
git clone <repo-url>
cd project-name
composer install
npm install
cp .env.example .env
php artisan key:generate
php artisan migrate
npm run dev        # Vite dev server
php artisan serve  # Laravel dev server
```

## Test

```bash
./vendor/bin/pest                  # PHP tests
./vendor/bin/pint --test           # Code style
./vendor/bin/phpstan analyse       # Static analysis
npm run build                      # Frontend build check
```

## Deploy
[deployment method — forge, rsync, Docker, etc.]

## Publish
- Registry: N/A (web application)
- Verify: no proj/ in deploy, no .env secrets exposed
```

---

## 5. Verification

After all proj/ files are created:

```
1. php artisan serve           → Laravel boots
2. npm run dev                 → Vite compiles
3. Browser → http://localhost:8000  → page renders
4. ./vendor/bin/pest           → tests pass
5. ./vendor/bin/pint --test    → code style clean
6. Read proj/PROJECT           → all sections filled
7. Read proj/TODO              → phase matches PROJECT
```

RULE: All proj/ files are created in one session — do not leave initialization partial
RULE: proj/PROJECT.Current.phase must be "1" after initialization
BANNED: Skipping proj/ file creation — all 7 files are mandatory for GUI projects
BANNED: Installing all stack options blindly — pick what the project needs
