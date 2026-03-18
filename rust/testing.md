---
tags: [testing, tdd, cargo-test]
concepts: [tdd, quality, testing]
requires: [rust/errors.md]
keywords: [test, cargo-test, assert, rstest, integration, unit-test]
layer: 4
---
# Testing

> Real data, not mocks — test behavior, not implementation

---

RULE: Test name: `test_<what_it_tests>` — describes the expected behavior
RULE: One `#[test]` per behavior — small, focused, readable
RULE: Use `#[cfg(test)] mod tests` at bottom of source file for unit tests
RULE: Integration tests in `tests/` directory — test public API only
RULE: Real databases — in-memory SQLite or temp files, not mocks
RULE: Test injection via constructor parameter, not global state
RULE: `assert_eq!(actual, expected)` — actual first, expected second
RULE: Use `rstest` for parameterized tests when >3 similar test cases

BANNED: Mock objects for data layer — use real in-memory database
BANNED: `#[ignore]` without a tracking issue
BANNED: Tests that depend on execution order
BANNED: Tests that depend on external services (network, API)
BANNED: `sleep()` in tests — use channels or condition variables

---

## Structure

```rust
// Unit tests — bottom of source file
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_valid_input() {
        let result = parse("42");
        assert_eq!(result, Ok(42));
    }
}
```

```rust
// Integration tests — tests/ directory
// tests/api_test.rs
use my_crate::public_api;

#[test]
fn test_full_workflow() {
    let result = public_api::process("input");
    assert!(result.is_ok());
}
```

## Test Naming

| Pattern | Example |
|---------|---------|
| Happy path | `test_parse_valid_number` |
| Error case | `test_parse_rejects_empty_string` |
| Edge case | `test_parse_handles_max_value` |
| Integration | `test_save_and_load_roundtrip` |
