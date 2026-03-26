---
tags: [naming, conventions, psr-12]
concepts: [naming-conventions, readability]
requires: [global/consistency.md]
related: [global/naming-suffix.md]
layer: 3
---
# Naming Conventions

> PSR-12 naming — consistent across PHP codebase

---

RULE: Classes: `PascalCase` (`UserService`, `InvoiceRepository`)
RULE: Methods: `camelCase` (`getUser`, `validateInput`, `processPayment`)
RULE: Functions: `snake_case` for standalone functions (`array_flatten`, `str_slug`)
RULE: Variables: `$camelCase` (`$userId`, `$orderItems`)
RULE: Constants: `UPPER_SNAKE` (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
RULE: Properties: `$camelCase` — private by default, accessed via methods
RULE: Interfaces: `PascalCase` with `Interface` suffix (`PaymentGatewayInterface`)
RULE: Abstract classes: `Abstract` prefix (`AbstractRepository`)
RULE: Enums: `PascalCase` (`OrderStatus`, `UserRole`)

```php
class InvoiceService
{
    private const MAX_LINE_ITEMS = 100;

    public function __construct(
        private readonly InvoiceRepositoryInterface $repository,
        private readonly TaxCalculator $taxCalculator,
    ) {}

    public function calculateTotal(Invoice $invoice): Money
    {
        // ...
    }
}
```

BANNED: Hungarian notation (`$strName`, `$intCount`)
BANNED: Abbreviations unless universally known (`$cfg` OK, `$inv` not OK)
BANNED: Prefixing interfaces with `I` (`IPaymentGateway`) — use `Interface` suffix
