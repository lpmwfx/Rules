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
