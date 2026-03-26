---
tags: [validation, input, boundaries]
concepts: [runtime-checking, boundaries, validation]
requires: [global/validation.md]
related: [php/types.md]
keywords: [filter-var, assert, dto, value-object]
layer: 4
---
# Input Validation

> Validate at system boundaries — typed DTOs everywhere

---

RULE: Validate at system boundaries (HTTP input, API responses, file I/O, config)
RULE: Use DTOs (Data Transfer Objects) for structured data from external sources
RULE: Value objects for domain primitives (`Email`, `Money`, `UserId`)
RULE: Never pass raw arrays across layer boundaries — wrap in typed objects

```php
declare(strict_types=1);

final readonly class CreateUserRequest
{
    public function __construct(
        public string $email,
        public string $name,
        public string $password,
    ) {}

    public static function fromArray(array $data): self
    {
        // Validate + construct — throws on invalid input
        $email = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);
        if ($email === false) {
            throw new ValidationException('Invalid email');
        }

        return new self(
            email: $email,
            name: trim($data['name'] ?? ''),
            password: $data['password'] ?? '',
        );
    }
}
```

BANNED: Raw `$_GET`, `$_POST`, `$_REQUEST` in business logic
BANNED: Passing unvalidated arrays across layer boundaries
BANNED: `filter_input()` deep inside business logic — validate at the edge
