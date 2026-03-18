---
tags: [testing, tdd, junit]
concepts: [tdd, quality, testing]
keywords: [test, junit, kotest, assert, integration, unit-test]
layer: 4
---
# Testing — Kotlin

> Real data, not mocks — test behavior, not implementation

---

RULE: Test name: `test <what it tests>` or backtick syntax `` `should do X when Y` ``
RULE: One test per behavior — small, focused, readable
RULE: Real databases — in-memory Room/SQLite, not mocks
RULE: Use `@Before` / `@After` for setup/teardown, not global state
RULE: `assertEquals(expected, actual)` — expected first (JUnit convention)

BANNED: Mock objects for data layer — use real in-memory database
BANNED: `@Ignore` without a tracking issue
BANNED: Tests that depend on execution order
BANNED: Tests that depend on external services

---

## Structure

```kotlin
class CalculatorTest {
    @Test
    fun `should add two numbers`() {
        val result = Calculator.add(2, 3)
        assertEquals(5, result)
    }

    @Test
    fun `should reject negative input`() {
        assertThrows<IllegalArgumentException> {
            Calculator.add(-1, 3)
        }
    }
}
```
