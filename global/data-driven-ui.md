---
tags: [paradigm, data-driven, declarative, tokens, globals, adapter, reactive, architecture]
concepts: [data-driven-architecture, declarative-ui, adapter-controls-data, reactive-projection]
requires: [global/topology.md, global/config-driven.md]
feeds: [uiux/tokens.md, slint/states.md, rust/constants.md, slint/globals.md, global/naming-suffix.md]
related: [global/adapter-layer.md, global/persistent-state.md, uiux/theming.md, slint/themes.md, uiux/mother-child.md, global/mother-tree.md, web/components.md]
keywords: [data-driven, declarative, paradigm, out-property, set, adapter, reactive, projection, localization, theming, runtime, globals, state-files, create-before-use]
layer: 1
---
# Data-Driven UI — The Paradigm

> UI is a reactive projection of data. Adapter owns the data. Components are pure structure.

---

VITAL: This is not a naming system — it is a data-driven architecture
VITAL: Every token is a data source the Adapter can manipulate at runtime
VITAL: UI contains zero logic and zero values — it projects whatever the globals say

## The Core Idea

Every `out property` in a Slint global is a data endpoint.
Every `const` in a Rust `state/` module is a named data point.
Every `var(--token)` in CSS is an injectable value.

These are not "nice names for literals". They are **data sources** that the Adapter layer controls.

```
Traditional (imperative):
  Component hardcodes values → changing anything means editing components
  UI owns its own appearance → coupled to specific numbers and strings

Data-driven (this paradigm):
  Globals hold all values as out properties → Adapter set_*() controls them
  UI reads globals → pure reactive projection of data
  Change the data → UI updates automatically → zero component edits
```

## How It Works

```
┌─────────────┐     set_*()      ┌──────────────┐     reads      ┌──────────────┐
│   Adapter   │ ──────────────→  │   Globals    │ ←────────────  │  Components  │
│  (Rust)     │                  │  (Slint)     │                │  (Slint)     │
│             │                  │              │                │              │
│ owns data   │                  │ Theme.*      │                │ pure layout  │
│ owns logic  │                  │ Sizes.*      │                │ zero values  │
│ owns state  │                  │ Strings.*    │                │ zero logic   │
└─────────────┘                  └──────────────┘                └──────────────┘
```

1. **Globals** are `out property` declarations — Slint exposes them as `set_*()` methods to Rust
2. **Adapter** calls `set_*()` to push data into globals — colors, sizes, strings, state
3. **Components** bind to globals — they are reactive projections, not data owners
4. **Change a global** → every component using it updates instantly — Slint's reactive system

## What This Enables

| Capability | How |
|---|---|
| **Theming** | Adapter calls `set_accent()`, `set_bg_primary()` → entire UI re-themes |
| **Localization** | Adapter calls `set_save_label()`, `set_cancel_label()` → all text updates |
| **Runtime config** | User changes font size → Adapter calls `set_body_size()` → UI scales |
| **A/B testing** | Adapter swaps data set → UI shows variant B with zero code change |
| **Accessibility** | Adapter detects high-contrast → pushes different color tokens |
| **Dark mode** | Adapter reads system preference → sets color globals → instant switch |

All of these are the same operation: **Adapter pushes different data into globals**.

## The Tokens Are Data Sources

```slint
// This is NOT "a nice name for 100%"
// This IS a data endpoint the Adapter can change at runtime
export global Sizes {
    out property <length> pct-100: 100%;    // Adapter could set_pct_100() to 80% for compact mode
    out property <length> sidebar: 240px;   // Adapter could set_sidebar() to 0px to collapse it
}

// This is NOT "a nice name for a string"
// This IS a localization endpoint
export global Strings {
    out property <string> kind-dialogue: "dialogue";  // could be "dialoog" in Dutch
    out property <string> save: "Save";               // could be "Speichern" in German
}
```

RULE: Think of every token as a runtime-controllable data endpoint
RULE: The default value in the global file is just the initial state — Adapter can override it
RULE: Components must never know WHERE data comes from — they just read globals

## The Three Layers

| Layer | Contains | Owns |
|---|---|---|
| **State files** (`state/`, `globals/theme/`) | All concrete values — the data | Default values |
| **Adapter** (Rust) | `set_*()` calls — the controller | Runtime decisions |
| **Components** (Slint) | Layout + bindings — the projection | Nothing — reads only |

RULE: Values flow one way: state files → globals → components
RULE: Control flows one way: Adapter → globals (via set)
RULE: Components never push values — they bind and react

## Create-Before-Use

Globals start empty. The developer populates them as components are built:

1. Need a value in a component → it must exist in a global
2. Global does not have it → create the `out property` in the global file FIRST
3. Then bind to it in the component
4. The literal value appears ONLY in the global file — never in a component

This is not busywork. Each `out property` you create is a new data endpoint the Adapter can control. You are building the data API of your UI.

## Rust Side — Same Paradigm

The same separation applies to Rust code:

```
state/ modules = data layer     (const values, default endpoints)
_cfg structs   = runtime data   (loaded from disk, injectable)
function bodies = logic layer   (declarative, references only names)
```

A `const TIMEOUT: Duration = Duration::from_secs(30)` is not "a name for 30" — it is a data point that could move to `_cfg` and become runtime-configurable without changing any function.

See [rust/constants.md](../rust/constants.md) for the Rust-specific workflow.

## Contract

This paradigm is non-negotiable. Scanners enforce it:
- `slintscanners` — ERROR on any literal in a .slint component
- `rustscanners` — ERROR on any literal ≥ 2 in a Rust function body
- `rulestools` — ERROR on hardcoded values across all languages

The enforcement is automatic. The paradigm is not a style choice — it is the architecture.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
