---
tags: [types, strict-types, enums, union-types]
concepts: [type-safety, type-declarations]
requires: [global/validation.md]
feeds: [php/validation.md, php/testing.md]
keywords: [declare-strict-types, union-type, intersection-type, enum, readonly]
layer: 3
---
# Type Safety

> `declare(strict_types=1)` in every file — no exceptions

---

RULE: `declare(strict_types=1)` — first statement in EVERY `.php` file
RULE: Full type declarations on all parameters, return types, and properties
RULE: Union types for nullable: `string|null` (NEVER omit the type)
RULE: Enums for fixed value sets — not string constants
RULE: `readonly` properties for immutable data
RULE: Constructor promotion for dependency injection

```php
declare(strict_types=1);

enum OrderStatus: string
{
    case Pending = 'pending';
    case Paid = 'paid';
    case Shipped = 'shipped';
    case Cancelled = 'cancelled';
}

final readonly class OrderData
{
    public function __construct(
        public int $id,
        public string $customerEmail,
        public OrderStatus $status,
        public float $total,
        public ?DateTimeImmutable $shippedAt = null,
    ) {}
}

function processOrder(OrderData $order): OrderResult
{
    // Full type safety — strict_types enforces at runtime
}
```

BANNED: Files without `declare(strict_types=1)`
BANNED: Missing return type declarations
BANNED: Untyped parameters on public methods
BANNED: String/int constants where an enum fits
BANNED: `mixed` type unless genuinely required
