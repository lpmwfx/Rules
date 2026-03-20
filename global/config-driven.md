---
tags: [config, configuration, no-hardcoding, cfg, constants, settings]
concepts: [config-driven-design, settings-management, configuration]
requires: [global/topology.md]
feeds: [gateway/lifecycle.md, core/design.md]
related: [global/persistent-state.md, global/app-model.md, uiux/tokens.md, rust/constants.md, slint/states.md]
keywords: [config, constants, magic-numbers, hardcoded, gateway, cfg, struct, default, create-before-use]
layer: 1
---
# Config-Driven Design

> No hardcoded values — all constants come from `_cfg` structs loaded by Gateway

---

VITAL: Zero hardcoded values in business logic, UI, or adapter code
VITAL: Zero hardcoded values in UI styling — colors, sizes, spacing, fonts are design tokens (see uiux/tokens.md)
VITAL: Gateway is the sole entry point for loading configuration
RULE: Every configurable value lives in a `_cfg` struct
RULE: Config structs are passed as parameters — never accessed globally
RULE: Gateway loads config from disk on startup, passes it down the call chain
RULE: Config structs are immutable after startup — no runtime mutation
RULE: Default values are defined in Gateway's load function, not scattered in code
BANNED: Magic numbers in Core, Adapter, UI, or PAL
BANNED: Hardcoded strings (URLs, paths, thresholds, labels) outside `_cfg` structs
BANNED: `Config::default()` called outside Gateway — Gateway owns initialization
BANNED: Global mutable config singletons
BANNED: Environment variable reads outside Gateway

## Config vs State

Config and State are distinct concepts — never conflate them.

| Concept | Tag | Changes When? | Loaded By |
|---------|-----|---------------|-----------|
| Configuration | `_cfg` | App restart / explicit reload | Gateway at startup |
| State | `_sta` | During runtime | Gateway at startup, saved at shutdown |

RULE: `_cfg` structs are read-only during a session
RULE: `_sta` structs are read-write during a session — see persistent-state.md

## Config Struct Naming

RULE: Config struct names follow `<Layer>Config_cfg` or `<Feature>Config_cfg`
RULE: Each layer that needs config gets its own `_cfg` struct
RULE: Gateway composes layer configs into a root `AppConfig_cfg`

```
AppConfig_cfg {
    ui:      UiConfig_cfg,
    core:    CoreConfig_cfg,
    gateway: GatewayConfig_cfg,
    pal:     PalConfig_cfg,
}

UiConfig_cfg {
    theme: Theme_cfg,
    font_size: u16,
    animation_ms: u32,
}

CoreConfig_cfg {
    max_items: usize,
    retry_limit: u8,
    timeout_ms: u64,
}
```

## Gateway Loads, Others Receive

RULE: Gateway reads config file → constructs `AppConfig_cfg` → passes to each layer
RULE: Core receives `CoreConfig_cfg` as a parameter — it never calls a config API
RULE: Adapter receives `UiConfig_cfg` — it never reads env vars or files

```
// Good — config passed as parameter
fn process_items(items: &[Item_core], cfg: &CoreConfig_cfg) -> Result<Output_core, AppError_x> {
    if items.len() > cfg.max_items { ... }
}

// Bad — hardcoded limit
fn process_items(items: &[Item_core]) -> Result<Output_core, AppError_x> {
    if items.len() > 1000 { ... }  // BANNED: magic number
}

// Bad — config read inside Core
fn process_items(items: &[Item_core]) -> Result<Output_core, AppError_x> {
    let limit = std::env::var("MAX_ITEMS").unwrap_or("1000");  // BANNED: env in Core
}
```

## Config File Layout

RULE: Config files live in `~/.config/<app>/config/`
RULE: Gateway discovers config path via PAL — never hardcodes paths
RULE: Default config is written by Gateway on first run if config file is absent

```
~/.config/<app>/
├── config/
│   ├── app.toml       # AppConfig_cfg source
│   └── ui.toml        # UiConfig_cfg overrides (optional)
└── state/
    └── *.toml         # State files — see persistent-state.md
```

RESULT: Every configurable behavior is visible and changeable without code changes
REASON: Config-driven code is testable — inject any `_cfg` struct to control behavior


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
