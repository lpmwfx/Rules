---
tags: [css, cascade, specificity, layers]
concepts: [css-architecture, separation]
requires: [global/consistency.md]
feeds: [css/themes.md]
related: [css/separation.md]
keywords: [cascade-layers, specificity, at-layer]
layer: 4
---
# Cascade by Design

> Many files with separate domains — zero conflicts

---

PRINCIPLE: Many files with SEPARATE domains beats few files with MIXED domains
PRINCIPLE: Cascade is COLLABORATION not competition
PRINCIPLE: Each file ADDS, none OVERWRITES

## Domain Separation

```
reset.css       → box model, margins    (NEVER colors, fonts, widths)
typography.css  → fonts, line-height    (NEVER colors, layout)
site.css        → structure, widths     (NEVER colors, fonts)
theme.css       → colors, shadows       (NEVER layout, fonts)
nav.css         → only .nav-* classes   (NEVER other components)
```

## Why No Cascade Conflicts

- No file competes for same property
- No file overwrites another file's domain
- Import order is predictable and intentional
- Each file has ONE responsibility

## Traditional CSS Problem

```
styles.css → everything mixed
fixes.css  → overwrites styles.css
shame.css  → !important everywhere
= Cascade is a BATTLE
```

## This Architecture

```
Each file owns its domain exclusively
Files add layers, never fight
= Cascade is a FEATURE
```

RESULT: More CSS files = SIMPLER maintenance, not harder
REASON: AI changes colors? Only touch theme.css. Layout? Only site.css.
