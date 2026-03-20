---
tags: [wa, pwa, browser, platform]
concepts: [web-overview, web-platform, browser-apps]
feeds: [web/topology.md, web/gateway.md, web/pal.md, web/pwa.md, web/html.md, web/components.md, web/mother-child.md]
related: [global/consistency.md, global/app-model.md, uiux/about-web.md]
keywords: [browser, wa, pwa, react, solidjs, svelte, vanilla, esm, declarative, tokens, css-custom-properties]
layer: 6
---
# Web

> Platform rules for browser-based apps — WA and PWA project types

---

VITAL: Web is the platform category for browser apps — parallel to `slint/` for desktop
RULE: All web rules apply to WA (Web App) and PWA (Progressive Web App) project types
RULE: Framework-agnostic — React, SolidJS, Svelte, and vanilla JS all follow the same topology
RULE: ESM only — `"type": "module"` in package.json, `import`/`export` everywhere

## Topic files

| File | What it defines |
|------|-----------------|
| [topology.md](topology.md) | 6-layer folder mapping for browser projects |
| [gateway.md](gateway.md) | Gateway layer: fetch, localStorage, IndexedDB, Cache API |
| [pal.md](pal.md) | Web APIs as PAL implementations |
| [pwa.md](pwa.md) | PWA-specific: service worker, manifest, offline-first |
| [html.md](html.md) | Semantic HTML, template rules, accessibility |
| [components.md](components.md) | Web Components as mother-child enforcement |
| [mother-child.md](mother-child.md) | Mother-child pattern for web: Shell, Views, Widgets |

## Five invariants

1. **ESM only** — no CommonJS, no script tags without `type="module"`
2. **Declarative UI** — components render state, never mutate DOM imperatively
3. **Tokens via CSS custom properties** — `var(--color-primary)`, never raw values in components
4. **No imperative DOM** — no `getElementById`, no `innerHTML`, no `querySelector` for state
5. **Topology compliance** — same 6-layer DAG as all other project types

## Relationship to js/

`js/` defines language-level rules (ESM, JSDoc, testing, validation).
`web/` defines platform-level rules (browser APIs, HTML, Web Components, PWA).
A web project uses both: `js/` for how you write JavaScript, `web/` for how you structure a browser app.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
