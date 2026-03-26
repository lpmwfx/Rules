---
tags: [laravel, architecture, actions, controllers, structure]
concepts: [thin-controllers, actions-pattern, single-responsibility, project-structure]
requires: [php/laravel/README.md, php/modules.md]
feeds: [php/laravel/eloquent.md, php/laravel/services.md]
keywords: [action, service, controller, thin-controller, monolith, god-class]
layer: 3
---
# Architecture

> Thin controllers, dedicated Actions, clear layers — no clever abstractions

---

## Controller Responsibility

A controller does exactly four things:

1. Receive request
2. Validate via FormRequest
3. Call an Action or Service
4. Return response

RULE: Controllers must remain thin and contain no business logic
RULE: Controllers may not access raw input arrays when a validated request object exists

```php
declare(strict_types=1);

final class ArticleIngestController extends Controller
{
    public function store(
        StoreArticleRequest $request,
        UpsertArticleAction $action,
    ): JsonResponse {
        $article = $action->execute($request->validated());
        return response()->json($article, 201);
    }
}
```

## Actions Pattern

One use case = one Action class. Explicit naming, single responsibility.

RULE: Business use cases must be implemented in dedicated Action classes
RULE: One class, one responsibility — no god classes

```php
// Good — each action does one thing
app/Actions/Articles/
├── UpsertArticleAction.php
├── PublishArticleAction.php
├── PauseArticleAction.php
├── DeleteArticleAction.php
├── ReplaceArticleAction.php
└── ScheduleArticleAction.php

app/Actions/Domains/
└── ResolveDomainByHostAction.php

app/Actions/Rendering/
└── ResolveRenderableArticleAction.php
```

## Project Structure

```text
app/
  Actions/          — business use cases, one per class
    Articles/
    Domains/
    Rendering/
  Data/             — DTOs, value objects
  Enums/            — typed enums (ArticleState, etc.)
  Http/
    Controllers/
      Api/          — API endpoints
      Web/          — server-rendered endpoints
    Requests/       — FormRequest validation classes
      Api/
  Models/           — Eloquent models (data + relations + scopes)
  Policies/         — authorization (when needed)
  Services/         — technical helpers
    Markdown/
    Sanitization/
    Routing/
  ViewModels/       — complex view data preparation
  Support/          — shared utilities (minimal)
```

RULE: The application must remain a single Laravel monolith in the first version
RULE: Prefer explicit names over smart abstractions
RULE: Prefer straightforward query logic over premature generalization

BANNED: Business logic inside controllers
BANNED: God classes — classes that handle multiple unrelated responsibilities
BANNED: Custom abstractions duplicating built-in Laravel behavior
BANNED: Custom framework layers on top of Laravel
BANNED: Premature microservice splitting
