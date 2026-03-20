---
tags: [nesting, flat, readability]
concepts: [code-style, readability]
requires: [global/nesting.md]
keywords: [early-return, result-type]
layer: 4
---
# Flat Code — C++

> See [global/nesting.md](../global/nesting.md) for shared rules

---

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
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
