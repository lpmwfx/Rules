---
tags: [laravel, validation, form-request, dto]
concepts: [input-validation, form-request, typed-data]
requires: [php/laravel/architecture.md, php/validation.md]
keywords: [FormRequest, validated, rules, authorize, DTO, data-object]
layer: 4
---
# Validation

> FormRequest for all inbound data — no raw input in business logic

---

RULE: All inbound API/form payloads must use FormRequest validation
RULE: Controllers may not access raw input arrays when a validated request object exists
RULE: No untyped arrays passed deeply through the system — use DTOs or validated data objects

```php
declare(strict_types=1);

final class StoreArticleRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // handled by middleware
    }

    /**
     * @return array<string, mixed>
     */
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'max:255', 'regex:/^[a-z0-9-]+$/'],
            'body' => ['required', 'string'],
            'domain_id' => ['required', 'exists:domains,id'],
            'locale' => ['required', 'string', 'size:2'],
            'state' => ['sometimes', Rule::enum(ArticleState::class)],
        ];
    }
}
```

## DTOs for Deep Passing

When validated data needs to cross layer boundaries, wrap in a DTO:

```php
final readonly class ArticleData
{
    public function __construct(
        public string $title,
        public string $slug,
        public string $body,
        public int $domainId,
        public string $locale,
        public ArticleState $state = ArticleState::Draft,
    ) {}

    public static function fromRequest(StoreArticleRequest $request): self
    {
        $data = $request->validated();
        return new self(
            title: $data['title'],
            slug: $data['slug'],
            body: $data['body'],
            domainId: $data['domain_id'],
            locale: $data['locale'],
            state: ArticleState::tryFrom($data['state'] ?? '') ?? ArticleState::Draft,
        );
    }
}
```

BANNED: `$request->all()` or `$request->input()` when `$request->validated()` exists
BANNED: Raw `$_GET`, `$_POST` anywhere
BANNED: Passing unvalidated arrays deep into service/action layers
