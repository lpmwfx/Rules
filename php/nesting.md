---
tags: [nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md, php/modules.md]
keywords: [early-return, guard-clause, flat]
layer: 4
---
# Flat Code — PHP

> See [global/nesting.md](../global/nesting.md) for shared rules

---

RULE: Max 3 levels of indentation — use early returns and guard clauses
RULE: Simple try/catch at top level only — never nested

```php
// CORRECT — guard clauses, flat
public function processOrder(Order $order): Result
{
    if (!$order->isValid()) {
        return Result::error('Invalid order');
    }

    if ($order->isPaid()) {
        return Result::error('Already paid');
    }

    $total = $this->calculator->calculate($order);
    $this->repository->save($order);

    return Result::success($total);
}

// BANNED — deeply nested
public function processOrder(Order $order): Result
{
    if ($order->isValid()) {
        if (!$order->isPaid()) {
            try {
                // too deep
            } catch (...) {
            }
        }
    }
}
```

BANNED: More than 3 levels of indentation
BANNED: Nested try/catch blocks
