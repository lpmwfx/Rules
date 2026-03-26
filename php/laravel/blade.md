---
tags: [laravel, blade, rendering, views, templates]
concepts: [server-rendering, templating, view-safety, sanitization]
requires: [php/laravel/architecture.md]
related: [php/safety.md]
keywords: [blade, view, template, component, sanitize, xss, markdown, html]
layer: 4
---
# Blade Templates

> Views render already-decided data — no business logic, sanitized output

---

RULE: Public pages must be server-rendered with Blade in the first version
RULE: Views must not contain publication or authorization logic
RULE: Views only display already-decided data — all logic resolved before the view
RULE: Markdown must be converted to HTML through a dedicated service
RULE: Public HTML output must be sanitized before rendering
RULE: Theme behavior must be domain-configurable

```php
// Controller prepares everything — view just renders
public function show(Request $request, string $slug): View
{
    $domain = $request->attributes->get('domain');
    $article = $this->resolveAction->execute($domain, $slug);

    return view('article.show', [
        'title' => $article->title,
        'content' => $article->sanitizedHtml,  // already sanitized
        'theme' => $domain->theme,
    ]);
}
```

## Blade Components

Use Blade components with restraint:

```blade
{{-- Good — simple, data-driven --}}
<x-article-card :title="$article->title" :excerpt="$article->excerpt" />

{{-- Good — layout component --}}
<x-layouts.public :theme="$theme">
    <article>{!! $content !!}</article>
</x-layouts.public>
```

## ViewModels

When view data preparation becomes complex, use a ViewModel:

```php
final readonly class ArticleViewModel
{
    public function __construct(
        public string $title,
        public string $content,
        public string $publishedDate,
        public string $locale,
    ) {}

    public static function fromArticle(Article $article): self
    {
        return new self(
            title: $article->title,
            content: $article->sanitized_html,
            publishedDate: $article->published_at->format('d. M Y'),
            locale: $article->locale,
        );
    }
}
```

BANNED: Business rules in Blade (state checks, locale fallback, routing decisions)
BANNED: Complex conditionals in templates — resolve in controller/ViewModel
BANNED: Rendering unsanitized AI-generated HTML directly to public output
BANNED: Article files written to disk as primary source of truth — render from database
