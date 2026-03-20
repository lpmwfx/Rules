---
tags: [rust, adapter, bridge, api, event-listeners, state-push, mvvm]
concepts: [rust-slint-bridge, adapter-event-routing, state-push, type-mapping]
requires: [slint/component-model.md, global/adapter-layer.md, global/topology.md]
feeds: [slint/threading.md]
related: [uiux/state-flow.md, slint/globals.md, slint/validation.md]
keywords: [set-property, get-property, on-callback, invoke-callback, AdapterState-sta, event-listener, Adapter-init, SharedString, ModelRc, VecModel, as-weak]
layer: 3
---
# Slint Rust Bridge

> Adapter registers all `ui.on_*()` listeners and owns all `ui.set_*()` state pushes

---

VITAL: ONLY the Adapter layer (`_adp`) calls `ui.set_*()`, `ui.on_*()`, `ui.invoke_*()` — never Core, Gateway, or PAL
VITAL: `ui.on_*()` registrations ARE the event-routing described in adapter-layer.md — they go in `Adapter::init()`
RULE: Register all `ui.on_*()` handlers before `ui.run()` — in `Adapter::init()` or equivalent setup function
RULE: After every event handler: map result to view model, update AdapterState_sta, push all changed fields via `set_*()`
RULE: Always call `ui.as_weak()` before moving `ui` into a closure — required for re-entry and safe drop
BANNED: Any layer other than Adapter calling Slint API
BANNED: Calling `ui.set_*()` or `ui.on_*()` from a background thread — use `invoke_from_event_loop()` (see threading.md)

## Boot order and init

```rust
// main.rs — boot order: Gateway → Core → Adapter → ui.run()
fn main() -> Result<(), AppError_x> {
    let (cfg, state) = GatewayState_gtw::init()?;         // load config + persisted state
    let core         = CoreState_core::init(cfg.core)?;   // pure domain init
    let ui           = AppWindow::new()?;
    let adapter      = BuilderAdapter_adp::init(&ui, core, state.adapter)?;  // registers all listeners
    ui.run()?;
    GatewayState_gtw::shutdown(adapter.state())           // persist state on exit
}
```

## Adapter::init — registering event listeners

```rust
// src/adapter/builder_adapter.rs
impl BuilderAdapter_adp {
    pub fn init(ui: &AppWindow, core: CoreState_core, state: AdapterState_sta) -> Self {
        // 1. Push initial state to Slint
        ui.set_collections(make_model(&state.collections));
        ui.set_selected_collection(state.selected.clone().map(Into::into).unwrap_or_default());
        ui.set_is_loading(false);

        // 2. Register ALL event listeners here — this IS the event routing
        let ui_weak = ui.as_weak();
        let core = Rc::new(RefCell::new(core));

        {
            let ui_weak = ui_weak.clone();
            let core = core.clone();
            ui.on_collection_selected(move |id| {
                let items = core.borrow().load_items(id.as_str());
                if let Some(ui) = ui_weak.upgrade() {
                    ui.set_items(make_model(&items));
                    ui.set_selected_collection_id(id);
                }
            });
        }

        {
            let ui_weak = ui_weak.clone();
            ui.on_save_requested(move |data| {
                // validate input shape (not business logic — that's Core)
                if data.name.is_empty() { return; }
                // dispatch to Core, map result, push state back
                if let Some(ui) = ui_weak.upgrade() {
                    ui.set_is_loading(true);
                }
            });
        }

        Self { ui: ui_weak, core, state: AdapterState_sta::default() }
    }
}
```

## Type mapping

| Slint type | Rust type | Conversion |
|------------|-----------|------------|
| `string` | `SharedString` | `"text".into()` / `SharedString::from(s)` / `slint::format!()` |
| `int` | `i32` | direct |
| `float` | `f32` | direct |
| `bool` | `bool` | direct |
| `[T]` model | `ModelRc<T>` | `Rc::new(VecModel::from(vec)).into()` |
| custom struct | generated struct | defined in `.slint`, available after `include_modules!()` |

RULE: Use `SharedString` in all Slint-facing Rust code — never pass `String` or `&str` directly
RULE: Custom structs defined in `.slint` are flat, serializable view models — no domain logic (`_adp` role)
RULE: Domain objects (`_core`) are always mapped to generated Slint structs in the Adapter — never passed through

## Models

```rust
fn make_model(items: &[ItemViewModel_adp]) -> ModelRc<UiItem> {
    let rows: Vec<UiItem> = items.iter()
        .map(|i| UiItem { id: i.id.as_str().into(), title: i.title.as_str().into() })
        .collect();
    Rc::new(VecModel::from(rows)).into()
}

// Mutate in-place (avoids full re-render for append/update)
if let Some(model) = ui.get_items().as_any().downcast_ref::<VecModel<UiItem>>() {
    model.push(new_row);
}
```

RULE: Wrap `VecModel<T>` in `Rc::new(...).into()` — Slint requires `ModelRc<T>`
RULE: Use `FilterModel` / `SortModel` for filtered views — do not pre-filter in the Adapter

RESULT: All state changes originate in the Adapter and are traceable through `set_*()` calls
REASON: Centralised Slint ownership means every UI update is one grep away from the source


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
