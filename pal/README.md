---
tags: [pal, overview, platform, abstraction, traits, ffi]
concepts: [pal-layer, platform-abstraction, trait-per-concern]
related: [pal/design.md, pal/traits.md, global/topology.md, global/app-model.md]
layer: 6
---
# PAL Layer (Platform Abstraction Layer)

> One trait per concern, one implementation per platform — only layer with unsafe and FFI

---

PAL defines trait interfaces per concern (`FilePal_pal`, `WindowPal_pal`, `AppearancePal_pal`) with per-platform implementations. It is stateless: delegates to platform APIs, returns a result, holds nothing.

## Responsibilities

- **Trait definitions** — one trait per platform concern
- **Platform implementations** — one struct per target OS per trait
- **FFI wrappers** — safe API over unsafe platform calls
- **Path resolution** — platform-correct config/data/cache paths

## Rules

| File | Topic |
|------|-------|
| [design.md](design.md) | Trait pattern, injection, platform selection |
| [traits.md](traits.md) | Trait catalogue, naming, implementation guide |

RULE: `#[cfg(target_os)]` lives ONLY inside PAL implementations
RULE: Only layer allowed to use `unsafe` code and OS-specific crates
RULE: Adding a new platform = one new `_pal` implementation — zero changes elsewhere

See: [global/topology.md](../global/topology.md) | [global/app-model.md](../global/app-model.md)
