---
tags: [gateway, lifecycle, startup, shutdown, init, state, config, boot-order]
concepts: [gateway-lifecycle, startup-sequence, shutdown-sequence, state-distribution]
requires: [gateway/io.md, global/persistent-state.md, global/config-driven.md]
related: [global/app-model.md, adapter/event-flow.md]
keywords: [init, shutdown, startup, boot-order, distribute, AppConfig-cfg, AdapterState-sta, CoreState-sta, serialize, deserialize, Persistable-x]
layer: 3
---
# Gateway Lifecycle

> Gateway is initialized first and shut down last — it owns every layer's state on disk

---

VITAL: Gateway::init runs BEFORE Core, Adapter, and UI — it is the boot entry point
<!-- DEPRECATED: state rules paused — see sid-architecture/data-driven-runtime.md (prototype) -->
<!--
VITAL: Gateway::shutdown runs AFTER ui.run() returns — all _sta structs are written to disk here
RULE: Gateway returns fully parsed `_cfg` and `_sta` structs to the caller — layers receive, not fetch
RULE: Gateway collects all `_sta` registrations at init time — no runtime state discovery
RULE: If a state file does not exist, Gateway returns the default `_sta` — never an error
BANNED: Layers fetching their own config or state from disk — Gateway hands it to them
BANNED: Writing state mid-session from outside Gateway — flush via Gateway only
-->
<!-- /DEPRECATED -->
RULE: Partial state corruption → log warning, use default — never abort the whole app
BANNED: `_gtw` file importing a `_adp` type — Gateway must not know Adapter exists
BANNED: `_gtw` file importing a `_ui` type — Gateway must not know UI exists

## Boot order

```
main()
  │
  ├── 1. Gateway::init(pal)
  │     ├── PAL resolves config + state paths
  │     ├── read + parse AppConfig_cfg
  │     ├── read + deserialize AdapterState_sta  (default if missing)
  │     ├── read + deserialize CoreState_sta      (default if missing)
  │     └── returns (AppConfig_cfg, AllState_gtw)
  │
  ├── 2. Core::init(cfg.core, state.core)
  ├── 3. Adapter::init(ui, core, cfg.adapter, state.adapter)
  ├── 4. ui.run()                              ← event loop blocks here
  │
  └── 5. Gateway::shutdown(adapter.state(), core.state())
        ├── serialize AdapterState_sta → disk
        ├── serialize CoreState_sta    → disk
        └── serialize GatewayState_sta → disk
```

## Implementation pattern

```rust
// src/gateway/mod.rs
pub struct AllState_gtw {
    pub adapter: AdapterState_sta,
    pub core:    CoreState_sta,
}

impl RuntimeGateway_gtw {
    pub fn init(pal: Arc<dyn FilePal_pal>) -> Result<(AppConfig_cfg, AllState_gtw), AppError_x> {
        let cfg     = Self::load_config(&pal)?;
        let adapter = Self::load_or_default::<AdapterState_sta>(&pal, "adapter")?;
        let core    = Self::load_or_default::<CoreState_sta>(&pal, "core")?;
        Ok((cfg, AllState_gtw { adapter, core }))
    }

    pub fn shutdown(&self, adapter: &AdapterState_sta, core: &CoreState_sta) {
        // best-effort — log errors but do not propagate (process is exiting)
        if let Err(e) = self.save_state(adapter) { tracing::warn!("state save failed: {e}"); }
        if let Err(e) = self.save_state(core)    { tracing::warn!("state save failed: {e}"); }
    }

    fn load_or_default<T: Persistable_x + Default>(
        pal: &Arc<dyn FilePal_pal>, key: &str
    ) -> Result<T, AppError_x> {
        let path = pal.state_path(&format!("{key}.toml"))?;
        match pal.read_file(&path) {
            Ok(raw)  => T::deserialize(&raw).unwrap_or_else(|e| {
                tracing::warn!("corrupt {key} state, using default: {e}");
                T::default()
            }),
            Err(_)   => Ok(T::default()),   // first run — file does not exist
        }
    }
}
```

RESULT: Every app has a predictable startup — layers always receive config and state, never fetch them
REASON: Layers that cannot initiate IO cannot fail at IO — Gateway is the single point of recovery


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
