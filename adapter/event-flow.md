---
tags: [adapter, event-flow, event-routing, dispatch, core, ui-events, state-push]
concepts: [event-flow, adapter-event-routing, core-dispatch, state-update-cycle]
requires: [adapter/viewmodel.md, global/adapter-layer.md]
related: [slint/rust-bridge.md, slint/globals.md, uiux/state-flow.md, gateway/lifecycle.md]
keywords: [on-callback, ui-on, Adapter-init, dispatch, validate, state-push, set-property, event-handler, input-validation, complete-state, Core-dispatch]
layer: 3
---
# Adapter Event Flow

> Receive UI event → validate input → dispatch to Core → map result → push complete state to UI

---

VITAL: Adapter is the ONLY layer that registers `ui.on_*()` event listeners — in `Adapter::init()`
<!-- DEPRECATED: state rules paused — see sid-architecture/code-free-of-mutables.md (prototype) -->
<!--
VITAL: After every event handler, push the COMPLETE updated `AdapterState_sta` to UI — not just changed fields
BANNED: Pushing partial state updates — always push the whole `AdapterState_sta` after a change
BANNED: Event handlers that read from `ui.get_*()` to decide what to do — state lives in Adapter, not UI
-->
<!-- /DEPRECATED -->

RULE: Event handler steps in order: validate input shape → dispatch to Core → map result to _adp → push state
RULE: Input shape validation belongs in Adapter — Core trusts its inputs and enforces business rules
RULE: All `ui.on_*()` registrations happen before `ui.run()` — never registered lazily or conditionally
RULE: Adapter::init() receives `ui`, `core`, and `state` — wires them together, returns self
BANNED: Business logic in event handlers — one call to Core, no conditions around it

## Event handler cycle

```
ui.on_collection_selected(id)
       │
       ├── 1. validate input shape
       │         if id.is_empty() { return; }
       │
       ├── 2. set loading state immediately
       │         state.is_loading = true;
       │         push_state(&ui, &state);
       │
       ├── 3. dispatch to Core
       │         let items = core.load_items(id)?;
       │
       ├── 4. map Core result → _adp view models
       │         state.items = items.iter().map(ItemViewModel_adp::from_core).collect();
       │         state.selected = collections.find(id).map(Into::into);
       │         state.is_loading = false;
       │         state.error_message = None;
       │
       └── 5. push complete state to UI
                 push_state(&ui, &state);
```

## Implementation pattern

```rust
// src/adapter/builder_adapter.rs
impl BuilderAdapter_adp {
    pub fn init(
        ui:    &AppWindow,
        core:  CoreState_core,
        state: AdapterState_sta,
    ) -> Self {
        let state = Rc::new(RefCell::new(state));
        let core  = Rc::new(RefCell::new(core));

        // Push initial state before registering listeners
        push_state(ui, &state.borrow());

        // Register ALL event listeners here
        {
            let ui_weak = ui.as_weak();
            let state   = state.clone();
            let core    = core.clone();

            ui.on_collection_selected(move |id| {
                if id.is_empty() { return; }

                let mut st = state.borrow_mut();
                st.is_loading = true;
                if let Some(ui) = ui_weak.upgrade() { push_state(&ui, &st); }

                match core.borrow().load_items(id.as_str()) {
                    Ok(items) => {
                        st.items = items.iter().map(ItemViewModel_adp::from_core).collect();
                        st.is_loading = false;
                        st.error_message = None;
                    }
                    Err(e) => {
                        st.is_loading = false;
                        st.error_message = Some(e.to_string());
                    }
                }

                if let Some(ui) = ui_weak.upgrade() { push_state(&ui, &st); }
            });
        }

        Self { core, state }
    }

    pub fn state(&self) -> AdapterState_sta { self.state.borrow().clone() }
}

// Push entire AdapterState_sta to Slint — always complete, never partial
fn push_state(ui: &AppWindow, st: &AdapterState_sta) {
    ui.set_collections(make_model(&st.collections));
    ui.set_items(make_model(&st.items));
    ui.set_is_loading(st.is_loading);
    ui.set_error_message(st.error_message.as_deref().unwrap_or("").into());
}
```

RESULT: Every UI state change originates in one place — the Adapter's event handler
REASON: Complete state pushes mean UI always reflects `AdapterState_sta` exactly — no partial renders


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
