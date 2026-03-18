---
tags: [topology, architecture, hexagonal, layers, dag, folder-structure, wa, pwa]
concepts: [web-topology, browser-layer-mapping, esm-import-dag]
requires: [global/topology.md, global/app-model.md]
feeds: [web/gateway.md, web/pal.md, js/project-structure.md]
related: [web/README.md, web/mother-child.md]
keywords: [topology, layers, folder, src, ui, adapter, core, gateway, pal, shared, esm, import, dag, wa, pwa, service-worker, manifest]
layer: 2
---
# Web Topology

> 6-layer hexagonal MVVM mapped to browser folder structure

See [global/topology.md](../global/topology.md) for the canonical topology. This file covers browser-specific folder mapping and ESM import enforcement.

---

VITAL: Browser projects follow the same 6-layer DAG — no exceptions
VITAL: ESM import paths enforce the layer DAG — a `_ui` file importing from `core/` is a build-time visible violation
RULE: Suffix tags apply identically in JS: `feedAdapter_adp.js`, `feedCore_core.js`
RULE: Import direction is one-way — enforced by ESM static imports

## Folder Layout

```
src/
├── ui/           ← views, components, Web Components (_ui)
│   ├── views/    ← screen-level components (stateless)
│   ├── widgets/  ← reusable components (stateless)
│   └── shell.js  ← mother component (AppShell)
├── adapter/      ← ViewModel, event routing, state store (_adp)
├── core/         ← pure business logic (_core)
├── gateway/      ← fetch, localStorage, IndexedDB (_gtw)
├── pal/          ← Web API abstractions (_pal)
└── shared/       ← errors, result types (_x)
```

RULE: `src/ui/` = declarative components — no business logic, no IO
RULE: `src/adapter/` = the hub — only layer that imports from all others
RULE: `src/core/` = pure functions — no DOM, no fetch, no browser APIs
RULE: `src/gateway/` = all IO — fetch, localStorage, IndexedDB, Cache API
RULE: `src/pal/` = Web API wrappers — clipboard, notifications, matchMedia
RULE: `src/shared/` = cross-cutting — error types, result wrappers, constants
BANNED: `utils/`, `helpers/`, `lib/` — every file belongs to a layer

## ESM Import Rules

```js
// src/ui/views/HomeView.js — _ui file
import { homeState } from '../adapter/homeAdapter_adp.js';  // OK — UI reads Adapter
// import { validate } from '../../core/rules_core.js';     // BANNED — UI → Core

// src/core/rules_core.js — _core file
import { AppError } from '../shared/errors_x.js';           // OK — Core reads Shared
// import { fetchData } from '../gateway/api_gtw.js';       // BANNED — Core → Gateway
// import { HomeView } from '../ui/views/HomeView.js';      // BANNED — Core → UI

// src/adapter/homeAdapter_adp.js — _adp file (hub)
import { validate } from '../core/rules_core.js';           // OK — Adapter → Core
import { fetchItems } from '../gateway/api_gtw.js';         // OK — Adapter → Gateway
import { AppError } from '../shared/errors_x.js';           // OK — Adapter → Shared
```

RULE: A linter rule or `madge` circular-dependency check enforces these boundaries
RULE: `grep -r "from.*core/" src/ui/` returning hits = architecture violation

## Project Type Differences

| Concern | WA (Web App) | PWA (Progressive Web App) |
|---------|-------------|--------------------------|
| Service worker | None | Required — offline cache strategy |
| Manifest | Optional | Required — `manifest.json` |
| Install prompt | N/A | `beforeinstallprompt` handling |
| Cache API | Optional | Core — offline-first data flow |
| Gateway scope | fetch + localStorage | fetch + localStorage + IndexedDB + Cache API |
| PAL scope | Basic Web APIs | Basic + service worker registration |

RULE: WA is the simpler subset — no service worker, no manifest requirement
RULE: PWA extends WA with offline capability — see [web/pwa.md](pwa.md)

## Boot Order

```
1. Gateway.init()     → load config + state from localStorage/IndexedDB
2. Core.init(config)  → initialize business logic with loaded config
3. Adapter.init()     → set up event routing, create initial ViewModel
4. UI.mount()         → render shell component, bind to Adapter state
```

RULE: Gateway initializes first — all other layers receive config from it
RULE: UI mounts last — it renders what Adapter provides, nothing more
RULE: Same boot order as desktop/mobile — only the IO primitives differ

RESULT: A web project's folder structure reveals its architecture — `ls src/` shows all six layers
REASON: ESM static imports make the dependency DAG visible and enforceable at lint time
