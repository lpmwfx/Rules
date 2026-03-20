---
tags: [adapter, viewmodel, adp, state, mapping, flat-struct, ui-ready]
concepts: [viewmodel, domain-mapping, adapter-state, ui-ready-struct]
requires: [global/topology.md, global/adapter-layer.md]
feeds: [adapter/event-flow.md]
related: [global/persistent-state.md, uiux/state-flow.md, slint/rust-bridge.md]
keywords: [AdapterState-sta, ItemViewModel-adp, flat-struct, domain-mapping, _adp, _core, ui-ready, selected, is-loading, error-message, ViewModelType]
layer: 3
---
# Adapter ViewModel

> Domain objects stop at the Adapter boundary — UI only sees flat, UI-ready structs

---

VITAL: Domain objects (`_core`) never reach the UI — Adapter maps them to `_adp` view models first
VITAL: `AdapterState_sta` is the complete description of what the UI renders right now
RULE: View model types are flat, serializable structs tagged `_adp` — no methods, no domain logic
RULE: One `AdapterState_sta` per Adapter module — it contains exactly what that view needs
RULE: Map at the Adapter boundary — Core returns `_core`, Adapter converts to `_adp` immediately
RULE: Status flags (`is_loading`, `error_message`, `is_empty`) are always explicit in `AdapterState_sta`
RULE: `AdapterState_sta` is initialized from Gateway on startup and persisted on shutdown
BANNED: `_core` types in `AdapterState_sta` or passed to `ui.set_*()`
BANNED: Computed display values (formatted strings, derived booleans) in `_core` types — compute in Adapter
BANNED: Optional fields that hide loading or error state — make all states explicit

## AdapterState_sta shape

```rust
// src/adapter/state.rs
#[derive(Default, Serialize, Deserialize)]
pub struct AdapterState_sta {
    // Content — what the user sees
    pub collections: Vec<CollectionViewModel_adp>,
    pub selected:    Option<CollectionViewModel_adp>,
    pub items:       Vec<ItemViewModel_adp>,

    // Status — always explicit, never inferred in UI
    pub is_loading:    bool,
    pub error_message: Option<String>,

    // UI state — persisted so user returns to where they left off
    pub scroll_offset: u32,
    pub active_panel:  PanelId_adp,
}
```

## View model types

```rust
// src/adapter/types.rs — flat, UI-ready, no domain logic
pub struct CollectionViewModel_adp {
    pub id:           String,
    pub display_name: String,       // formatted for UI — never raw sql_name
    pub item_count:   u32,
    pub is_selected:  bool,
}

pub struct ItemViewModel_adp {
    pub id:            String,
    pub display_name:  String,
    pub preview_text:  String,      // truncated, formatted — Adapter computed
    pub created_at:    String,      // formatted date string — not NaiveDateTime
}
```

## Domain → ViewModel mapping

```rust
// src/adapter/mapping.rs
impl CollectionViewModel_adp {
    pub fn from_core(c: &Collection_core, selected_id: Option<&str>) -> Self {
        Self {
            id:           c.id.to_string(),
            display_name: c.display_name.clone(),
            item_count:   c.item_count,
            is_selected:  selected_id == Some(c.id.as_str()),
        }
    }
}
```

RULE: Mapping functions live in `src/adapter/mapping.rs` — one place for all `_core` → `_adp` conversions
RULE: Dates, prices, counts — format to display strings in the mapping, not in the UI component

RESULT: Changing domain type `Collection_core` requires updating only `src/adapter/mapping.rs`
REASON: UI never depends on domain representation — the mapping is the only coupling point


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
