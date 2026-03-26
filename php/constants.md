---
tags: [constants, configuration, magic-numbers, enums]
concepts: [named-constants, configuration, immutability]
requires: [global/config-driven.md]
feeds: [php/types.md]
keywords: [const, enum, magic-number, hardcoded, define]
layer: 3
---
# Constants

> Named constants and enums — no magic values in method bodies

---

RULE: Class constants for domain-specific values (`private const MAX_RETRIES = 3`)
RULE: Enums for fixed value sets — not string/int constants
RULE: `UPPER_SNAKE` for constant names
RULE: No magic numbers or strings in method bodies

```php
declare(strict_types=1);

final class PaymentProcessor
{
    private const MAX_RETRIES = 3;
    private const TIMEOUT_SECONDS = 30;
    private const CURRENCY_PRECISION = 2;

    public function charge(Money $amount): PaymentResult
    {
        for ($i = 0; $i < self::MAX_RETRIES; $i++) {
            // ...
        }
    }
}

// Prefer enums over string constants
enum Currency: string
{
    case EUR = 'EUR';
    case USD = 'USD';
    case DKK = 'DKK';
}
```

BANNED: `define()` for new constants — use `const` or enum
BANNED: Magic numbers in method bodies
BANNED: Hardcoded URLs, paths, or credentials
