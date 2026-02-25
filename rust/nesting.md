---
tags: [rust, nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md]
related: [python/nesting.md, cpp/nesting.md]
keywords: [question-mark-operator, pattern-match]
layer: 4
---
# Flat Code — Rust

> See [global/nesting.md](../global/nesting.md) for shared rules

---

RULE: Use `?` operator instead of nested match/if-let

```rust
// GOOD: Flat with ? operator
fn process(input: &Input) -> Result<Data, Error> {
    if !input.is_valid() {
        return Err(Error::InvalidInput);
    }

    let parsed = parse(input)?;
    let transformed = transform(&parsed)?;

    Ok(transformed)
}
```
