---
tags: [testing, phpunit, pest]
concepts: [tdd, quality, testing]
requires: [php/types.md]
keywords: [phpunit, pest, real-db, sqlite, no-mocks]
layer: 4
---
# Testing

> Real databases, not mocks — TDD always

---

RULE: Real databases — in-memory SQLite or test database, not mocks
RULE: One test class per production class
RULE: Test method name: `test_<what_it_tests>` or `it_<describes_behavior>` (Pest)
RULE: Arrange-Act-Assert pattern in every test
RULE: No test depends on another test — each test is isolated

```php
// PHPUnit
class InvoiceServiceTest extends TestCase
{
    use RefreshDatabase;

    public function test_calculate_total_includes_tax(): void
    {
        // Arrange
        $invoice = Invoice::factory()->withLineItems(3)->create();

        // Act
        $total = $this->service->calculateTotal($invoice);

        // Assert
        $this->assertGreaterThan($invoice->subtotal, $total);
    }
}

// Pest
it('calculates total including tax', function () {
    $invoice = Invoice::factory()->withLineItems(3)->create();
    $total = $this->service->calculateTotal($invoice);
    expect($total)->toBeGreaterThan($invoice->subtotal);
});
```

BANNED: Mock objects for data layer — use real database
BANNED: Tests that depend on execution order
BANNED: `@doesNotPerformAssertions` — every test asserts
