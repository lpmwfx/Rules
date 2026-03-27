---
tags: [topology, profiles, project-types, architecture]
concepts: [topology-profiles, project-type-mapping, layer-activation]
requires: [global/topology.md]
feeds: [php/laravel/topology.md, js/topology-cli.md, js/topology-mcp.md, web/topology.md, rust/topology.md]
related: [global/app-model.md, core/design.md, adapter/viewmodel.md, gateway/io.md, pal/design.md]
keywords: [profile, gui, cli, mcp, daemon, pwa, spa, blade, desktop, server, project-type]
layer: 1
---
# Topology Profiles

> Same 6 layers, different activation — project type determines the shape

---

Topology is universal. Every project has core, gateway, and shared. What changes is which layers are active and what they map to concretely.

RULE: Choose profile at project start — it determines folder structure and layer activation
RULE: Inactive layers are absent, not empty folders

## Profile Overview

| Profile | ui | adapter | core | gateway | pal | shared |
|---|---|---|---|---|---|---|
| **gui-desktop** | views, components | viewmodel, events | domain logic | disk, network | OS APIs | errors, types |
| **gui-web** | Svelte pages | Inertia / viewmodel | domain logic | fetch, IndexedDB | Web APIs | errors, types |
| **cli** | — | stdio, args parser | domain logic | disk, network | OS APIs | errors, types |
| **mcp-server** | — | tools (MCP) | domain logic | disk, network, API | runtime (Bun) | errors, types |
| **daemon** | — | API endpoints | domain logic | disk, network | OS APIs | errors, types |
| **blade-admin** | Blade (thin) | controllers | domain logic | DB, disk | — | errors, types |

## Layer Definitions

Each layer has a dedicated definition file — read these for rules, not this overview.

| Layer | Tag | Definition | Responsibility |
|---|---|---|---|
| ui | `_ui` | [uiux/README.md](../uiux/README.md) | Declarative rendering — views, components, templates |
| adapter | `_adp` | [adapter/viewmodel.md](../adapter/viewmodel.md) | Data exchange hub — transforms between core and ui/stdio/tools |
| core | `_core` | [core/design.md](../core/design.md) | Business logic — pure functions, domain rules, no IO |
| gateway | `_gtw` | [gateway/io.md](../gateway/io.md) | IO boundary — disk, network, processes, DB |
| pal | `_pal` | [pal/design.md](../pal/design.md) | Platform abstraction — OS, runtime, hardware interfaces |
| shared | `_x` | below | Cross-layer types — errors, result types, enums used by 2+ layers |

## Shared (`_x`) — Definition

Shared is NOT "utils" or "helpers". It holds types that cross layer boundaries:

- **Error types** — `AppError_x`, error enums (definition, not handling — handling is in core)
- **Result types** — `Result<T, AppError_x>` wrappers
- **Cross-layer enums** — enums used by 2+ layers (e.g. `FileFormat_x`)
- **Value objects** — types with no behavior, used across layers

RULE: A type belongs in shared only if it is imported by 2+ layers
RULE: If a type is only used within one layer, it belongs in that layer
BANNED: `utils/`, `helpers/`, `common/` as shared — shared has strict membership criteria
BANNED: Functions in shared — shared holds types and constants, not logic

## Per-Profile Twins

Each profile has a concrete mapping file in its language/framework area:

| Profile | Twin file |
|---|---|
| gui-desktop (Rust+Slint) | [rust/topology.md](../rust/topology.md) |
| gui-web (Laravel+Svelte) | [php/laravel/topology.md](../php/laravel/topology.md) |
| gui-web (PWA/SPA) | [web/topology.md](../web/topology.md) |
| cli (Bun/Node) | [js/topology-cli.md](../js/topology-cli.md) |
| mcp-server (Bun) | [js/topology-mcp.md](../js/topology-mcp.md) |
| blade-admin | [php/laravel/topology.md](../php/laravel/topology.md) |
