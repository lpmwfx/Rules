---
tags: [laravel, artisan, jobs, scheduler, commands]
concepts: [queue-jobs, scheduler, cli-commands]
requires: [php/laravel/architecture.md, php/threading.md]
keywords: [artisan, job, scheduler, command, queue, ShouldQueue, dispatch]
layer: 4
---
# Jobs, Scheduler & Commands

> Jobs for async, scheduler for recurring, commands for CLI — all idempotent

---

RULE: Use Jobs for background and async work
RULE: Use scheduler for recurring tasks
RULE: Jobs must be idempotent — safe to retry
RULE: One job per class — single responsibility
RULE: Events only where there is a real domain event need — not for everything

```php
declare(strict_types=1);

// Job — idempotent, single responsibility
final class PublishScheduledArticlesJob implements ShouldQueue
{
    public function handle(): void
    {
        Article::query()
            ->where('state', ArticleState::Scheduled)
            ->where('publish_at', '<=', now())
            ->each(function (Article $article) {
                app(PublishArticleAction::class)->execute($article);
            });
    }
}

// Scheduler — in app/Console/Kernel.php or routes/console.php
Schedule::job(new PublishScheduledArticlesJob())->everyMinute();
```

## Custom Commands

```php
final class PurgeExpiredRevisionsCommand extends Command
{
    protected $signature = 'articles:purge-revisions {--days=90}';
    protected $description = 'Remove article revisions older than N days';

    public function handle(): int
    {
        $days = (int) $this->option('days');
        $count = ArticleRevision::where('created_at', '<', now()->subDays($days))->delete();

        $this->info("Purged {$count} revisions older than {$days} days.");
        return self::SUCCESS;
    }
}
```

## Laravel Features to Use

- Job middleware (rate limiting, preventing overlaps)
- Scheduler
- Queue workers with retry/backoff
- Artisan commands with proper signatures

BANNED: Long-running tasks in HTTP request cycle
BANNED: Events used as a general-purpose pub/sub when a direct Action call is clearer
