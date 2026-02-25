---
tags: [css, separation, concerns, architecture]
concepts: [architecture, concerns]
related: [css/cascade.md, css/modules.md]
layer: 4
---
# Separation of Concerns

> Layout separate from colors — zero overlap

---

RULE: Separation of concerns — layout separate from colors
RULE: CSS Custom Properties for all colors and shadows
RULE: Theme switching via `data-theme` attribute
RULE: Mobile-first responsive design
RULE: No CSS frameworks — vanilla CSS only

## File Structure

```
css/
├── site.css         # Layout, typography, spacing (NO colors)
├── nav.css          # Navigation layout (NO colors)
├── light-theme.css  # Light mode colors only
└── dark-theme.css   # Dark mode overrides only
```

RULE: Layout files contain ZERO color values
RULE: Theme files contain ONLY color values and color-dependent styles
RULE: Each file has a header comment explaining its purpose
