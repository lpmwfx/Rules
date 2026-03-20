---
tags: [pal, platform-abstraction, web-api, browser]
concepts: [web-pal, browser-api-abstraction, web-platform-layer]
requires: [pal/design.md, web/topology.md]
related: [web/gateway.md, web/components.md]
keywords: [pal, web-api, localStorage, indexeddb, opfs, fetch, websocket, clipboard, notification, matchMedia, prefers-color-scheme, navigator]
layer: 3
---
# Web PAL

> Web APIs as PAL implementations — one module per concern, stateless

See [pal/design.md](../pal/design.md) for the general PAL pattern. This file covers browser-specific implementations. `pal/design.md` already lists `WebFilePal_pal` as an example — this file defines the full mapping.

---

VITAL: PAL is stateless — it wraps Web APIs, returns results, holds nothing
RULE: One PAL module per concern — `filePal_pal.js`, `appearancePal_pal.js`, `clipboardPal_pal.js`
RULE: PAL modules export functions with a consistent interface — Core and Gateway import only these
RULE: Platform-specific feature detection (`'serviceWorker' in navigator`) lives only in PAL
BANNED: Web API calls outside `src/pal/` and `src/gateway/` — all other layers are platform-agnostic
BANNED: PAL modules holding mutable state — stateless delegate only
BANNED: Business logic in PAL — it executes, not decides

## Web API to PAL Mapping

| PAL concern | Web API implementation | Module |
|---|---|---|
| File / storage | localStorage, IndexedDB, OPFS | `filePal_pal.js` |
| Network | fetch, WebSocket | `networkPal_pal.js` |
| Clipboard | `navigator.clipboard` | `clipboardPal_pal.js` |
| Notifications | Notification API | `notificationPal_pal.js` |
| Appearance | `matchMedia('prefers-color-scheme')` | `appearancePal_pal.js` |
| Fullscreen | Fullscreen API | `windowPal_pal.js` |
| Geolocation | `navigator.geolocation` | `geoPal_pal.js` |

RULE: Not all PAL modules are needed in every project — include only what the app uses
RULE: Adding a new Web API = adding one PAL module — zero changes to Core or Gateway logic

## PAL Module Pattern

```js
// src/pal/appearancePal_pal.js — stateless, wraps matchMedia
/** @returns {'light' | 'dark'} */
export function getColorScheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
}

/** @param {(scheme: 'light' | 'dark') => void} callback */
export function onColorSchemeChange(callback) {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', (e) => callback(e.matches ? 'dark' : 'light'));
}
```

```js
// src/pal/clipboardPal_pal.js — stateless, wraps navigator.clipboard
/** @param {string} text @returns {Promise<{success: boolean, error?: Error}>} */
export async function writeText(text) {
    try {
        await navigator.clipboard.writeText(text);
        return { success: true };
    } catch (e) {
        return { success: false, error: e };
    }
}

/** @returns {Promise<{success: boolean, data?: string, error?: Error}>} */
export async function readText() {
    try {
        const text = await navigator.clipboard.readText();
        return { success: true, data: text };
    } catch (e) {
        return { success: false, error: e };
    }
}
```

RULE: Every PAL function wraps one Web API call — no compound operations
RULE: Feature detection goes in PAL — callers never check `'clipboard' in navigator`
RULE: PAL functions return result objects — never throw

## Feature Detection

```js
// src/pal/filePal_pal.js
export function hasOpfs() {
    return 'getDirectory' in navigator.storage;
}

export function hasIndexedDb() {
    return 'indexedDB' in window;
}
```

RULE: Feature detection is a PAL responsibility — other layers call `hasOpfs()`, never check directly
RESULT: Swapping a Web API for a polyfill = changing one PAL module — nothing else touches platform
REASON: Browser API fragmentation is real — PAL contains it in one place


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
