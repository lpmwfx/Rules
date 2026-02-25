---
tags: [css, quick-ref, reference, summary]
concepts: [reference, summary]
related: [css/cascade.md, css/modules.md, css/naming.md, css/custom-properties.md, css/themes.md]
layer: 6
---
# CSS Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Philosophy | Vanilla CSS, no frameworks |
| Separation | Layout files: ZERO colors. Theme files: ONLY colors |
| Cascade | Each file ADDS, none OVERWRITES — separate domains |
| Modules | One file per component, self-contained |
| Tokens | `--color-bg-1/2/3`, `--color-text-1/2/3`, `--shadow-1/2/3` |
| Themes | Light on `:root`, dark on `[data-theme="dark"]` |
| Naming | BEM-inspired: `.block-element--modifier` |
| Responsive | Mobile-first, single breakpoint: 768px, `min-width` |
| Typography | System fonts, `rem` units, unitless line-height |
| Layout | Flexbox for 1D, Grid for 2D |
| BANNED | `!important`, ID selectors, deep nesting, Tailwind/Bootstrap |
