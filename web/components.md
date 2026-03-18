---
tags: [web, web-components, custom-elements, shadow-dom, encapsulation, mother-child]
concepts: [web-components, custom-elements-pattern, shadow-dom-encapsulation, slint-web-parallel]
requires: [uiux/mother-child.md, web/html.md, global/mother-tree.md]
related: [web/mother-child.md, slint/component-model.md, global/data-driven-ui.md, css/modules.md]
keywords: [web-component, custom-element, shadow-dom, slot, attributeChangedCallback, CustomEvent, observed-attribute, property, encapsulation, mother-child]
layer: 3
---
# Web Components

> Custom Elements as mother-child enforcement — attributes in, events up, Shadow DOM encapsulates

Web Components are the browser-native mechanism for component encapsulation. They enforce the same mother-child pattern as Slint's property direction system.

---

VITAL: Shadow DOM = encapsulation boundary = file boundary — styles and DOM do not leak
VITAL: Observed attributes = data in (like Slint `in property`)
VITAL: CustomEvent dispatch = signal up (like Slint `callback`)
RULE: One Custom Element per file — matches one-module-per-file rule
RULE: Element name must contain a hyphen — `<app-shell>`, `<nav-bar>`, `<user-card>`
RULE: Children are stateless — they receive attributes, emit events, own nothing
BANNED: Children querying parent DOM — parent passes data via attributes
BANNED: Children dispatching to siblings — events bubble up to parent
BANNED: Shared mutable state between components — all state routes through mother

## Slint ↔ Web Component Parallel

| Slint concept | Web Component equivalent |
|---|---|
| `in property` | Observed attribute / property setter |
| `callback` | `CustomEvent` dispatched up (`bubbles: true`) |
| `in-out property` | N/A — use attribute + event pair instead |
| Mother `inherits Window` | `<app-shell>` root element |
| `export component` | `customElements.define()` |
| Slint globals | CSS custom properties on `:root` |

## Custom Element Pattern

```js
// src/ui/widgets/navBar.js — CHILD (stateless widget)
const template = document.createElement('template');
template.innerHTML = `
    <style>
        :host { display: flex; }
        nav { width: 100%; }
        .active { font-weight: bold; }
    </style>
    <nav>
        <slot></slot>
    </nav>
`;

class NavBar extends HTMLElement {
    static observedAttributes = ['active-view'];

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    attributeChangedCallback(name, oldVal, newVal) {
        if (name === 'active-view') this.#updateActive(newVal);
    }

    #updateActive(view) {
        // update internal rendering based on attribute
    }

    // Event UP — notify parent of navigation request
    #handleClick(viewId) {
        this.dispatchEvent(new CustomEvent('navigate', {
            detail: { viewId },
            bubbles: true,
            composed: true,
        }));
    }
}

customElements.define('nav-bar', NavBar);
```

RULE: `observedAttributes` declares the component's input interface — like Slint `in property`
RULE: `dispatchEvent(new CustomEvent(...))` is the output interface — like Slint `callback`
RULE: `bubbles: true, composed: true` — events cross Shadow DOM boundaries to reach parent
RULE: `attributeChangedCallback` handles state changes — no polling, no manual DOM observation

## Shadow DOM as Encapsulation

```
<app-shell>                          ← mother (owns state)
  #shadow-root
    <nav-bar active-view="home">     ← child (stateless)
      #shadow-root
        <nav>...</nav>               ← encapsulated — styles don't leak
    </nav-bar>
    <main>
      <home-view>                    ← child (stateless)
        #shadow-root
          <section>...</section>     ← encapsulated
      </home-view>
    </main>
</app-shell>
```

RULE: Shadow DOM prevents style leakage — each component owns its own styles
RULE: Shadow DOM prevents DOM leakage — `querySelector` does not cross shadow boundaries
RULE: `<slot>` is the composition point — parent projects content into child slots

## Framework-Agnostic Applicability

These principles apply regardless of whether you use vanilla Web Components, React, Solid, or Svelte:

| Principle | Web Components | React | Svelte |
|---|---|---|---|
| Data in | observed attributes | props | props |
| Signal up | CustomEvent | callback props | `dispatch()` |
| Encapsulation | Shadow DOM | module scope | scoped styles |
| Composition | `<slot>` | `children` / `slots` | `<slot>` |

RULE: The enforcement mechanism varies by framework — the mother-child pattern is identical
RESULT: Components are independently testable — set attributes, assert events
REASON: Web Components enforce encapsulation at the platform level — no framework required
