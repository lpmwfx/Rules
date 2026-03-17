---
tags: [nesting, flat, readability, early-return, control-flow]
concepts: [code-style, readability, control-flow-complexity]
feeds: [python/nesting.md, cpp/nesting.md, rust/nesting.md, js/nesting.md, kotlin/nesting.md]
related: [global/consistency.md, global/file-limits.md]
keywords: [max-nesting, early-return, extract-helper, flat-code, control-flow, depth]
layer: 1
---
# Flat Code

> Nesting measures control-flow complexity — not brace depth

---

VITAL: Flat is better than nested — all languages, no exceptions
VITAL: Nesting = control-flow depth, NOT total brace count
RULE: Early returns to reduce nesting — guard clauses at top
RULE: Extract helpers for complex logic — name the intent
RULE: If/else on same level, not nested

BANNED: Exceeding language-specific nesting limit (see table below)

---

## What Counts as Nesting

Nesting depth measures **control-flow complexity** — how many decisions deep the code is.

Counts as nesting:
- `if` / `else` / `else if` / `match` / `switch`
- `for` / `while` / `loop`
- `fn` / `def` / `function` body (one level)
- Closures / callbacks / `=> {`
- Slint component bodies, conditionals, repeaters

Does NOT count:
- `struct` / `enum` / `impl` / `trait` definitions (data, not flow)
- Type annotations: `property <{x: int, y: int}>` in Slint
- `mod` / `pub mod` declarations
- `const` / `static` definitions
- `#[attribute]` blocks

## Limits per Language

| Language | Limit | Rationale |
|----------|-------|-----------|
| JavaScript / TypeScript | 4 | Callbacks compound fast |
| Rust | 5 | Pattern matching adds levels |
| Slint | 6 | UI component nesting is visual |
| Kotlin | 6 | Scope functions reduce visual nesting |
| C# | 7 | LINQ/async patterns |
| Python | 8 | Measured by indentation (4 spaces = 1 level) |

## Python Special Case

Python uses indentation, not braces. Nesting depth = indentation level on control-flow lines.
`{}` in Python (dicts, sets) are NOT nesting — only `if`, `for`, `while`, `def`, `class`, `with`, `try` count.

## Scanner Check

`global/nesting` — measures control-flow depth per function.
Struct/enum/impl bodies are tracked for brace-matching but do not increment flow depth.
