---
tags: [naming, suffix, layer-tag, type-naming, architecture, grep]
concepts: [layer-tag-naming, type-placement, grep-topology]
requires: [global/stereotypes.md, global/topology.md]
related: [global/persistent-state.md, global/config-driven.md, adapter/viewmodel.md, core/design.md, pal/design.md, gateway/io.md, uiux/state-flow.md, slint/component-model.md, global/data-driven-ui.md]
keywords: [suffix, _adp, _core, _pal, _gtw, _ui, _x, _sta, _cfg, _test, layer-tag, type-name, grep, placement, PascalCase]
layer: 1
---
# Type Naming — Layer Tag Suffix

> Every public type carries its layer tag — `BuilderAdapter_adp`, `CoreState_sta`, `AppConfig_cfg`

---

VITAL: All public types have a layer tag suffix — the tag identifies where the type lives and what it does
VITAL: Tag and folder always agree — `_adp` lives in `src/adapter/`, `_gtw` lives in `src/gateway/`
RULE: Suffix is appended to the PascalCase type name — `TypeName_tag`
RULE: `grep _adp` finds every Adapter type across all files — the tag is the search key
RULE: `_sta` and `_cfg` override the layer tag — state and config structs use their own suffix regardless of layer
BANNED: Public types without a layer tag suffix
BANNED: Tag and folder disagreeing — `_core` type in `src/adapter/` is a placement error

## Layer tag table

| Tag | Folder | Role | Rules file |
|-----|--------|------|------------|
| `_ui` | `src/ui/` | Declarative views, components, templates | [uiux/](../uiux/README.md) · [slint/](../slint/README.md) |
| `_adp` | `src/adapter/` | ViewModel, event routing, domain→UI mapping | [adapter/viewmodel.md](../adapter/viewmodel.md) |
| `_core` | `src/core/` | Domain types, business logic, pure functions | [core/design.md](../core/design.md) |
| `_pal` | `src/pal/` | Platform abstraction interfaces and implementations | [pal/design.md](../pal/design.md) |
| `_gtw` | `src/gateway/` | IO adapter — config load, state persist, network | [gateway/io.md](../gateway/io.md) |
| `_x` | `src/shared/` | Cross-cutting — errors, results, shared traits | any layer |
| `_sta` | any layer | Mutable session state — persisted by Gateway | [global/persistent-state.md](persistent-state.md) |
| `_cfg` | any layer | Immutable config — loaded once by Gateway at startup | [global/config-driven.md](config-driven.md) |
| `_test` | `tests/` | Test doubles, fixtures, test-only helpers | mirror of `src/` |

## Examples

```rust
// Layer types — tag = folder
pub struct BuilderAdapter_adp { ... }   // src/adapter/
pub struct SchemaCore_core     { ... }  // src/core/
pub struct WindowsPal_pal      { ... }  // src/pal/
pub struct RuntimeGateway_gtw  { ... }  // src/gateway/
pub struct FieldRow_ui         { ... }  // src/ui/

// State and config — tag overrides layer
pub struct AdapterState_sta    { ... }  // lives in src/adapter/, tagged _sta
pub struct CoreState_sta       { ... }  // lives in src/core/, tagged _sta
pub struct AppConfig_cfg       { ... }  // lives in src/gateway/, tagged _cfg
pub struct CoreConfig_cfg      { ... }  // lives in src/core/, tagged _cfg

// Shared / cross-cutting
pub struct AppError_x          { ... }  // src/shared/
pub type   BuilderResult_x<T>  = Result<T, AppError_x>;

// Test double
pub struct TestFilePal_pal     { ... }  // tests/ or src/pal/ — tagged as PAL impl
```

## Grep as topology

The tag suffix is a grep-searchable architecture map:

```
grep _gtw   → all Gateway types       (IO boundary)
grep _adp   → all Adapter types       (ViewModel, event routing)
grep _core  → all Core domain types   (business logic)
grep _sta   → all state structs       (persisted by Gateway)
grep _cfg   → all config structs      (loaded at startup)
```

RULE: When in doubt where a type belongs — pick the layer, apply the tag, move it to the matching folder
RULE: If a type spans two layers, move it to `_x` (shared)

RESULT: Type origin is readable without opening the file — the tag is the address
REASON: AI and humans can navigate the codebase by grep alone — no IDE required
