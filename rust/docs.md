---
tags: [rust, docs, documentation, rustdocumenter]
concepts: [documentation, public-api, discoverability]
requires: []
related: [slint/docs.md]
keywords: [doc-comment, triple-slash, rustdoc, pub, rustdocumenter]
layer: 2
---
# Documentation Rules

> Every public item must have a `///` doc comment — reported as **errors**, blocks build and commit

---

## Requirement

RULE: Every `pub` item (fn, struct, enum, trait, type, mod, const) MUST have a `///` doc comment directly above it
RULE: `pub use` re-exports are exempt
RULE: Test files (`#[cfg(test)]`) are exempt
RULE: Doc comment must appear before any `#[...]` attribute lines that precede the item

## Rule ID

`rust/docs/doc-required`

## Enforcement

Three enforcement layers — all report as **errors** (blocks build and commit):

| Tool | Trigger | Severity | Output |
|---|---|---|---|
| `rustscanners` (cargo build) | Automatic on `cargo build` | error | stderr, blocks build |
| `rustdocumenter gen` | Manual | error | `proj/ISSUES` + `man/`, blocks further steps |
| `rustdocumenter check` | Pre-commit hook | error | stderr, blocks commit |

Missing `///` doc comments are reported as **errors** and block `cargo build`, pre-commit hooks, and CI/CD pipelines. Every `pub` item must be documented before code can be shipped.

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

## `man/` — Design Evaluation Reference

The `man/` folder is a generated **design reference** for evaluating project architecture. It extracts every `pub` item and its `///` doc comment into a browsable structure that mirrors `src/` 1:1.

### Purpose

`man/` answers design questions without reading implementation:

| Question | How `man/` answers it |
|----------|-----------------------|
| Is the public API coherent? | Scan man pages per module — do the pub items form a clear contract? |
| Are responsibilities correctly placed? | Check if `_core` pages contain IO, or `_gtw` pages contain logic |
| Is the module tree balanced? | Compare page sizes — a huge man page = an oversized module |
| Are error types well-designed? | Read `# Errors` sections — are variants specific and recoverable? |
| Does the naming follow conventions? | Scan for missing `_adp`/`_core`/`_sta` suffixes across all pages |
| Are doc comments meaningful? | Spot one-word or copy-paste descriptions that add no value |

RULE: Use `man/` to evaluate whether the project's public API design is sound — it is a design review tool, not a coding aid
RULE: A man page that looks wrong reveals a design problem — fix the design, not just the doc comment
RULE: After writing new pub items, run `rustdocumenter gen` and verify the item appears in `man/` — missing entry = missing doc comment

### `man/` folder structure

```
man/
├── MANIFEST.json              ← index: maps source files to doc pages
├── src/
│   ├── lib.md                 ← pub items in src/lib.rs
│   ├── config.md              ← pub items in src/config.rs
│   └── checks/
│       ├── mod.md             ← pub items in src/checks/mod.rs
│       ├── nesting.md         ← pub items in src/checks/nesting.rs
│       └── naming.md          ← pub items in src/checks/naming.rs
└── (mirrors src/ hierarchy 1:1)
```

Each `.md` file lists every `pub` item from its corresponding source file with the `///` content.

## Viewing documentation

After running `rustdocumenter gen`, browse the generated `man/` documentation:

```bash
# Install the viewer (one-time)
cargo install --force --git https://github.com/lpmwfx/RustDocumenter rustdoc-viewer

# Open the Slint GUI browser in your project
rustdoc-viewer .

# Or use the rustman wrapper to auto-discover
rustman              # finds nearest man/MANIFEST.json and opens viewer
rustman gen          # generate docs and immediately open viewer
```

The viewer displays:
- **Left sidebar**: project folder hierarchy (`src/`, `src/checks/`, etc.)
- **Right panel**: all `///` doc comments for items in the selected file
- **Search**: find items by name or doc text across the entire project
