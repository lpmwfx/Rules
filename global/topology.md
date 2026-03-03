---
tags: [topology, architecture, hexagonal, mvvm, layers, dag, folder-structure, project-structure, ui]
concepts: [architecture, layer-topology, dependency-graph, hexagonal-mvvm, app-structure]
feeds: [global/adapter-layer.md, global/config-driven.md, global/persistent-state.md, core/design.md, pal/design.md]
related: [global/app-model.md]
keywords: [ui, adapter, core, pal, gateway, shared, folder-structure, import-rules, dag, placement, project, setup, app-layout, src, init, directory]
layer: 1
---
# Application Topology

> 6-layer hexagonal MVVM — every file has a home, every import has a direction

---

VITAL: All projects follow this 6-layer folder topology — no exceptions
VITAL: Import direction is one-way — lower layers never import higher layers
RULE: Each type's suffix tag matches its folder (e.g. `_adp` lives in `src/adapter/`)
RULE: Folder name maps directly to suffix tag — no ambiguity
RULE: Gateway is the only layer that touches external IO (disk, network, processes)
RULE: Adapter is the only layer that imports from all other layers
BANNED: Circular imports between layers
BANNED: UI importing Core directly — all communication goes through Adapter
BANNED: Core importing UI, Adapter, or Gateway
BANNED: Types living outside their designated folder

## Folder → Tag Mapping

| Folder | Tag | Role |
|--------|-----|------|
| `src/ui/` | `_ui` | Declarative UI layer — views, components, templates; or MCP server (AI interface) |
| `src/adapter/` | `_adp` | Data exchange hub — routing, transformation, ViewModel |
| `src/core/` | `_core` | Business logic — pure functions, domain rules |
| `src/pal/` | `_pal` | Platform abstraction — OS, window, filesystem interface |
| `src/gateway/` | `_gtw` | IO adapter — loads config+state, saves at shutdown |
| `src/shared/` | `_x` | Cross-cutting — errors, results, shared traits |

RULE: A type tagged `_adp` lives in `src/adapter/` — tag and folder always agree
RULE: State structs use `_sta` tag regardless of layer — see persistent-state.md
RULE: Config structs use `_cfg` tag regardless of layer — see config-driven.md

## Dependency DAG

```
GUI (_ui)  ◄──props───┐
                       │  Adapter  ──dispatch──►  Core
MCP (_ui)  ◄──data────┘    │◄────── results ────┤
    │                       │                     │
    └──events──────────────►│                     ▼
GUI └──events──────────────►│              PAL  ──abstracts──►  Platform
                             ▼              (iOS, Android, Win, Linux)
                          Gateway ──IO──►
                             │              ▲
                             └──────────────┘
```

RULE: GUI and MCP are both `_ui` — alternative rendering surfaces for the same Adapter state
RULE: `--mcp` flag switches the UI surface from GUI to MCP — Core, Gateway, PAL are identical in both modes

RULE: UI ↔ Adapter (events up, computed props down)
RULE: Adapter → Core (dispatch); Core → Adapter (results/reads)
RULE: Core → PAL (platform operations from business logic)
RULE: Adapter → Gateway (state read/write)
RULE: Gateway → PAL (disk/network IO via platform abstraction)
RULE: PAL → Platform APIs (iOS, Android, Windows, Linux — all platform targets are PAL implementations)
RULE: Shared (`_x`) may be imported by any layer
BANNED: Core → Adapter, Core → UI, Core → Gateway (direct)
BANNED: UI → Core (must go through Adapter)
BANNED: PAL → Core, PAL → Adapter, PAL → UI, PAL → Gateway

## Forbidden Cross-Suffix Imports

Derived directly from the DAG — a static scanner enforces these by grepping import lines for suffix co-occurrence:

| File suffix | BANNED from importing |
|-------------|----------------------|
| `_ui` | `_core`, `_pal`, `_gtw` — must route through `_adp` |
| `_core` | `_adp`, `_ui`, `_gtw` — Core is pure; calls only `_pal` |
| `_pal` | `_core`, `_adp`, `_ui`, `_gtw` — PAL is the bottom layer |
| `_gtw` | `_adp`, `_ui` — Gateway calls `_pal`; does not know Adapter or UI |
| `_adp` | *(hub — may reference all layers)* |
| `_x` | *(shared — no import restrictions)* |

BANNED: `_ui` file importing a `_core` type — UI must not know Core exists
BANNED: `_ui` file importing a `_pal` type — UI must not know platform exists
BANNED: `_ui` file importing a `_gtw` type — UI must not know IO exists
BANNED: `_core` file importing a `_adp` type — Core must not know Adapter exists
BANNED: `_core` file importing a `_ui` type — Core must not know UI exists
BANNED: `_core` file importing a `_gtw` type — Core must not know IO exists
BANNED: `_pal` file importing a `_core` type — PAL must not know domain exists
BANNED: `_pal` file importing a `_adp` type — PAL must not know Adapter exists
BANNED: `_pal` file importing a `_ui` type — PAL must not know UI exists
BANNED: `_pal` file importing a `_gtw` type — PAL must not know Gateway exists
BANNED: `_gtw` file importing a `_adp` type — Gateway must not know Adapter exists
BANNED: `_gtw` file importing a `_ui` type — Gateway must not know UI exists

RULE: `_sta` and `_cfg` types follow their host layer's import rules
RULE: A `_core` file importing a `_adp` type is always a placement error — move the logic up
RESULT: `grep "_adp" src/core/` returning hits = architecture violation

## Architecture Diagram

```mermaid
graph TB
    GUI["GUI _ui\nDeclarative views"]
    MCP["MCP _ui\nAI interface"]
    AD["Adapter _adp\nData exchange hub"]
    CORE["Core _core\nBusiness logic"]
    PAL["PAL _pal\nPlatform abstraction"]
    GTW["Gateway _gtw\nIO adapter"]
    SH["Shared _x\nCross-cutting"]
    PLAT["Platform\niOS · Android · Win · Linux"]

    GUI -->|events| AD
    MCP -->|events| AD
    AD -->|computed props| GUI
    AD -->|computed props| MCP
    AD -->|dispatch| CORE
    CORE -->|results| AD
    AD -->|read/write state| GTW
    CORE -->|platform calls| PAL
    GTW -->|IO calls| PAL
    PAL -->|implements| PLAT
    SH -.->|available to all| AD
    SH -.->|available to all| CORE
    SH -.->|available to all| GTW
    SH -.->|available to all| PAL
```

## Placement Rules

RULE: New type → pick folder → apply matching tag → done
RULE: If a type spans two layers, split it or move it to `_x`
RULE: Tests live in `tests/` mirroring `src/` — test types use `_test` tag
BANNED: `utils/`, `helpers/`, `misc/` folders — every file belongs to a layer
BANNED: Adapter logic in Core or PAL

RESULT: Folder structure is self-documenting — grep `_gtw` to find all gateway types
REASON: Placement is architectural enforcement — wrong folder = wrong design
