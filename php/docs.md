---
tags: [docs, phpdoc, documentation]
concepts: [documentation, api-surface, discoverability]
requires: [php/types.md]
feeds: [php/testing.md]
keywords: [phpdoc, param, return, throws, template]
layer: 4
---
# Documentation

> PHPDoc on all public API — @param, @return, @throws

---

RULE: PHPDoc on all public methods and classes
RULE: `@param`, `@return`, `@throws` sections required
RULE: Skip PHPDoc when type declarations say everything — avoid redundant docs
RULE: Class-level docstring describes purpose and responsibility

```php
/**
 * Calculates tax for an invoice based on jurisdiction rules.
 *
 * @param Invoice $invoice  The invoice to calculate tax for.
 * @param TaxRate $rate     Applicable tax rate for the jurisdiction.
 *
 * @return Money Calculated tax amount.
 *
 * @throws InvalidArgumentException If invoice has no line items.
 * @throws TaxCalculationException  If jurisdiction rules cannot be resolved.
 */
public function calculateTax(Invoice $invoice, TaxRate $rate): Money
{
    // ...
}
```

RULE: When native types are sufficient, omit redundant PHPDoc:

```php
// Types say everything — no PHPDoc needed
public function isActive(): bool
{
    return $this->status === OrderStatus::Active;
}
```

BANNED: PHPDoc that just repeats the method signature
BANNED: Undocumented public API with complex parameters
