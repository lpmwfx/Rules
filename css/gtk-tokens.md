---
tags: [gtk, adwaita, tokens, design-tokens, system-colors]
concepts: [gtk-design-tokens, adwaita-variables]
requires: [uiux/tokens.md, css/tokens.md]
related: [uiux/theming.md, uiux/gtk.md]
keywords: [adwaita, accent-bg-color, card-bg-color, view-fg-color, gtk4, libadwaita, system-token]
layer: 4
---
# GTK/Adwaita Token Implementation

> Map Adwaita system color variables to app-level tokens — never hardcode GTK colors

---

```css
/* tokens/colors.css — uses Adwaita system color variables */
:root {
    --app-accent: var(--accent-bg-color);    /* maps to Adwaita system token */
    --app-surface: var(--card-bg-color);
    --app-text: var(--view-fg-color);
}

/* Component */
.my-button {
    background: var(--app-accent);           /* token */
    color: var(--app-text);                  /* token */
}
```

RULE: Map Adwaita variables (`--accent-bg-color`, `--card-bg-color`) to app-level tokens in `:root`
RULE: Components reference app tokens, never Adwaita variables directly — allows non-GTK fallbacks

RESULT: GTK apps inherit system theme automatically while maintaining app-level token consistency
REASON: Direct Adwaita variable usage scatters platform dependency through every component
