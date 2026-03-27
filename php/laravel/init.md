---
tags: [laravel, init, setup, scaffold, installation]
concepts: [project-initialization, project-setup, bootstrap]
requires: [php/laravel/README.md, global/initialize.md, php/laravel/stacks.md]
feeds: [php/laravel/init-install.md, php/laravel/init-proj.md]
keywords: [laravel, init, new project, setup, scaffold]
layer: 2
---
# Laravel Project Initialization

> Entry point — choose stack, install, create proj/ files

---

VITAL: Run this ONCE per project — not every session (that is startup.md)
VITAL: Do not skip steps — each step feeds the next

## Sequence

```
1. Choose stack        → stacks.md (Blade or Svelte)
2. Install             → init-install.md (composer, npm, config)
3. Create proj/ files  → init-proj.md (PROJECT, RULES, TODO, etc.)
4. Verify              → php artisan serve + npm run dev + pest
```

RULE: All steps are completed in one session — do not leave initialization partial
RULE: Stack choice (step 1) determines which install path to follow
BANNED: Skipping stack choice — decide Blade or Svelte before installing anything
BANNED: Installing all stack options blindly — pick what the project needs
