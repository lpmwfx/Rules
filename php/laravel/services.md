---
tags: [laravel, services, dependency-injection, container]
concepts: [service-container, dependency-injection, technical-services]
requires: [php/laravel/architecture.md]
keywords: [service, container, provider, facade, injection, markdown, sanitizer]
layer: 4
---
# Services & Dependency Injection

> DI over facades — services are technical helpers, not business logic

---

## Service vs Action

- **Action** = business use case (`PublishArticleAction`)
- **Service** = technical capability (`MarkdownRenderer`, `HtmlSanitizer`)

RULE: Dependency injection over facades in domain logic
RULE: Services are technical helpers — not business orchestration
RULE: No facades in core domain logic when DI is clearer

```php
declare(strict_types=1);

// Service — technical capability
final class MarkdownRenderer
{
    public function __construct(
        private readonly HtmlSanitizer $sanitizer,
    ) {}

    public function render(string $markdown): string
    {
        $html = $this->parseMarkdown($markdown);
        return $this->sanitizer->sanitize($html);
    }
}

// Action uses services via DI
final class UpsertArticleAction
{
    public function __construct(
        private readonly MarkdownRenderer $renderer,
    ) {}

    public function execute(ArticleData $data): Article
    {
        return Article::updateOrCreate(
            ['domain_id' => $data->domainId, 'locale' => $data->locale, 'slug' => $data->slug],
            [
                'title' => $data->title,
                'body_markdown' => $data->body,
                'body_html' => $this->renderer->render($data->body),
                'state' => $data->state,
            ],
        );
    }
}
```

## Service Providers

Register bindings only when the default auto-resolution isn't enough:

```php
// Only when interface binding is needed
$this->app->bind(HtmlSanitizerInterface::class, HtmlSanitizer::class);
```

## Laravel Features to Use

- Service container auto-resolution
- Constructor injection everywhere
- Config system for service configuration
- `env()` only inside config files

BANNED: Overuse of facades in core domain logic
BANNED: Large static helper classes
BANNED: Random `helpers.php` with unstructured global functions
BANNED: "Utility" classes with 40 mixed methods
BANNED: Direct use of `env()` outside config files
BANNED: No repository abstraction without a concrete need
