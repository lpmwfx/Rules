---
tags: [web, gateway, fetch, localstorage, indexeddb, cache-api, io]
concepts: [web-gateway, browser-io, fetch-pattern, storage-pattern]
requires: [web/topology.md, global/adapter-layer.md]
related: [gateway/io.md, web/pwa.md, web/pal.md]
keywords: [gateway, fetch, localStorage, sessionStorage, indexeddb, cache-api, io, DOMContentLoaded, beforeunload, boot, lifecycle]
layer: 3
---
# Web Gateway

> Gateway in the browser — fetch, localStorage, IndexedDB, Cache API

See [gateway/io.md](../gateway/io.md) for the general Gateway pattern. This file covers browser-specific IO primitives.

---

VITAL: Gateway is the ONLY layer that calls `fetch()`, reads `localStorage`, or opens IndexedDB
VITAL: All IO returns a result — Gateway never throws on network or storage failure
RULE: Gateway delegates to PAL for platform-specific API access (see [web/pal.md](pal.md))
RULE: One Gateway module per IO concern — `apiGateway_gtw.js`, `storageGateway_gtw.js`
BANNED: `fetch()` outside `src/gateway/`
BANNED: `localStorage.getItem()` outside `src/gateway/`
BANNED: `indexedDB.open()` outside `src/gateway/`
BANNED: Gateway containing business logic — IO marshalling only

## Browser IO Primitives

| Primitive | Use case | Sync/Async |
|-----------|----------|------------|
| `fetch()` | Network requests — API calls, resource loading | Async |
| `localStorage` | Small key-value state (<5 MB) — settings, tokens | Sync |
| `sessionStorage` | Tab-scoped state — form drafts, temp data | Sync |
| `IndexedDB` | Structured data — offline cache, large datasets | Async |
| `Cache API` | HTTP response cache — PWA offline (see [web/pwa.md](pwa.md)) | Async |

RULE: `localStorage` for small, simple state — config, preferences, auth tokens
RULE: `IndexedDB` for structured or large data — use via PAL wrapper, not raw API
RULE: `Cache API` only in PWA projects — managed by service worker

## Gateway Pattern

```js
// src/gateway/storageGateway_gtw.js
import { AppError } from '../shared/errors_x.js';

/** @returns {{ success: boolean, data?: AppConfig, error?: AppError }} */
export function loadConfig() {
    try {
        const raw = localStorage.getItem('app-config');
        if (!raw) return { success: true, data: defaultConfig() };
        return { success: true, data: JSON.parse(raw) };
    } catch (e) {
        return { success: false, error: AppError.storage('config-load', e) };
    }
}

export function saveConfig(config) {
    try {
        localStorage.setItem('app-config', JSON.stringify(config));
        return { success: true };
    } catch (e) {
        return { success: false, error: AppError.storage('config-save', e) };
    }
}
```

```js
// src/gateway/apiGateway_gtw.js
export async function fetchItems(endpoint) {
    try {
        const res = await fetch(endpoint);
        if (!res.ok) return { success: false, error: AppError.network(res.status) };
        const data = await res.json();
        return { success: true, data };
    } catch (e) {
        return { success: false, error: AppError.network(0, e) };
    }
}
```

RULE: Every Gateway function returns a result object — never throws
RULE: Error types are `AppError_x` — shared across all Gateways

## Gateway Lifecycle

```
DOMContentLoaded
├── storageGateway.loadConfig()    → AppConfig_cfg
├── storageGateway.loadState()     → AdapterState_sta
└── hand off to Adapter.init()

beforeunload
├── storageGateway.saveState(adapterState)
└── storageGateway.saveConfig(config)
```

RULE: Load state on `DOMContentLoaded` — Gateway is the first thing that runs
RULE: Save state on `beforeunload` — persist current session
RULE: Boot order: Gateway → Core → Adapter → UI mount

RESULT: All IO is in one place — `grep "_gtw" src/` finds every IO operation
REASON: Browser IO is fragmented (fetch, localStorage, IndexedDB) — Gateway centralizes it
