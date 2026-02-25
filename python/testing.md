---
tags: [python, testing, tdd, pytest]
concepts: [tdd, quality, testing]
requires: [python/types.md, python/ack-pattern.md]
related: [rust/verification.md, cpp/testing.md, js/testing.md]
keywords: [pytest, real-db, sqlite, no-mocks]
layer: 4
---
# Testing

> Real databases, not mocks — TDD always

---

RULE: Real databases — in-memory SQLite, not mocks
RULE: Test injection via `set_test_connection()` pattern
RULE: Test class per function: `class TestValidate`
RULE: Test name: `test_<what_it_tests>`
RULE: Docstring explains expected behavior
BANNED: Mock objects for data layer
BANNED: Fixtures that fake behavior
