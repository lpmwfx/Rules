---
tags: [scanners, enforcement, SlintUITemplates]
concepts: [enforcement, declarative-ui]
requires: [slint/README.md]
related: [slint/component-model.md, slint/mother-child.md, slint/rust-bridge.md, slint/globals.md, slint/states.md, slint/themes.md, slint/responsive-layout.md, slint/threading.md, slint/validation.md, slint/docs.md, global/topology.md, global/file-limits.md, global/language.md]
layer: 6
binding: true
---
# Slint Quick Reference

> All enforced rules at a glance — slintscan tests these automatically on `cargo build`

---

## Contract

AXIOM: This ruleset is binding for humans and AI agents — not subject to interpretation.
AXIOM: These are not suggestions or guidelines. They are constraints enforced by scanners.
AXIOM: Rule violations block `cargo build` and block commits. There are no exceptions.

---

## Language

All `.slint` code, doc comments, identifiers, and property names must be in **English**.
Only ASCII characters. UI strings go through a `Strings` global — localize at the boundary only.

## What Slint Is

Slint is a declarative DSL for building UI — it maps 1:1 to the `_ui` topology layer.
`.slint` files define **what** the UI looks like. Rust (via Adapter) defines **what happens**.
Scripting logic uses Rhai where lightweight runtime behavior is needed.

## UI + Adapter Foundation — `slint-ui-templates`

Slint projects use `slint-ui-templates` as the standard `_ui` + `_adp` foundation layer.
Provides a near-complete implementation of both topology layers — the project adds `_core`, `_gtw`, `_pal`, `_x`.

Covered: AppWindow (mother), desktop/mobile shells, shared widgets (Button, Card, Badge, Toggle,
TextInput, Avatar, ProgressBar, SelectField), design tokens, AppAdapter.

Three usage modes:
- **Design tool**: `slint-viewer ui/desktop/app-window.slint --auto-reload` — live preview, no Rust
- **Library**: add `slint-ui-templates` to `Cargo.toml` — use widgets, AppAdapter, layout DSL
- **Template**: clone → edit `ui/views/*.slint` → add `_core`/`_gtw`/`_pal` → ship

Layout DSL: `layout::build("1:2/1:1:1", w, h)` — `:` splits horizontal, `/` splits vertical, numbers are ratios.

For repo URL and install: `list_libraries(["slint", "rust"])` — or see `catalog/slint-ui-templates.md`.

## Topology — Slint Is the `_ui` Layer

`.slint` files live in `ui/` at project root (separate from `src/`).
Slint knows nothing about Core, Gateway, or PAL — all data flows through Adapter.

```
ui/                          ← .slint files (declarative UI)
src/adapter/                 ← Rust Adapter (owns bridge: set_*, on_*)
src/core/                    ← business logic (pure, no UI knowledge)
```

Only the Adapter layer calls `ui.set_*()`, `ui.on_*()`, `ui.invoke_*()` — never Core, Gateway, or PAL.

## Mother–Child Composition

Every UI has exactly **one mother** — the `AppWindow` component that `inherits Window`.
All other components are **stateless children**.

- Mother owns all state via `in-out property`
- Children receive state via `in property` — they never fetch or derive their own
- Children emit events via `callback` — mother decides what happens
- Siblings never communicate directly — all coordination routes through mother
- Children have no hardcoded sizes — mother controls all dimensions

```
AppWindow (mother — inherits Window, owns ALL state)
├── NavBar (child)             ← in property + callback
├── WorkspaceView (child)      ← composes its own sub-children
│   ├── LeftPanel (module)
│   ├── Canvas (module)
│   └── Inspector (module)
└── Overlays                   ← visibility controlled by mother
```

Overlays (modals, dialogs) are children of mother — not of the view that triggered them.

## Documentation — `///` Required

Every exported component, struct, enum, callback, and property must have a `///` doc comment.
Missing doc comments are **errors** — they block `cargo build` (via slintscan) and block commits.
Private properties are exempt.

```slint
/// Main editor window — hosts sidebar, content, and toolbar.
export component EditorWindow inherits Window {
    /// Title shown in the header bar.
    in property <string> window-title;
    /// Emitted when the user requests saving.
    callback save-requested();
}
```

## File Size — 200 Lines Max

Slint components have a **200-line hard limit** — the strictest in the project.
Declarative markup gives AI no way to skip or summarize sections; above 200 lines, bugs are guaranteed.

When approaching the limit, split into a mother/child folder:

```
sidebar.slint  →  sidebar/
                   ├── sidebar.slint     ← mother: composes children
                   ├── nav-item.slint    ← child: one job
                   └── nav-group.slint   ← child: one job
```

Many small components are always preferred over fewer large ones. One file = one component.

## Four Invariants

1. **`in property`** — Adapter pushes state in; component renders it
2. **`callback`** — component fires event; Adapter registers handler with `on_*()`
3. **Token globals** — all literal values live in `Colors`, `Spacing`, `Sizes` globals
4. **No logic in `.slint`** — callback body = one delegation call, nothing else

