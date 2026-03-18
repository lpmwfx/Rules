---
tags: [combo, rust, cli, library, tool]
concepts: [quick-ref, project-type]
keywords: [rust, cargo, workspace, scanner]
requires: [global/quick-ref.md, rust/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: Rust Project

> Rust CLI, library, or tool — no GUI. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | Rust: 300 lines max. Split into mother/child folder | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. `?` over nested match | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## Rust-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Docs | `///` on every pub item — missing = build error | [rust/docs.md](../rust/docs.md) |
| Errors | `Result<T,E>` + `thiserror`. No `unwrap()` outside tests | [rust/errors.md](../rust/errors.md) |
| Constants | Zero literals in fn bodies. Named consts in `state/` | [rust/constants.md](../rust/constants.md) |
| Modules | One module per file. No `utils.rs`. `pub(crate)` default | [rust/modules.md](../rust/modules.md) |
| Naming | Layer-tag suffix. `is_`/`has_` booleans. Plural collections | [rust/naming.md](../rust/naming.md) |
| Types | No `&Vec`/`&String`. No `static mut`. Concrete error types | [rust/types.md](../rust/types.md) |
| Ownership | Minimize `.clone()`. Borrow by default | [rust/ownership.md](../rust/ownership.md) |
| Threading | No fire-and-forget spawns. `Arc`/`Rc` needs comment | [rust/threading.md](../rust/threading.md) |
| Safety | `unsafe` needs `// SAFETY:` comment | [rust/safety.md](../rust/safety.md) |
| Testing | Unit tests in same file. Integration tests in `tests/` | [rust/testing.md](../rust/testing.md) |
| Nesting | Max 3 levels. `?` over nested match/if-let | [rust/nesting.md](../rust/nesting.md) |

## Workspace layout (multi-crate)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Workspace | Topology = crate names: `crates/{core,adapter,gateway,pal,shared}` | [rust/workspace.md](../rust/workspace.md) |
| PAL | Platform abstraction — traits in PAL, impls per platform | [rust/pal-structure.md](../rust/pal-structure.md) |
| Multi-binary | One crate per binary. Shared logic in library crate | [rust/multi-binary.md](../rust/multi-binary.md) |
| Scanner config | `proj/rulestools.toml` — project kind, check overrides | [rust/scanner-config.md](../rust/scanner-config.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test` |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `build.rs` → `rulestools_scanner::scan_project()` |

## BANNED

- `unwrap()`/`expect()` outside tests
- `panic!()` for recoverable errors
- `pub` without `///`
- Files over 300 lines
- `utils.rs`, `helpers.rs`, `common.rs`
- Hardcoded values in fn bodies
- Deep nesting (4+ levels)
- `static mut`
- Children owning state

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`
