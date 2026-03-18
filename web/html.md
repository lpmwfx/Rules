---
tags: [web, html, semantic, template, accessibility, aria, web-components]
concepts: [semantic-html, html-templates, accessibility-rules, component-templates]
requires: [global/module-tree.md, web/topology.md]
related: [web/components.md, uiux/file-structure.md, css/modules.md]
keywords: [html, semantic, nav, main, article, section, aside, template, slot, aria, accessibility, keyboard, web-component, div-soup, inline-style, inline-script]
layer: 3
---
# HTML — Semantic Markup and Templates

> HTML is the declarative UI layer for web — parallel to `.slint` files for desktop

---

VITAL: HTML is declarative UI — it describes structure, not behavior
VITAL: One component = one template — same one-module-per-file rule as Slint and JS
RULE: Semantic elements over generic `<div>` — use `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`
RULE: ~200 line limit for HTML templates — AI comprehension boundary (see global/module-tree.md)
RULE: Accessibility is not optional — ARIA roles, labels, and keyboard navigation are required
BANNED: `<div>` soup — nested `<div>` without semantic meaning
BANNED: Inline styles (`style="..."`) — use CSS classes and custom properties
BANNED: Inline scripts (`onclick="..."`) — use event listeners from the Adapter layer
BANNED: `<table>` for layout — tables are for tabular data only

## Semantic Structure

```html
<!-- CORRECT — semantic elements reveal structure -->
<header>
    <nav aria-label="Main navigation">
        <a href="/">Home</a>
        <a href="/settings">Settings</a>
    </nav>
</header>
<main>
    <article>
        <h1>Title</h1>
        <section aria-label="Content">
            <p>Body text</p>
        </section>
        <aside aria-label="Related">
            <p>Sidebar content</p>
        </aside>
    </article>
</main>
<footer>
    <p>Copyright info</p>
</footer>

<!-- WRONG — div soup, no semantics -->
<div class="header">
    <div class="nav">
        <div class="link">Home</div>
    </div>
</div>
<div class="main">
    <div class="content">
        <div class="title">Title</div>
    </div>
</div>
```

RULE: `<nav>` for navigation — not `<div class="nav">`
RULE: `<main>` for primary content — one per page
RULE: `<article>` for self-contained content — blog posts, cards, items
RULE: `<section>` for thematic grouping — with a heading
RULE: `<aside>` for tangentially related content — sidebars, callouts
RULE: `<header>` and `<footer>` for page or section boundaries

## Template and Slot Pattern

`<template>` and `<slot>` are the building blocks for Web Components (see [web/components.md](components.md)):

```html
<!-- Widget template — reusable, encapsulated -->
<template id="card-template">
    <style>
        :host { display: block; }
        .card { border: 1px solid var(--color-border); }
    </style>
    <div class="card">
        <slot name="header"></slot>
        <slot></slot>  <!-- default slot for content -->
        <slot name="footer"></slot>
    </div>
</template>
```

RULE: `<template>` is inert — it defines structure but does not render until cloned
RULE: `<slot>` is the composition point — parent fills named slots with content
RULE: One template per component — matches one-module-per-file rule

## Accessibility Requirements

RULE: All interactive elements must be keyboard-accessible — `tabindex`, `Enter`/`Space` handlers
RULE: All images must have `alt` text — empty `alt=""` for decorative images
RULE: Form inputs must have associated `<label>` elements — use `for`/`id` pairing
RULE: ARIA roles supplement semantics — `role="dialog"`, `role="alert"`, `role="tablist"`
RULE: ARIA labels describe purpose — `aria-label="Search"`, `aria-describedby="help-text"`
RULE: Color must not be the only differentiator — use icons, text, or patterns alongside color
BANNED: Interactive elements without keyboard support
BANNED: Images without `alt` attribute
BANNED: Form inputs without labels
BANNED: Custom widgets without ARIA roles

```html
<!-- CORRECT — accessible dialog -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
    <h2 id="dialog-title">Confirm action</h2>
    <p>Are you sure?</p>
    <button autofocus>Confirm</button>
    <button>Cancel</button>
</div>

<!-- CORRECT — accessible form -->
<label for="email">Email address</label>
<input id="email" type="email" required aria-describedby="email-help">
<span id="email-help">We will never share your email</span>
```

RESULT: Semantic HTML is self-documenting — the element names describe the content
REASON: AI reads HTML literally — semantic elements are unambiguous, `<div>` is not
