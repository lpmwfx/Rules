---
tags: [gateway, io, boundary, lifecycle]
concepts: [gateway-layer, io-boundary, startup-shutdown]
related: [gateway/io.md, gateway/lifecycle.md, global/topology.md, global/app-model.md]
layer: 6
---
# Gateway Layer

> The I/O boundary — all disk, network, process, and database access goes here

---

Gateway is the only layer that performs I/O. It reads config, persists state, makes network calls, and spawns processes. All actual I/O is delegated to PAL. First layer to init, last to shutdown.

## Responsibilities

- **Config loading** — `AppConfig_cfg` from disk
- **State persistence** — read/write `<Layer>State_sta` via `Persistable_x`
- **Network calls** — HTTP, WebSocket, RPC
- **Subprocess management** — spawn, pipe stdin/stdout
- **Lifecycle** — first to initialize, last to shut down

## Rules

| File | Topic |
|------|-------|
| [io.md](io.md) | IO pattern, PAL delegation, error handling |
| [lifecycle.md](lifecycle.md) | Startup/shutdown order, state loading |

RULE: All IO returns `Result<T, AppError_x>` — Gateway never panics on IO failure
RULE: No business logic in Gateway — IO marshalling only

See: [global/topology.md](../global/topology.md) | [global/app-model.md](../global/app-model.md)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
