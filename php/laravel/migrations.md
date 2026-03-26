---
tags: [laravel, migrations, database, schema]
concepts: [schema-management, data-integrity, immutability]
requires: [php/laravel/eloquent.md, php/laravel/state-flow.md]
keywords: [migration, schema, seeder, unique-constraint, revision, event-log]
layer: 4
---
# Migrations & Schema

> All schema changes through migrations — immutable revisions, append-only events

---

RULE: All schema changes must be implemented through Laravel migrations
RULE: Article revisions must be immutable — no updates, only new rows
RULE: Event logs must be append-only where practical
RULE: Domain + locale + slug must be unique (composite unique constraint)

```php
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('articles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('domain_id')->constrained();
            $table->string('slug');
            $table->string('locale', 5);
            $table->string('title');
            $table->text('body_markdown');
            $table->text('body_html')->nullable();
            $table->string('state')->default(ArticleState::Draft->value);
            $table->timestamp('published_at')->nullable();
            $table->timestamps();

            $table->unique(['domain_id', 'locale', 'slug']);
        });

        Schema::create('article_revisions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('article_id')->constrained()->cascadeOnDelete();
            $table->text('body_markdown');
            $table->text('body_html');
            $table->json('metadata')->nullable();
            $table->timestamp('created_at');
            // No updated_at — revisions are immutable
        });

        Schema::create('article_events', function (Blueprint $table) {
            $table->id();
            $table->foreignId('article_id')->constrained()->cascadeOnDelete();
            $table->string('type');       // published, paused, updated, etc.
            $table->json('payload')->nullable();
            $table->timestamp('created_at');
            // No updated_at — events are append-only
        });
    }
};
```

BANNED: Schema changes outside migrations
BANNED: Updating revision rows — create new revision instead
BANNED: Deleting event log entries in normal operation
