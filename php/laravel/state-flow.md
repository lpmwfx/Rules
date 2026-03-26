---
tags: [laravel, state, enums, transitions, workflow]
concepts: [explicit-state, state-machine, domain-events]
requires: [php/laravel/eloquent.md, php/types.md]
feeds: [php/laravel/migrations.md]
keywords: [enum, state, transition, publish, schedule, ArticleState, explicit]
layer: 3
---
# Explicit State Flow

> State is always explicit — transitions are explicit — no hidden magic

---

RULE: State is always an explicit enum value — never inferred from timestamps
RULE: State transitions must be handled in application logic (Actions), never inferred from queries
RULE: Public visibility is determined by state + date rule — no hidden magic
RULE: Event logs should be append-only where practical

```php
declare(strict_types=1);

enum ArticleState: string
{
    case Draft = 'draft';
    case Scheduled = 'scheduled';
    case Published = 'published';
    case Paused = 'paused';
    case Archived = 'archived';
}
```

## Transitions in Actions

```php
final class PublishArticleAction
{
    public function execute(Article $article): Article
    {
        if ($article->state !== ArticleState::Draft
            && $article->state !== ArticleState::Scheduled) {
            throw new InvalidStateTransitionException(
                "Cannot publish from {$article->state->value}"
            );
        }

        $article->state = ArticleState::Published;
        $article->published_at = now();
        $article->save();

        // Append-only event log
        ArticleEvent::create([
            'article_id' => $article->id,
            'type' => 'published',
            'payload' => ['by' => auth()->id()],
        ]);

        return $article;
    }
}
```

BANNED: Implicit publication — "if `published_at` is set then maybe it's live"
BANNED: State inferred only from timestamps or nullable columns
BANNED: State transitions hidden in views or queries
BANNED: Business rules in Blade templates that determine publication state
