---
tags: [laravel, eloquent, models, orm]
concepts: [data-models, relationships, scopes, no-fat-models]
requires: [php/laravel/architecture.md]
feeds: [php/laravel/state-flow.md, php/laravel/migrations.md]
keywords: [eloquent, model, relation, scope, cast, query-builder, repository-pattern]
layer: 3
---
# Eloquent Models

> Models = data shape + relations + simple scopes — nothing more

---

## Model Responsibility

RULE: Models must not contain complex domain workflows
RULE: Model = data shape + relations + casts + simple scopes
RULE: Business flow belongs in Action/Service classes, not models
RULE: Use Eloquent directly — no repository abstraction without concrete need

```php
declare(strict_types=1);

final class Article extends Model
{
    // Casts — type-safe attribute access
    protected $casts = [
        'state' => ArticleState::class,
        'published_at' => 'immutable_datetime',
        'metadata' => 'array',
    ];

    // Relations — data shape
    public function revisions(): HasMany
    {
        return $this->hasMany(ArticleRevision::class);
    }

    public function domain(): BelongsTo
    {
        return $this->belongsTo(Domain::class);
    }

    // Simple scopes — reusable query filters
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('state', ArticleState::Published);
    }

    public function scopeForDomain(Builder $query, Domain $domain): Builder
    {
        return $query->where('domain_id', $domain->id);
    }
}
```

## Query Patterns

Direct Eloquent queries are fine — no need to wrap them:

```php
// Good — direct, readable
$article = Article::query()
    ->published()
    ->forDomain($domain)
    ->where('slug', $slug)
    ->firstOrFail();

// Good — simple query in Action
$articles = Article::query()
    ->where('state', ArticleState::Scheduled)
    ->where('publish_at', '<=', now())
    ->get();
```

BANNED: Fat models with business workflow methods
BANNED: `Article::publishNowAndInvalidateCachesAndNotify()` — split into Actions
BANNED: Repository pattern unless there is a concrete need (e.g., swappable data source)
BANNED: Repository interfaces for standard database access
