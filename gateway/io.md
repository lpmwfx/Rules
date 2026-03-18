---
tags: [gateway, io, pal, disk, network, io-boundary, result]
concepts: [io-boundary, gateway-pattern, pal-delegation, error-propagation]
requires: [global/topology.md, global/persistent-state.md]
feeds: [gateway/lifecycle.md]
related: [global/app-model.md, web/gateway.md]
keywords: [gateway, pal, disk, io, file, read, write, result, AppError, syscall, io-boundary, one-gateway]
layer: 3
---
# Gateway IO

> Gateway is the only layer that touches disk, network, and processes — everything else is pure

---

VITAL: Gateway is the ONLY layer that performs IO — file read/write, network, subprocess, clipboard
VITAL: All IO returns `Result<T, AppError_x>` — Gateway never panics on IO failure
RULE: Gateway delegates all actual IO to PAL — no direct syscalls, no `std::fs` outside Gateway
RULE: Gateway functions take `_cfg` and `_sta` types as parameters — no global state
RULE: One Gateway module per IO concern — `RuntimeGateway_gtw`, `PublishGateway_gtw`, `McpGateway_gtw`
RULE: Path resolution always goes through PAL — never hardcode `~/.config` or platform paths
BANNED: `std::fs::read`, `std::fs::write`, `reqwest::get` outside Gateway
BANNED: `unwrap()` on any IO operation — surface all errors as `Result`
BANNED: Gateway modules containing business logic — IO marshalling only
BANNED: `_gtw` file importing a `_adp` type — Gateway must not know Adapter exists
BANNED: `_gtw` file importing a `_ui` type — Gateway must not know UI exists

## What belongs in Gateway

```
Gateway handles:
  ├── config file read/parse   → AppConfig_cfg
  ├── state file read/write    → <Layer>State_sta (via Persistable_x)
  ├── database connections     → connection pool, query execution
  ├── network calls            → HTTP, WebSocket, RPC
  ├── subprocess               → spawn, stdin/stdout pipe
  └── clipboard / OS APIs      → via PAL interface

Gateway does NOT handle:
  ├── business rules           → Core
  ├── UI events                → Adapter
  └── data transformation      → Adapter
```

## IO pattern

```rust
// src/gateway/runtime_gateway.rs
pub struct RuntimeGateway_gtw {
    pal: Arc<dyn FilePal_pal>,
    state: GatewayState_sta,
}

impl RuntimeGateway_gtw {
    pub fn load_config(&self) -> Result<AppConfig_cfg, AppError_x> {
        let path = self.pal.config_path("app.toml")?;
        let raw  = self.pal.read_file(&path)?;
        AppConfig_cfg::deserialize(&raw).map_err(AppError_x::Config)
    }

    pub fn save_state(&self, state: &dyn Persistable_x) -> Result<(), AppError_x> {
        let path = self.pal.state_path(&format!("{}.toml", state.state_key()))?;
        self.pal.write_file(&path, &state.serialize()?)
    }
}
```

RULE: Gateway structs hold a PAL reference — IO calls go through it, not through `std` directly
RULE: Each Gateway method does one IO operation — no compound multi-step methods that mix concerns

RESULT: IO errors have one origin — Gateway — making failure modes easy to reason about
REASON: Layers that cannot do IO cannot corrupt state or leave partial writes
