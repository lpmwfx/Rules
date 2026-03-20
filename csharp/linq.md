---
tags: [linq, collections, querying]
concepts: [linq, functional, collections]
requires: [csharp/types.md]
related: [csharp/nesting.md]
keywords: [linq, select, where, groupby, async-enumerable]
layer: 4
---
# LINQ

> Method syntax, deferred execution — explicit materialisation

---

RULE: Method syntax preferred over query syntax (consistent with codebase style)
RULE: LINQ is lazy — materialise (`ToList()`, `ToArray()`) only when needed
RULE: Never use LINQ inside tight loops on hot paths — profile first
RULE: `IAsyncEnumerable<T>` + `await foreach` for async streaming collections

```csharp
// GOOD: Method syntax, explicit materialisation
var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => new UserSummary_core(u.Id, u.Name))
    .ToList();

// GOOD: Async streaming
await foreach (var record in _db.StreamAsync(query, ct))
    await ProcessAsync(record, ct);
```

## Composition

RULE: Break long LINQ chains into named intermediate steps

```csharp
// BAD: One unreadable chain
var result = orders.Where(o => o.IsValid).GroupBy(o => o.CustomerId)
    .Select(g => new { CustomerId = g.Key, Total = g.Sum(o => o.Amount) })
    .Where(x => x.Total > 1000).OrderByDescending(x => x.Total).ToList();

// GOOD: Named steps
var validOrders = orders.Where(o => o.IsValid);
var byCustomer  = validOrders.GroupBy(o => o.CustomerId);
var summaries   = byCustomer.Select(g => new CustomerSummary_core(g.Key, g.Sum(o => o.Amount)));
var highValue   = summaries.Where(s => s.Total > 1000).OrderByDescending(s => s.Total).ToList();
```

BANNED: `First()` without null check — use `FirstOrDefault()` and handle null
BANNED: `Count() > 0` — use `Any()`
BANNED: `Select(...).Where(...)` when `Where(...).Select(...)` is clearer
BANNED: LINQ to materialise only to iterate once — keep as `IEnumerable<T>`
BANNED: Side effects inside LINQ expressions (`Select(x => { Log(x); return x; })`)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
