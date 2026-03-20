---
tags: [mother-child, composition, stateless, shell, views, widgets]
concepts: [web-mother-child, shell-views-widgets, web-state-ownership]
requires: [uiux/mother-child.md, web/topology.md, global/mother-tree.md]
feeds: [uiux/mother-child-react.md]
related: [web/components.md, web/html.md]
keywords: [mother, child, shell, view, widget, stateless, state-owner, AppShell, web-component, vanilla, react, solid, svelte, layout, css-custom-properties]
layer: 3
---
# Web Mother-Child

> Shell → Views → Widgets — same 3-tier hierarchy as Slint, enforced in the browser

See [uiux/mother-child.md](../uiux/mother-child.md) for the general pattern and [slint/mother-child.md](../slint/mother-child.md) for the Slint-specific implementation. This file covers web-specific enforcement.

---

VITAL: Every web app has exactly one mother — the `<app-shell>` root component
VITAL: Views are stateless screens — they render what mother gives them
VITAL: Widgets are stateless, reusable components — importable by mother and any view
RULE: State ownership lives in Shell (mother) — views and widgets never own app state
RULE: Layout ownership lives in Shell — CSS custom properties control dimensions
RULE: Views are imported only by Shell — never by another view
RULE: Widgets are imported by Shell, views, or other widgets — shared component library
BANNED: Views importing sibling views — route shared composition through Shell or extract to widgets
BANNED: Widgets importing views — widgets are lower in the hierarchy
BANNED: Children querying global state, stores, or context — mother passes everything down

## Three-Tier Hierarchy

```
Shell (app-shell.js — root, owns ALL state)
├── imports Views      ← screens, view-specific, stateless
└── imports Widgets    ← generic, reusable, stateless

Views (src/ui/views/)
├── HomeView           ← stateless, receives props from Shell
├── SettingsView       ← stateless, receives props from Shell
└── imports Widgets    ← OK — views compose from the widget library

Widgets (src/ui/widgets/)
├── NavBar, Card, SearchBar  ← generic, stateless
├── imports other Widgets    ← OK — widgets compose other widgets
└── importable by Shell, Views, Widgets
```

| Tier | Folder | State | Importable by |
|------|--------|-------|---------------|
| **Shell** | `src/ui/shell.js` | Owns all (`let state = {...}`) | — top level |
| **View** | `src/ui/views/` | Stateless (receives props) | Shell only |
| **Widget** | `src/ui/widgets/` | Stateless (receives props) | Shell, Views, Widgets |

## Vanilla JS Implementation

```js
// src/ui/shell.js — MOTHER (owns state, controls layout)
import './views/homeView.js';
import './views/settingsView.js';
import './widgets/navBar.js';

class AppShell extends HTMLElement {
    // State ownership — only Shell owns app state
    #state = {
        activeView: 'home',
        sidebarOpen: true,
        selectedItem: null,
        items: [],
    };

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.#render();
        this.#bindEvents();
    }

    #render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: grid;
                    grid-template-columns: var(--sidebar-width, 240px) 1fr;
                    height: 100vh;
                }
            </style>
            <nav-bar active-view="${this.#state.activeView}"></nav-bar>
            <main>
                <home-view ${this.#state.activeView === 'home' ? '' : 'hidden'}></home-view>
                <settings-view ${this.#state.activeView === 'settings' ? '' : 'hidden'}></settings-view>
            </main>
        `;
    }

    #bindEvents() {
        // Events UP from children — Shell decides what happens
        this.shadowRoot.addEventListener('navigate', (e) => {
            this.#state.activeView = e.detail.viewId;
            this.#render();
        });

        this.shadowRoot.addEventListener('item-selected', (e) => {
            this.#state.selectedItem = e.detail.item;
            this.#updateViews();
        });
    }

    #updateViews() {
        const homeView = this.shadowRoot.querySelector('home-view');
        if (homeView) homeView.setAttribute('selected', this.#state.selectedItem?.id ?? '');
    }
}

customElements.define('app-shell', AppShell);
```

```js
// src/ui/views/homeView.js — CHILD (stateless view)
class HomeView extends HTMLElement {
    static observedAttributes = ['selected'];

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    attributeChangedCallback(name, oldVal, newVal) {
        if (name === 'selected') this.#highlightItem(newVal);
    }

    // Event UP — notify Shell of user action
    #onItemClick(item) {
        this.dispatchEvent(new CustomEvent('item-selected', {
            detail: { item },
            bubbles: true,
            composed: true,
        }));
    }
}

customElements.define('home-view', HomeView);
```

## Layout Ownership via CSS Custom Properties

Shell controls all layout dimensions through CSS custom properties — the web equivalent of Slint's mother-owned sizes:

```js
// Shell sets layout tokens — children use them
this.style.setProperty('--sidebar-width', '240px');
this.style.setProperty('--header-height', '48px');
this.style.setProperty('--content-padding', '16px');
```

```css
/* Child widget — uses Shell's tokens, never sets its own outer dimensions */
:host {
    width: 100%;               /* fills slot provided by Shell */
    padding: var(--content-padding);  /* reads Shell's token */
}
```

RULE: Shell sets CSS custom properties — children read them via `var(--token)`
RULE: Children use `width: 100%` or `flex: 1` — they fill their slot
BANNED: Children setting their own `width`, `height`, or `position: fixed/absolute`

## Framework Applicability

This pattern is framework-agnostic. The enforcement mechanism differs:

| Framework | Mother | Data down | Events up |
|---|---|---|---|
| Vanilla | `<app-shell>` Custom Element | attributes | `CustomEvent` |
| React | `<AppShell>` component | props | callback props |
| SolidJS | `<AppShell>` component | props / signals | callback props |
| Svelte | `<AppShell>` component | props | `dispatch()` |

See [uiux/mother-child-react.md](../uiux/mother-child-react.md) for the React-specific implementation.

RESULT: Any view can be understood by reading one file — it receives props, emits events, done
REASON: Mother-child in the browser is the same pattern as desktop — only the API surface differs


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