## Property Direction

| Keyword | Who writes | Who reads | Use case |
|---------|-----------|-----------|----------|
| `in property` | Adapter (Rust) | Component | State pushed down |
| `out property` | Component | Adapter (Rust) | Computed values read up |
| `private property` | Component | Component | Internal UI state (hover, focus) |
| `in-out property` | Mother only | Mother only | `<=>` delegation in Window |

Children never use `in-out property` — that is state ownership, reserved for mother.
Exception: `in-out property` in children only for `<=>` two-way binding from mother.

## Zero Literals in Components

Every value in a component is a variable reference — no hardcoded numbers, colors, or strings.

| Instead of | Use |
|-----------|-----|
| `#4a90d9` | `Colors.accent` |
| `16px` | `Spacing.md` |
| `0px` | `Sizes.zero` |
| `200ms` | `Durations.slide` |
| `"Save"` | `Strings.save` |
| `0`, `1`, `2` | `ViewStates.nav-home` |

Only `true`/`false` are allowed as literals in components.
Three compiler exceptions: `GridLayout row:/col:`, `@image-url("...")`, `@tr("...")`.

**Create-before-use:** Tokens do not pre-exist. When you need a value: search the global → not found → create it in the global file FIRST → then reference it. See [slint/states.md](../slint/states.md) and [uiux/tokens.md](../uiux/tokens.md).

**String comparisons:** Never `== "literal"` — use `== Strings.kind-dialogue`. Create the constant in Strings global first.

## Globals — Tokens, Strings, Bridge

| Global | Purpose | Property type |
|--------|---------|--------------|
| `Colors` | Color tokens (light + dark) | `out property` |
| `Spacing` | Spacing tokens | `out property` |
| `Effects` | Blur, opacity, shadows | `out property` |
| `Strings` | All user-visible UI text | `in property` |
| `AppBridge` | Centralised event routing | `callback` |

Theme files are the only place literal hex/px values appear in `.slint` source.
Each theme file contains both light AND dark values — no separate files.

## Responsive Layout

- Only `AppWindow` reads `root.width` for breakpoints — never deep in sub-components
- Children set `preferred-width: 100%` and use `horizontal-stretch` / `vertical-stretch`
- Use `preferred-width` on Window — never `width` (locks resize)
- Use `min-width` for constraints — not absolute pixel sizes

## Rust Bridge — Adapter Only

Boot order: Gateway → Core → `AppWindow::new()` → `Adapter::init()` → `ui.run()`.
All `ui.on_*()` handlers registered in `Adapter::init()` before `ui.run()`.

Type mapping:

| Slint | Rust | Conversion |
|-------|------|-----------|
| `string` | `SharedString` | `"text".into()` |
| `int` / `float` | `i32` / `f32` | direct |
| `[T]` model | `ModelRc<T>` | `Rc::new(VecModel::from(vec)).into()` |

## Threading

Slint is single-threaded. Background thread → UI must use `invoke_from_event_loop()`.
Always call `ui.as_weak()` before spawning threads. Never call `ui.set_*()` from a background thread.

## File Structure

```
ui/
├── app-window.slint           ← mother (inherits Window)
├── globals/
│   ├── theme.slint            ← entry point (re-exports active theme)
│   ├── theme/
│   │   ├── solid.slint        ← Colors + Effects (light + dark)
│   │   ├── spacing.slint      ← shared spacing tokens
│   │   └── typography.slint   ← shared type tokens
│   ├── app-bridge.slint       ← centralised event routing
│   └── strings.slint          ← localization strings
├── state/
│   ├── view-states.slint      ← navigation enums
│   ├── sizes.slint            ← fixed sizes, divisors
│   └── durations.slint        ← animation timings
└── views/
    ├── navbar.slint           ← stateless child
    └── workspace-view.slint   ← stateless child
```

## Naming

- Component names: `PascalCase`
- All other identifiers: `kebab-case` (Slint auto-converts to `snake_case` in Rust)
- One component per file — filename matches component name in kebab-case
- `export` every component used from another file

## BANNED

- Logic inside `.slint` callback bodies — one delegation call only
- `in-out property` on child components — reserved for mother
- Hardcoded hex colors, px values, or strings in components — use tokens
- `pub` items without `///` doc comment
- Files over 200 lines
- Children with hardcoded width/height — mother controls layout
- Children importing from siblings — route through mother
- Components importing theme files directly — only via `theme.slint`
- Non-English code, comments, or identifiers

## Enforcement

| Scanner | Trigger | What it checks |
|---------|---------|---------------|
| `slintscan` | `cargo build` (build.rs) | Zero-literal, tokens, structure, events, docs |
| `rustdocumenter` | Manual / pre-commit | `///` doc comments on all pub items |

## Contract

This ruleset is binding for humans and AI agents — not subject to interpretation.
Rule violations are flagged by scanners and block builds and commits.
