---
tags: [scanners, enforcement]
concepts: [enforcement]
related: [rust/types.md, rust/ownership.md, rust/modules.md, rust/errors.md, rust/verification.md, global/topology.md, global/file-limits.md, global/language.md, rust/docs.md]
layer: 6
binding: true
---
# Rust Quick Reference

> All enforced rules at a glance — scanners test these automatically

---

## Contract

AXIOM: This ruleset is binding for humans and AI agents — not subject to interpretation.
AXIOM: These are not suggestions or guidelines. They are constraints enforced by scanners.
AXIOM: Rule violations block `cargo build` and block commits. There are no exceptions.

---

## Language

All code, comments, doc comments, identifiers, file names, and commit messages must be in **English**.
Only ASCII characters in source code. UI strings start as English — localize at the boundary only.

## Topology — 6-Layer Architecture

Every file lives in exactly one layer. Import direction is one-way downward.

| Folder | Tag | Role |
|--------|-----|------|
| `src/ui/` | `_ui` | Declarative UI (Slint) or MCP server |
| `src/adapter/` | `_adp` | Data exchange hub — ViewModel, routing |
| `src/core/` | `_core` | Pure business logic — no IO, no UI |
| `src/pal/` | `_pal` | Platform abstraction — OS, filesystem |
| `src/gateway/` | `_gtw` | IO adapter — config/state load/save |
| `src/shared/` | `_x` | Cross-cutting — errors, traits, shared types |

All types carry a layer-tag suffix matching their folder (`ConfigLoader_gtw`, `AppState_adp`).
UI never imports Core. Core never imports Adapter, UI, or Gateway.

## Mother–Child Module Pattern

Every scope has exactly **one owner** (mother) and **stateless children**.

- `mod.rs` / `lib.rs` / `main.rs` = **mother** — composes and wires children, owns state
- Child `.rs` files = **stateless** — receive state as parameters, return results
- Children never own `static`, `lazy_static!`, `OnceLock` — state belongs in mother
- Siblings never communicate directly — all coordination routes through mother
- Each child is independently understandable by reading that one file

## Documentation — `///` Required

Every `pub` item (`fn`, `struct`, `enum`, `trait`, `type`, `mod`, `const`) must have a `///` doc comment.
Missing doc comments are **errors** — they block `cargo build` (via rustscanners) and block commits (via pre-commit hook).

Minimum: one sentence explaining what the item does.
`pub use` re-exports and `#[cfg(test)]` items are exempt.

## Zero Literals — [rust/constants.md](../rust/constants.md)

Function bodies contain zero literal values. Only `0` and `1` are allowed bare.
All other numbers, durations, paths, URLs, and thresholds are named constants from `state/` modules or `_cfg` structs.

**Create-before-use:** Constants do not pre-exist. When you need a value: search the state module → not found → `pub const NAME: Type = value;` in `state/sizes.rs` (or `durations.rs`, `limits.rs`, `paths.rs`) FIRST → then reference it. Never write the literal in the function body.

## File Size — 300 Lines Max

Rust modules have a **300-line hard limit**. Slint components have a **200-line hard limit**.
When a file approaches the limit, split into a mother/child folder cascade:

```
feature.rs  →  feature/
                ├── mod.rs      ← mother: composes + re-exports
                ├── child_a.rs  ← one job
                └── child_b.rs  ← one job
```

Many small modules are preferred over fewer large files. One file = one responsibility.
The split is the design — not a workaround.

## Errors

`Result<T, E>` for all fallible operations. `thiserror` for custom error types.
`anyhow` only at CLI/binary top-level. `?` operator for propagation.
Match error variants exhaustively — no wildcard `_ =>` arms that discard errors.

## Modules

One module per file. `mod.rs` only for re-exports.
`pub(crate)` for internal APIs, `pub` for external APIs only.
Max ~10 pub items per module. No `utils.rs`, `helpers.rs`, `common.rs`.

## Naming

Names explain **why** the variable exists. Layer-tag suffix on all types.
Booleans: `is_`, `has_`, `can_`, `should_`. Collections: always plural.
Lifecycle names: `*_input`, `*_parsed`, `*_validated`, `*_resolved`, `*_final`.

## Nesting

Max 3 levels of indentation. Use `?` operator instead of nested match/if-let.
Early returns to keep the happy path flat.

## Verification Stack

| Gate | Tools |
|------|-------|
| Level 0 — Local | `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test` |
| Level 1 — Merge | `cargo deny check`, `cargo audit`, `cargo machete`, `typos` |
| Level 2 — Release | `cargo miri test`, sanitizers, `cargo llvm-cov` |

## BANNED

- `unwrap()` / `expect()` outside tests
- `panic!()` for recoverable errors
- `Box<dyn Error>` — use concrete error types
- Deep nesting (> 3 levels)
- `pub` items without `///` doc comment
- Files over 300 lines (Rust) or 200 lines (Slint)
- Children owning state (`static`, `OnceLock`) — state belongs in mother
- Non-English code, comments, or identifiers

## Contract

This ruleset is binding for humans and AI agents — not subject to interpretation.
Rule violations are flagged by scanners and block builds and commits.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
