---
tags: [core, business-logic, pure-functions, domain, stateless, hexagonal]
concepts: [pure-business-logic, domain-rules, core-isolation, input-output]
requires: [global/topology.md, global/app-model.md]
feeds: [core/state.md]
related: [global/adapter-layer.md, pal/design.md]
keywords: [core, pure-function, domain, business-logic, no-ui, no-io, no-platform, CoreState-sta, _core, isolation, same-input-same-output]
layer: 3
---
# Core Design

> Core is pure business logic — same input, same output, no side effects, no platform

---

VITAL: Core imports ZERO UI, Adapter, Gateway, or platform code — it is fully isolated
VITAL: Core functions are pure where possible — same input always produces the same output
RULE: Platform operations (file paths, clipboard, appearance) go through PAL — Core defines the need, PAL provides it
RULE: Core receives `AppConfig_cfg` and `CoreState_sta` as constructor parameters — never fetches them
RULE: One module per domain concern — one file, one responsibility, one `_core` type family
RULE: Core returns `Result<T, AppError_x>` — it never panics, never crashes silently
BANNED: `use slint`, `use gtk`, `use winit`, `use tokio`, `use std::fs`, `use reqwest` in Core
BANNED: Core knowing about screen names, view models, or UI structure
BANNED: Core calling Gateway or Adapter — it only calls PAL when platform behaviour is needed
BANNED: `_core` file importing a `_adp` type — Core must not know Adapter exists
BANNED: `_core` file importing a `_ui` type — Core must not know UI exists
BANNED: `_core` file importing a `_gtw` type — Core must not know IO exists

## What lives in Core

```
Core handles:
  ├── business rules         → validate data against domain invariants
  ├── domain computations    → calculate, transform, derive
  ├── domain state           → CoreState_sta — caches, active sessions, computed aggregates
  └── platform needs via PAL → file paths, clipboard content, current time

Core does NOT handle:
  ├── UI rendering           → Adapter + UI
  ├── disk IO                → Gateway
  ├── event routing          → Adapter
  └── platform-specific code → PAL
```

## Structure pattern

```rust
// src/core/schema_core.rs
pub struct SchemaCore_core {
    pal:   Arc<dyn FilePal_pal>,    // platform needs injected at construction
    state: CoreState_sta,
}

impl SchemaCore_core {
    pub fn new(pal: Arc<dyn FilePal_pal>, state: CoreState_sta) -> Self {
        Self { pal, state }
    }

    // Pure domain operation — validates business rules, returns domain result
    pub fn add_field(
        &mut self,
        collection_id: &str,
        field: FieldSpec_core,
    ) -> Result<Field_core, AppError_x> {
        self.validate_field_name(&field.name)?;           // business rule
        self.validate_no_duplicate(&field.name, collection_id)?;
        let field = self.state.schema.insert_field(collection_id, field)?;
        Ok(field)
    }

    fn validate_field_name(&self, name: &str) -> Result<(), AppError_x> {
        if name.is_empty() || name.len() > 64 {
            return Err(AppError_x::InvalidFieldName(name.to_string()));
        }
        Ok(())
    }
}
```

RULE: `_core` types are the domain vocabulary — `Field_core`, `Collection_core`, `Schema_core`
RULE: Validation of business rules belongs here — validation of input shape belongs in Adapter

RESULT: Core can be tested without a UI, disk, or OS — pure `cargo test` with no mocking of platform
REASON: Isolated Core means business logic survives a UI toolkit change, OS port, or storage engine swap
