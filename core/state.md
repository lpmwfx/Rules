---
tags: [core, state, CoreState-sta, domain-state, session, cache]
concepts: [core-state, domain-session-state, state-ownership]
requires: [core/design.md, global/persistent-state.md]
related: [adapter/viewmodel.md, gateway/lifecycle.md]
keywords: [CoreState-sta, domain-state, session, cache, computed, Gateway-init, Persistable-x, _sta, _core, state-key]
layer: 3
---
# Core State

> CoreState_sta owns domain session data — caches, active sessions, computed aggregates

---

RULE: `CoreState_sta` holds domain session state — computed results, active selections, caches
RULE: Gateway deserializes `CoreState_sta` from disk on startup and passes it to Core as a parameter
RULE: Core updates `CoreState_sta` internally — no other layer mutates it directly
RULE: Gateway serializes `CoreState_sta` to disk on shutdown via `Persistable_x`
RULE: `CoreState_sta` contains only domain types (`_core`, `_x`) — never view models (`_adp`)
BANNED: UI state (scroll, selection, active panel) in `CoreState_sta` — that belongs in `AdapterState_sta`
BANNED: Config values in `CoreState_sta` — config is `_cfg`, state is `_sta`

## What belongs in CoreState_sta

```
CoreState_sta holds:
  ├── loaded schema / domain model    (expensive to recompute — cached here)
  ├── active session data             (current user, active transaction)
  ├── computed aggregates             (counts, summaries recomputed on change)
  └── domain-layer feature flags      (not UI visibility — domain behaviour)

CoreState_sta does NOT hold:
  ├── which panel is open             → AdapterState_sta
  ├── scroll position                 → AdapterState_sta
  ├── is_loading flag                 → AdapterState_sta
  └── config values                  → AppConfig_cfg
```

## Implementation

```rust
// src/core/state.rs
#[derive(Default, Serialize, Deserialize)]
pub struct CoreState_sta {
    pub schema:         Schema_core,
    pub active_project: Option<ProjectId_core>,
    pub field_cache:    HashMap<String, Vec<Field_core>>,
}

impl Persistable_x for CoreState_sta {
    fn state_key() -> &'static str { "core" }

    fn serialize(&self) -> Result<String, AppError_x> {
        toml::to_string(self).map_err(AppError_x::Serialize)
    }

    fn deserialize(data: &str) -> Result<Self, AppError_x> {
        toml::from_str(data).map_err(AppError_x::Deserialize)
    }
}
```

RULE: `state_key()` matches the filename Gateway writes — `"core"` → `state/core.toml`
RULE: `Default` implementation is the first-run state — no separate init logic needed

RESULT: Core starts from a known state every session — Gateway is the only code that touches the file
REASON: `grep CoreState_sta` finds every place domain session state is read or written
