---
tags: [laravel, init, proj, project-files]
concepts: [project-files, project-state, initialization-templates]
requires: [php/laravel/init.md, php/laravel/architecture.md, project-files/project-file.md, project-files/todo-file.md, project-files/rules-file.md, project-files/fixes-file.md]
feeds: [php/laravel/services.md]
related: [project-files/install-file.md, project-files/uiux-file.md]
keywords: [proj, project, todo, rules, fixes, phases, uiux, install, templates]
layer: 2
---
# Laravel proj/ Templates

> Standard proj/ files for Laravel projects — create all in one session

---

VITAL: Fill in `[bracketed]` sections — do not leave placeholders

## proj/PROJECT

```markdown
# PROJECT: project-name

## Goal
[2-5 sentences]

## Stack
- Language: PHP 8.2+, TypeScript 5
- Framework: Laravel 11
- Frontend: [Blade / Inertia.js + Svelte 5]
- CSS: Tailwind CSS 4
- Build: Vite
- DB: [MySQL 8 / PostgreSQL 16 / SQLite]
- Testing: Pest (PHP), [Vitest (JS) — Stack 2 only]
- Linting: Laravel Pint (PSR-12), Larastan level 8

## Structure
- src: app/
- frontend: resources/js/
- views: resources/views/
- config: config/
- routes: routes/
- migrations: database/migrations/
- proj: proj/

## Patterns
- thin-controllers
- actions-pattern
- explicit-state
- dto-boundaries

## Current
- phase: 1
- id: foundation
- status: development
```

## proj/RULES

```markdown
# RULES: project-name

## Always
- global/topology.md
- global/module-tree.md
- global/file-limits.md
- global/tools-and-scripts.md

## PHP
- php/README.md
- php/types.md
- php/naming.md
- php/error-handling.md
- php/safety.md
- php/modules.md

## Laravel
- php/laravel/architecture.md
- php/laravel/stacks.md
- php/laravel/[stack-blade.md / stack-svelte.md]
- php/laravel/eloquent.md
- php/laravel/state-flow.md
- php/laravel/validation.md
- php/laravel/routing.md
- php/laravel/migrations.md

## UI (Stack 2 only)
- js/README.md
- js/project-structure.md
- css/README.md
- uiux/state-flow.md
- uiux/components.md
```

## proj/TODO

```markdown
# TODO: Project foundation

phase: 1
id: foundation

## Setup
- id: 1
  task: Create project and install stack
  pass: php artisan serve + npm run dev works
  status: pending

- id: 2
  task: Database migrations for core models
  pass: php artisan migrate runs clean
  status: pending

- id: 3
  task: Eloquent models with relations and enums
  pass: Models load, relations work
  status: pending

- id: 4
  task: First Action class and test
  pass: Pest test passes with real database
  status: pending

- id: 5
  task: First controller + route + page
  pass: Browser shows rendered page
  status: pending

## Quality
- id: 6
  task: Pint + Larastan clean
  pass: pint --test and phpstan pass
  status: pending
```

## proj/FIXES

```markdown
# FIXES: project-name

(empty — populated as issues are resolved)
```

## proj/PHASES

```markdown
# PHASES: project-name

## Active
- phase: 1
  id: foundation
  title: "Project foundation"
  milestone: "Core architecture in place, one page renders"
  status: active

## Planned
- phase: 2
  id: core-features
  title: "Core features"
  milestone: "Primary user workflow functional"
  status: planned

- phase: 3
  id: polish
  title: "Polish and deploy"
  milestone: "Production-ready"
  status: planned
```

## proj/INSTALL

```markdown
# INSTALL: project-name

## Requirements
- PHP 8.2+, Composer 2
- Node.js 20+ / Bun
- [MySQL 8 / PostgreSQL 16 / SQLite]

## Setup
git clone <repo> && cd project-name
composer install
npm install
cp .env.example .env
php artisan key:generate
php artisan migrate
npm run dev
php artisan serve

## Test
./vendor/bin/pest
./vendor/bin/pint --test
./vendor/bin/phpstan analyse

## Deploy
[method]
```

## proj/UIUX (GUI projects only)

See [project-files/uiux-file.md](../../project-files/uiux-file.md) for format.

RULE: Ask user before creating UIUX — confirm it is a GUI project
RULE: All proj/ files created in one session
RULE: proj/PROJECT.Current.phase must be "1" after initialization
