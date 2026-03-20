---
tags: [pwa, service-worker, manifest, offline-first, cache-api]
concepts: [pwa-architecture, service-worker-pattern, offline-first-data]
requires: [web/topology.md, web/gateway.md]
related: [web/pal.md, global/app-model.md]
keywords: [pwa, service-worker, manifest, cache-api, offline, install-prompt, beforeinstallprompt, workbox, indexeddb, progressive-web-app]
layer: 4
---
# PWA — Progressive Web App

> Service worker as Gateway extension, offline-first data flow, installability

Only relevant for PWA project type. WA projects skip this entirely.

---

VITAL: A PWA is a WA with three additions: service worker, manifest, offline data strategy
RULE: Service worker manages the Cache API — it is a Gateway extension, not a separate layer
RULE: `manifest.json` is required — without it the browser cannot install the app
RULE: Offline-first means Gateway tries cache before network, not the other way around

## Service Worker as Gateway Extension

The service worker intercepts `fetch()` requests and applies a caching strategy.
It is part of the Gateway layer — it controls IO, not business logic.

```
Browser tab                         Service Worker
────────────                        ──────────────
UI → Adapter → Gateway.fetch()  ──► sw intercepts
                                    ├── cache hit? → return cached response
                                    └── cache miss? → fetch from network
                                        ├── success → cache + return
                                        └── failure → return offline fallback
```

RULE: Service worker lives in project root (`sw.js`) — not inside `src/`
RULE: Service worker only caches — no business logic, no state mutation
BANNED: Business logic in service worker — it is a cache layer only
BANNED: Service worker importing from `src/core/` — it is Gateway, not Core

## Cache Strategies

| Strategy | When | Pattern |
|----------|------|---------|
| Cache-first | Static assets (CSS, JS, images) | Try cache → fallback to network |
| Network-first | API data | Try network → fallback to cache |
| Stale-while-revalidate | Semi-static content | Return cache, update in background |

RULE: Static assets use cache-first — they change only on deploy
RULE: API responses use network-first — freshness matters
RULE: Choose one strategy per route pattern — no mixed strategies per route

## manifest.json

```json
{
    "name": "App Name",
    "short_name": "App",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
        { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
    ]
}
```

RULE: `display: "standalone"` — PWA should look like a native app
RULE: At least two icon sizes: 192x192 and 512x512
RULE: `start_url` matches the app's entry point

## Offline Data Flow

```
Online:   Gateway.fetch(url) → network response → cache response → return data
Offline:  Gateway.fetch(url) → network fail → cache hit → return cached data
          Gateway.fetch(url) → network fail → cache miss → return offline fallback

Mutations while offline:
  Gateway.saveOffline(action) → IndexedDB queue
  Online again → Gateway.syncQueue() → replay actions → clear queue
```

RULE: Read operations use cached data when offline — user sees last known state
RULE: Write operations queue in IndexedDB — synced when connection returns
RULE: Sync queue replay must be idempotent — retries are safe

## Install Prompt

```js
// src/pal/installPal_pal.js — PAL wraps the install prompt
let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
});

export async function promptInstall() {
    if (!deferredPrompt) return { success: false, error: 'no-prompt' };
    deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    deferredPrompt = null;
    return { success: true, data: result.outcome };
}
```

RULE: Install prompt handling lives in PAL — Adapter decides when to show it
RULE: Never auto-prompt — let the user trigger install from a UI button

RESULT: A PWA is a WA with a cache layer — the topology is identical, only Gateway gains offline capability
REASON: Keeping service worker as Gateway extension prevents a parallel architecture from forming


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
