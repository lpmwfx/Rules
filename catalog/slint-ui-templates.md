---
tags: [catalog, library, slint, rust, ui-layer, adapter-layer, topology, slint-ui-templates]
concepts: [library, ui-template, topology-layer, mother-child]
type: library
name: slint-ui-templates
languages: [slint, rust]
layers: [_ui, _adp]
related: [slint/quick-ref.md, global/topology.md, uiux/mother-child.md]
layer: 3
---
# slint-ui-templates — UI + Adapter Foundation

Standard foundation library for topology-compliant Slint apps.
Provides a near-complete `_ui` and `_adp` layer — your project adds the remaining layers.

> **crates.io:** `https://crates.io/crates/slint-ui-templates`
> **Install:** `cargo add slint-ui-templates`

---

## What It Covers

| Layer | Provided |
|-------|----------|
| `_ui` | AppWindow (mother), desktop/mobile shells, shared widgets, design tokens, state globals |
| `_adp` | AppAdapter — apply_settings, apply_theme, apply_grid, set_active_view |

Your project adds: `_core`, `_gtw`, `_pal`, `_x`, and your own `ui/views/*.slint`.

---

## Usage Modes

### 1. Design tool (no Rust)

```
slint-viewer ui/desktop/app-window.slint --auto-reload
```

Live preview — edit `ui/views/*.slint`, see changes instantly. No Cargo build needed.

### 2. Library (add to existing project)

```toml
[dependencies]
slint-ui-templates = "0.3"
```

```rust
use slint_ui_templates::layout;

let panels = layout::build("1:2/1:1:1", 1920.0, 1080.0);
// Returns Vec<SolvedItem> with normalized x/y/w/h
```

### 3. App template (fastest start)

Clone repo → edit `ui/views/*.slint` → add `_core`/`_gtw`/`_pal` layers → ship.

---

## AppAdapter — `_adp` Layer

```rust
let adapter = AppAdapter::new()?;
adapter.apply_settings(&settings);
adapter.apply_theme();
adapter.set_active_view("home");
adapter.run()?;
```

Boot order: Gateway → Core → `AppAdapter::new()` → configure → `adapter.run()`.

---

## Shared Widgets

Button, Card, Badge, Toggle, TextInput, Avatar, ProgressBar, SelectField.

All token-driven — zero hardcoded values. Compliant with `slint/states.md` zero-literal rule.

---

## Layout DSL

```rust
layout::build("1:2/1:1:1", width, height)
// `:` = horizontal split, `/` = vertical split, numbers = ratios
// Returns Vec<SolvedItem> with normalized x/y/w/h
```

---

## Project Structure When Using as Template

```
ui/
├── tokens/          ← provided: colors, spacing, typography, scale
├── state/           ← provided: Theme, Settings globals
├── shared/          ← provided: Button, Card, Toggle, ...
├── desktop/         ← provided: AppWindow mother + shell
├── mobile/          ← provided: mobile AppWindow
└── views/           ← YOURS: home.slint, list.slint, settings.slint

src/
├── adapter/         ← provided: AppAdapter (_adp)
├── layout/          ← provided: DSL parser + solver
├── grid/            ← provided: TOML grid loader
├── core/            ← YOURS: business logic (_core)
├── gateway/         ← YOURS: IO (_gtw)
├── pal/             ← YOURS: platform abstraction (_pal)
└── shared/          ← YOURS: cross-cutting (_x)
```
