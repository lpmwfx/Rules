---
tags: [cpp, nesting, flat, readability]
concepts: [code-style, readability]
related: [python/nesting.md, rust/nesting.md]
keywords: [max-3-levels, early-return]
layer: 4
---
# Flat Code

> Max 3 nesting levels — early returns, extract helpers

---

RULE: Same as Python/JS — max 3 indentation levels
RULE: Early returns to reduce nesting
RULE: Extract helpers for complex logic

```cpp
// GOOD: Flat with early returns
Result<Data> process(Input input) {
    if (!input.valid()) {
        return Result<Data>::fail("Invalid input");
    }

    auto parsed = parse(input);
    if (!parsed.success) {
        return Result<Data>::fail(parsed.error);
    }

    return transform(parsed.data);
}

// BAD: Deep nesting
Result<Data> process(Input input) {
    if (input.valid()) {
        auto parsed = parse(input);
        if (parsed.success) {
            auto transformed = transform(parsed.data);
            if (transformed.success) {
                // too deep!
            }
        }
    }
}
```
