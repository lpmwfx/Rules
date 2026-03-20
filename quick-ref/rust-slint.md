---
tags: [combo, slint-app, gui]
concepts: [quick-ref, project-type]
keywords: [rust, slint, gui, desktop, ui, adapter]
requires: [global/quick-ref.md, rust/quick-ref.md, slint/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: Rust + Slint (GUI App)

> Desktop GUI app — Rust backend + Slint declarative UI. All rules at a glance.

---

## Foundation — global rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | Pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x`, `_ui` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | Rust: 300 lines. Slint: 200 lines. Split into mother/child | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Data-driven UI | UI is reactive projection of data — globals are data endpoints | [global/data-driven-ui.md](../global/data-driven-ui.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |

## Rust rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Docs | `///` on every pub item — missing = build error | [rust/docs.md](../rust/docs.md) |
| Errors | `Result<T,E>` + `thiserror`. No `unwrap()` outside tests | [rust/errors.md](../rust/errors.md) |
| Constants | Zero literals in fn bodies. Named consts in `state/` | [rust/constants.md](../rust/constants.md) |
| Modules | One module per file. No `utils.rs`. `pub(crate)` default | [rust/modules.md](../rust/modules.md) |
| Naming | Layer-tag suffix. `is_`/`has_` booleans. Plural collections | [rust/naming.md](../rust/naming.md) |
| Types | No `&Vec`/`&String`. No `static mut`. Concrete error types | [rust/types.md](../rust/types.md) |
| Ownership | Minimize `.clone()`. Borrow by default | [rust/ownership.md](../rust/ownership.md) |
| Threading | No fire-and-forget. `Arc`/`Rc` needs comment | [rust/threading.md](../rust/threading.md) |
| Safety | `unsafe` needs `// SAFETY:` comment | [rust/safety.md](../rust/safety.md) |
| Workspace | Topology = crate names: `crates/{core,adapter,gateway,pal,shared}` | [rust/workspace.md](../rust/workspace.md) |
| PAL | Traits in PAL, impls per platform | [rust/pal-structure.md](../rust/pal-structure.md) |

## Slint rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Docs | `///` on every export — missing = build error | [slint/docs.md](../slint/docs.md) |
| Mother-child | AppWindow is mother (owns state). All others are stateless | [slint/mother-child.md](../slint/mother-child.md) |
| Component model | `in property` = data in, `callback` = events out, no logic | [slint/component-model.md](../slint/component-model.md) |
| Zero literals | All values from globals: Colors, Spacing, Sizes, Strings | [slint/states.md](../slint/states.md) |
| Globals | Colors, Spacing, Effects = `out property`. Strings = `in property` | [slint/globals.md](../slint/globals.md) |
| Themes | One file = light + dark. Only place hex/px literals appear | [slint/themes.md](../slint/themes.md) |
| Rust bridge | Only Adapter calls `ui.set_*()`, `ui.on_*()`. Boot: Gtw→Core→UI→Adp→run | [slint/rust-bridge.md](../slint/rust-bridge.md) |
| Threading | Single-threaded. `invoke_from_event_loop()` + `ui.as_weak()` | [slint/threading.md](../slint/threading.md) |
| Responsive | Only AppWindow reads `root.width`. Children use stretch | [slint/responsive-layout.md](../slint/responsive-layout.md) |
| Validation | Create-before-use: token → global → then bind | [slint/validation.md](../slint/validation.md) |

## UI/UX rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Mother-child UI | Window is mother, views are stateless children | [uiux/mother-child.md](../uiux/mother-child.md) |
| State flow | Adapter owns AppState, pushes to UI via set_* | [uiux/state-flow.md](../uiux/state-flow.md) |
| Tokens | Design tokens = data API. Create-before-use | [uiux/tokens.md](../uiux/tokens.md) |
| Components | One component per file. Max 200 lines | [uiux/components.md](../uiux/components.md) |
| File structure | `ui/` at root, `globals/`, `state/`, `views/` | [uiux/file-structure.md](../uiux/file-structure.md) |

## Project layout

```
project/
├── proj/                    ← project files (PROJECT, TODO, FIXES, RULES)
├── ui/                      ← .slint files (declarative UI)
│   ├── app-window.slint     ← mother (inherits Window)
│   ├── globals/             ← Colors, Spacing, Strings, AppBridge
│   ├── state/               ← ViewStates, Sizes, Durations
│   └── views/               ← stateless child components
├── src/
│   ├── main.rs              ← boot: gateway → core → ui → adapter → run
│   ├── adapter/             ← _adp: hub, owns bridge (set_*, on_*)
│   ├── core/                ← _core: pure logic, no IO, no UI
│   ├── gateway/             ← _gtw: config/state load/save
│   ├── pal/                 ← _pal: platform abstraction
│   └── shared/              ← _x: errors, traits, types
└── build.rs                 ← slint_build + rulestools scanner
```

## Property direction

| Keyword | Writer | Reader | Use |
|---------|--------|--------|-----|
| `in property` | Adapter (Rust) | Component | State pushed down |
| `out property` | Component | Adapter | Computed values read up |
| `private property` | Component | Component | Internal UI state |
| `in-out property` | Mother only | Mother only | `<=>` delegation |

## Verification

| Gate | Tools |
|------|-------|
| Local | `cargo fmt`, `cargo clippy -D warnings`, `cargo test` |
| Build | `build.rs` → slint_build + rulestools scanner + slintscan |
| Pre-commit | `rulestools check .` — scan + deny errors |

## BANNED

- `unwrap()`/`expect()` outside tests
- `pub`/`export` without `///` doc comment
- Rust files over 300 lines, Slint files over 200 lines
- Hardcoded values in fn bodies or components — use consts/tokens
- Logic in `.slint` callback bodies — one delegation call only
- `in-out property` on child components — reserved for mother
- Children importing from siblings — route through mother
- UI calling Core/Gateway/PAL directly — only via Adapter
- `utils.rs`, `helpers.rs`, `common.rs`
- `static mut`, fire-and-forget spawns


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
