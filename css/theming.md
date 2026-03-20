---
tags: [theming, dark-mode, prefers-color-scheme, web, pwa]
concepts: [css-dark-mode, prefers-color-scheme, web-theming]
requires: [uiux/theming.md, css/tokens.md]
related: [css/themes.md]
keywords: [prefers-color-scheme, dark, light, matchMedia, css-variables, root, localStorage, theme-toggle]
layer: 4
---
# CSS Dark-Mode Implementation

> `prefers-color-scheme` media query alongside `:root` — system preference is the default

---

```css
/* Always define both — browser picks based on OS */
:root {
    --bg:   #ffffff;
    --text: #1a1a1a;
    --surface: #f5f5f5;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg:   #1a1a1a;
        --text: #f0f0f0;
        --surface: #2a2a2a;
    }
}
```

```js
// Detect and react to changes
const mq = window.matchMedia('(prefers-color-scheme: dark)');
mq.addEventListener('change', e => updateTheme(e.matches ? 'dark' : 'light'));
```

RULE: Define `prefers-color-scheme: dark` media query alongside `:root` — never one without the other
RULE: All color values must be CSS custom properties — never inline hex values
BANNED: `localStorage` theme toggle as the ONLY mechanism — system preference is the default

RESULT: Browser automatically applies the correct theme based on OS preference — zero JS required
REASON: Users who set dark mode in their OS expect every web app to respect it without configuration


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
