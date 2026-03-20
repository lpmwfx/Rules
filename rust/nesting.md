---
tags: [nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md]
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


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
