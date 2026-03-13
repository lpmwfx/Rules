---
tags: [rust, docs, documentation, rustdocumenter]
concepts: [documentation, public-api, discoverability]
requires: []
related: [slint/docs.md]
keywords: [doc-comment, triple-slash, rustdoc, pub, rustdocumenter]
layer: 2
---
# Documentation Rules

> Every public item must have a `///` doc comment — enforced by `rustdocumenter check` and `rulestools scan`

---

## Requirement

RULE: Every `pub` item (fn, struct, enum, trait, type, mod, const) MUST have a `///` doc comment directly above it
RULE: `pub use` re-exports are exempt
RULE: Test files (`#[cfg(test)]`) are exempt
RULE: Doc comment must appear before any `#[...]` attribute lines that precede the item

## Rule ID

`rust/docs/doc-required`

## Enforcement

Two enforcement layers — both reference the same rule ID:

| Tool | Trigger | Output |
|---|---|---|
| `rulestools scan` | Manual / pre-commit | `proj/ISSUES` |
| `rustdocumenter check` | Manual | stderr + exit 1 |
| `rustdocumenter gen` | Manual | `man/` + `proj/ISSUES` |

`rustdocumenter gen` generates `man/` documentation and writes `proj/ISSUES` listing every undocumented item with file and line number.

## Format

```rust
/// Short summary line — what this does, not how.
///
/// Optional longer description. Explain WHY it exists,
/// key invariants, and edge cases the caller must know.
///
/// # Errors
/// Returns `Err(...)` when ...
///
/// # Panics
/// Panics if `x` is zero.
pub fn process(x: usize) -> Result<Output, MyError> { ... }
```

```rust
/// Configuration loaded from `proj/rulestools.toml`.
pub struct Config {
    /// Maximum nesting depth before emitting an error.
    pub max_depth: usize,
}
```

## Minimal acceptable doc

One sentence is enough for simple items:

```rust
/// Returns true if the file has been modified since last scan.
pub fn is_dirty(&self) -> bool { ... }
```

## BANNED

BANNED: Items with no `///` comment:
```rust
// BAD — no doc comment, will appear in proj/ISSUES
pub fn load_config(path: &Path) -> Result<Config, ConfigError> { ... }
```

BANNED: Only inline comments (not picked up by rustdocumenter):
```rust
// BAD — // is not a doc comment
pub struct Manifest { ... }
```

## Workflow

1. Run `rustdocumenter gen` after adding new pub items → `man/` is updated and `proj/ISSUES` lists gaps
2. Add `///` to every item listed in `proj/ISSUES`
3. Run `rustdocumenter gen` again — `proj/ISSUES` shrinks or disappears
4. Pre-commit: `rustdocumenter check` exits 0 only when all pub items are documented
