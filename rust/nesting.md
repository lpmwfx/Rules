---
tags: [rust, nesting, flat, readability]
concepts: [code-style, readability]
related: [python/nesting.md, cpp/nesting.md]
keywords: [max-3-levels, early-return, pattern-match]
layer: 4
---
# Flat Code

> Max 3 nesting levels — early returns, ? operator

---

RULE: Same as Python/JS — max 3 indentation levels
RULE: Early returns to reduce nesting
RULE: Extract helpers for complex logic

```rust
// GOOD: Flat with early returns
fn process(input: &Input) -> Result<Data, Error> {
    if !input.is_valid() {
        return Err(Error::InvalidInput);
    }

    let parsed = parse(input)?;
    let transformed = transform(&parsed)?;

    Ok(transformed)
}

// BAD: Deep nesting
fn process(input: &Input) -> Result<Data, Error> {
    if input.is_valid() {
        if let Ok(parsed) = parse(input) {
            if let Ok(transformed) = transform(&parsed) {
                // too deep!
            }
        }
    }
    Err(Error::Failed)
}
```
