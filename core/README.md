---
tags: [core, business-logic, pure, isolation]
concepts: [core-layer, pure-logic, domain-isolation]
related: [core/design.md, core/state.md, global/topology.md, global/app-model.md]
layer: 6
---
# Core Layer

> Pure business logic — no I/O, no UI, no platform dependencies

---

Core contains domain rules, computations, and state. Functions are pure where possible: same input, same output, no side effects. Platform needs go through PAL trait interfaces.

## Responsibilities

- **Business rules** — validate domain invariants
- **Domain computation** — calculate, transform, derive
- **Domain state** — `CoreState_sta` for caches and computed aggregates
- **Platform needs** — via injected `Arc<dyn SomePal_pal>`, never direct

## Rules

| File | Topic |
|------|-------|
| [design.md](design.md) | Core isolation, structure pattern, type conventions |
| [state.md](state.md) | CoreState, domain state management |

RULE: Core imports zero UI, Adapter, Gateway, or platform code
RULE: Testable with `cargo test` alone — no mocking of platform or I/O

See: [global/topology.md](../global/topology.md) | [global/app-model.md](../global/app-model.md)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
