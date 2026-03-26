---
tags: [laravel, routing, middleware, api, controllers]
concepts: [route-model-binding, middleware, api-structure]
requires: [php/laravel/architecture.md]
feeds: [php/laravel/validation.md]
keywords: [route, middleware, api, web, route-model-binding, auth]
layer: 4
---
# Routing & Middleware

> Route model binding where it helps, middleware for cross-cutting concerns

---

RULE: Route model binding — but only where it doesn't hide important domain logic
RULE: API authentication must be handled by middleware
RULE: External systems may never write directly to the database
RULE: Separate API and Web route groups with appropriate middleware stacks

```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/articles', [ArticleIngestController::class, 'store']);
    Route::put('/articles/{article}', [ArticleIngestController::class, 'update']);
    Route::post('/articles/{article}/publish', [ArticlePublicationController::class, 'publish']);
    Route::post('/articles/{article}/pause', [ArticlePublicationController::class, 'pause']);
});

// routes/web.php
Route::get('/{slug}', [ArticleController::class, 'show'])
    ->where('slug', '[a-z0-9-]+');
```

## Middleware

Use built-in middleware and write custom middleware only for domain-specific cross-cutting concerns:

```php
// Domain resolution middleware
final class ResolveDomain
{
    public function handle(Request $request, Closure $next): Response
    {
        $domain = Domain::where('host', $request->getHost())->firstOrFail();
        $request->attributes->set('domain', $domain);

        return $next($request);
    }
}
```

RULE: Domain resolution must be configuration-driven, never folder-driven

## Laravel Features to Use

- Route model binding
- FormRequest validation
- Middleware stacks
- Rate limiting
- Route caching in production

BANNED: Business logic in middleware — only cross-cutting concerns
BANNED: Domain-as-folder architecture
