---
tags: [combo, script, automation, single-file]
concepts: [quick-ref, project-type]
keywords: [rust, script, rust-script, cargo-script, automation, single-file]
requires: [global/quick-ref.md, rust/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: Rust Script

> Single-file Rust scripts for automation, tooling, and one-off tasks.
> Lighter rules than full Rust projects — pragmatic, not architectural.

---

## What Rust Script is

Single-file Rust programs run via `cargo-script`, `rust-script`, or `cargo +nightly -Zscript`.
No `Cargo.toml`, no `src/` tree, no workspace — just one `.rs` file that runs.

Typical uses: build tooling, code generators, data transforms, CI helpers, migration scripts.

## Rules that STILL apply

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only | [global/language.md](../global/language.md) |
| File limits | Max 300 lines — if bigger, promote to a proper project | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK | [global/tech-debt.md](../global/tech-debt.md) |
| Docs | `///` on pub functions (if any) | [rust/docs.md](../rust/docs.md) |
| Errors | `Result` + `?`. No bare `unwrap()` on user input | [rust/errors.md](../rust/errors.md) |
| Naming | Descriptive names. `is_`/`has_` booleans | [rust/naming.md](../rust/naming.md) |
| Constants | No magic numbers — named consts at top of file | [rust/constants.md](../rust/constants.md) |
| Safety | `unsafe` needs `// SAFETY:` comment | [rust/safety.md](../rust/safety.md) |

## Rules that DO NOT apply

| Rule | Why skipped |
|------|-------------|
| Topology layers | Single file — no `src/core/`, no `_adp` suffixes |
| Layer tags | No layers to tag |
| Mother-child | One file — no module hierarchy |
| Workspace | No Cargo.toml, no crates |
| `pub(crate)` | Everything is in one scope |
| Scanner/build.rs | No build system integration |
| Pre-commit hooks | Scripts live outside managed projects |

## Script structure

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! anyhow = "1"
//! ```

use anyhow::Result;

/// Script-level constants — no magic numbers in main().
const MAX_RETRIES: u32 = 3;
const OUTPUT_DIR: &str = "generated";

fn main() -> Result<()> {
    // flat, sequential, readable
    let input = parse_args()?;
    let data = process(&input)?;
    write_output(&data)?;
    Ok(())
}
```

## Guidelines

| Guideline | Detail |
|-----------|--------|
| One job | Each script does one thing. Multiple jobs = multiple scripts |
| Flat flow | `main()` reads top-to-bottom: parse → process → output |
| Error handling | `anyhow` is fine for scripts. `?` everywhere. Clear error messages |
| Dependencies | Inline in `//! [dependencies]`. Minimize — stdlib first |
| Promotion | If script exceeds 300 lines or gains structure → promote to project |
| Arguments | `std::env::args()` or `clap` for complex CLIs. Always `--help` |

## When to promote to a full project

A script should become a proper Rust project (`cargo init`) when:

- It exceeds 300 lines
- It needs multiple files or modules
- It's used by other tools or CI
- It needs tests
- It has configuration or state

When promoting: run `rulestools new . --kind tool` and apply full Rust rules.

## BANNED

- Scripts over 300 lines without promotion
- `unwrap()` on user input or file IO
- Hardcoded paths without constants
- Deep nesting (4+ levels)
- Non-English code or comments


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
