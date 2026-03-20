---
tags: [adapter, data-exchange, viewmodel, events]
concepts: [adapter-layer, data-hub, event-routing]
related: [adapter/viewmodel.md, adapter/event-flow.md, global/adapter-layer.md, global/topology.md, global/app-model.md]
layer: 6
---
# Adapter Layer

> The data exchange hub — owns viewmodel state, routes events, translates types

---

Adapter sits between Core/Gateway and UI. It owns `AdapterState_sta`, maps `_core` types to `_adp` view models, and routes UI events to the correct layer. No business logic, no I/O.

## Responsibilities

- **State ownership** — `AdapterState_sta` is the complete UI-ready snapshot
- **Type mapping** — `_core` to `_adp` conversions in `mapping.rs`
- **Event routing** — UI callbacks dispatch to Core or Gateway
- **Status flags** — `is_loading`, `error_message`, `is_empty` always explicit

## Rules

| File | Topic |
|------|-------|
| [viewmodel.md](viewmodel.md) | ViewModel types, AdapterState, domain mapping |
| [event-flow.md](event-flow.md) | Event routing, callback dispatch |

See: [global/adapter-layer.md](../global/adapter-layer.md) | [global/topology.md](../global/topology.md)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
