---
tags: [uiux, about, web, pwa, shortcuts-overlay]
concepts: [about-web, web-shortcuts-overlay]
requires: [uiux/help-about.md]
related: [js/modules.md, web/README.md]
keywords: [modal, about-route, shortcuts-overlay, keydown, PWA, web]
layer: 4
---
# About and Shortcuts — Web / PWA

> Modal dialog or `/about` route, shortcuts overlay via `?` key

---

**About:** Modal dialog or `/about` route.

**Shortcuts:** Overlay triggered by `?` key — show app-specific shortcuts only.

```js
document.addEventListener('keydown', e => {
    if (e.key === '?' && !e.ctrlKey && !e.metaKey) showShortcutsOverlay()
})
```

RULE: `?` key opens shortcuts overlay — do not require Ctrl/Cmd modifier on web
RULE: About page must contain: app name, version, author, license, source link

RESULT: Web users discover shortcuts with a single keypress — same as desktop Ctrl+?
REASON: Web apps without discoverable shortcuts lose power users to competitors
