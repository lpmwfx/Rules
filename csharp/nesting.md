---
tags: [nesting, flat, readability, guard-clauses]
concepts: [code-style, readability]
requires: [global/nesting.md]
keywords: [guard-clause, early-return, pattern-matching]
layer: 4
---
# Flat Code — C#

> See [global/nesting.md](../global/nesting.md) for shared rules

---

RULE: Guard clauses at top — return/throw early for preconditions
RULE: Max 3 levels of nesting — extract method if deeper

```csharp
// BAD: Pyramid of doom
public Result<Order_core> Process(Order_core? order)
{
    if (order != null)
    {
        if (order.Items.Count > 0)
        {
            if (order.TotalAmount > 0)
            {
                // actual logic buried here
            }
        }
    }
}

// GOOD: Guard clauses
public Result<Order_core> Process(Order_core? order)
{
    if (order is null)
        return Result<Order_core>.Fail("Order is null");
    if (order.Items.Count == 0)
        return Result<Order_core>.Fail("Order has no items");
    if (order.TotalAmount <= 0)
        return Result<Order_core>.Fail("Order amount must be positive");

    // actual logic — flat and readable
    return Execute(order);
}
```

## Pattern Matching

RULE: Prefer `switch` expressions over chains of `if/else if`

```csharp
// GOOD: Switch expression
var message = status switch
{
    OrderStatus.Pending   => "Awaiting payment",
    OrderStatus.Paid      => "Processing",
    OrderStatus.Shipped   => "On the way",
    OrderStatus.Delivered => "Delivered",
    _                     => throw new UnreachableException($"Unknown status: {status}"),
};
```

BANNED: `else` after a `return` or `throw`
BANNED: More than 3 levels of `{ }` nesting
BANNED: `_ => { }` switch arm that silently discards — always throw or log+recover


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
