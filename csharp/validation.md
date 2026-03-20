---
tags: [validation, fluent-validation, data-annotations, boundaries]
concepts: [boundary-validation, null-guards, domain-trust, input-validation]
requires: [csharp/types.md, global/validation.md]
feeds: [csharp/errors.md]
keywords: [fluentvalidation, dataannotations, throwifnull, required, boundary, guard]
layer: 4
---
# Validation

> Validate at system boundaries — domain code trusts typed inputs

---

RULE: FluentValidation or DataAnnotations at system boundaries (API controllers, message handlers)
RULE: `ArgumentNullException.ThrowIfNull()` for null guards on public method parameters
RULE: Validate at Gateway/Adapter boundary — domain code trusts its typed inputs
RULE: `required` keyword on non-nullable properties in DTOs and config types

```csharp
// GOOD: Boundary validation with FluentValidation
public class CreateUserRequest_gtw
{
    public required string Email { get; init; }
    public required string DisplayName { get; init; }
}

public class CreateUserValidator : AbstractValidator<CreateUserRequest_gtw>
{
    public CreateUserValidator()
    {
        RuleFor(x => x.Email).NotEmpty().EmailAddress();
        RuleFor(x => x.DisplayName).NotEmpty().MaximumLength(100);
    }
}

// GOOD: Null guard at public API boundary
public async Task<User_core> GetUserAsync(UserId id, CancellationToken ct)
{
    ArgumentNullException.ThrowIfNull(id);
    // Domain code — no further null checks needed
    return await _repo.FindAsync(id, ct);
}

// BAD: Validation scattered in domain logic
public decimal CalculateDiscount(Order order)
{
    if (order == null) throw new ArgumentNullException();     // too late
    if (order.Items == null) throw new ArgumentNullException(); // should be typed
    if (order.Items.Count == 0) return 0;                      // scattered
    // ...
}
```

BANNED: Manual null-check chains in domain code — validate at boundaries, trust types inside
BANNED: Validation logic scattered in business methods — centralize in validator classes
BANNED: `string.IsNullOrEmpty()` deep in domain code — use `required` and boundary validation
BANNED: Silently accepting invalid input — fail fast at the boundary


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
