---
tags: [responsive, layout, mother-child, breakpoints, preferred-width, stretch, sizing]
concepts: [responsive-layout, constraint-layout, breakpoints, mother-child-pattern, stretch-factors]
requires: [slint/component-model.md, uiux/mother-child.md]
related: [slint/globals.md, uiux/tokens.md, uiux/file-structure.md]
keywords: [preferred-width, horizontal-stretch, vertical-stretch, breakpoints, root.width, min-width, percent, if, layout, responsive, resize, window, size, hardcoded, px, AppWindow]
layer: 3
---
# Slint Responsive Layout

> AppWindow is mother — it owns all dimensions and breakpoints; child components declare constraints only

---

VITAL: Child components never hardcode their own outer width or height — they declare constraints and stretch factors
VITAL: `AppWindow` is the only component that reads `root.width` for breakpoints
VITAL: Use `preferred-width` / `preferred-height` on `Window` — never `width` / `height` (locks the window)
RULE: Modules set `preferred-width: 100%` and `preferred-height: 100%` to fill whatever slot mother provides
RULE: Use `horizontal-stretch` / `vertical-stretch` to distribute space — not pixel arithmetic
RULE: Breakpoint `if` conditions live in `AppWindow` only — never deep in sub-components
RULE: `min-width` / `min-height` are acceptable in child components — they express constraints, not absolute size
BANNED: `width: 400px` on a child component's outer bounds — that measurement belongs to mother
BANNED: `width: parent.width - 200px` inside a module — use stretch factors instead
BANNED: `width: <fixed>` on `Window` — use `preferred-width` to allow resize
BANNED: Breakpoint `if root.width` inside a `component ... inherits Rectangle` with layout inside — compiler bug (issue #7126)

## Why this is the mother–child pattern in Slint

Slint is constraint-based, not CSS-based. There is no flexbox or media queries — instead every binding is a reactive expression evaluated top-down. This makes the mother–child pattern a natural fit:

- `AppWindow` (mother) knows `root.width` and dispatches layout structure
- Modules (children) declare only `preferred-width: 100%` and `horizontal-stretch` — they fill their slot
- Changing a module never touches layout logic — that lives only in `AppWindow`
- Adding a new breakpoint requires editing exactly one file: `AppWindow`

## Preferred-width on modules

```slint
// modules/NavBar.slint — CHILD: no outer size, fills slot
export component NavBar {
    preferred-width: 100%;
    min-height: 48px;
    // Internal layout only — padding, spacing, icon sizes
    HorizontalLayout {
        padding: Spacing.md;
        spacing: Spacing.sm;
        // nav items...
    }
}

// modules/ContentArea.slint — CHILD: fills remaining space
export component ContentArea {
    preferred-width: 100%;
    preferred-height: 100%;
    // Internal layout only
}
```

## Stretch factors instead of pixel arithmetic

```slint
// GOOD — stretch distributes space, no px arithmetic
HorizontalLayout {
    sidebar := Rectangle {
        min-width: 180px;
        horizontal-stretch: 0;   // does not grow beyond min-width
    }
    content := Rectangle {
        horizontal-stretch: 1;   // takes all remaining space
    }
}

// BANNED — pixel arithmetic in layout
HorizontalLayout {
    sidebar := Rectangle { width: 200px; }
    content := Rectangle { width: parent.width - 200px; }  // BANNED
}
```

## Percentage shorthand

```slint
// These three are equivalent — prefer the % shorthand
width: parent.width * 0.5;
width: parent.width / 2;
width: 50%;   // preferred
```

## Breakpoints in AppWindow only

```slint
// AppWindow.slint — MOTHER: owns root.width, dispatches layout
import { NavBar }      from "modules/nav-bar.slint";
import { ContentArea } from "modules/content-area.slint";

export component AppWindow inherits Window {
    preferred-width: 1024px;   // start size — freely resizable
    preferred-height: 768px;

    // Mobile layout
    if root.width < 640px: VerticalLayout {
        NavBar { }
        ContentArea { vertical-stretch: 1; }
    }

    // Desktop layout
    if root.width >= 640px: HorizontalLayout {
        NavBar {
            min-width: 220px;
            horizontal-stretch: 0;
        }
        ContentArea {
            horizontal-stretch: 1;
        }
    }
}
```

RULE: `if root.width` breakpoints are safe at `AppWindow` level and inside plain `Rectangle` wrappers
RULE: Wrap layout in a `Rectangle` if you need a named element with breakpoints inside

```slint
// Safe pattern — Rectangle wrapper avoids compiler issue with component-level if
export component AppWindow inherits Window {
    preferred-width: 1024px;
    preferred-height: 768px;

    Rectangle {
        if root.width < 640px: VerticalLayout { /* ... */ }
        if root.width >= 640px: HorizontalLayout { /* ... */ }
    }
}
```

## Window sizing

```slint
// GOOD — preferred-width allows window manager to resize freely
export component AppWindow inherits Window {
    preferred-width: 1024px;
    preferred-height: 768px;
}

// BANNED — locks window to fixed size, prevents resize
export component AppWindow inherits Window {
    width: 1024px;    // BANNED
    height: 768px;    // BANNED
}
```

## Canonical module layout

```
ui/
  app-window.slint        ← MOTHER: breakpoints, root.width, layout dispatch
  modules/
    nav-bar.slint         ← preferred-width: 100%, no outer px
    content-area.slint    ← preferred-width/height: 100%
    editor-panel.slint    ← preferred-width: 100%
    item-list.slint       ← preferred-width: 100%
```

RULE: Module folder structure mirrors `uiux/file-structure.md` — one component per file
RULE: `app-window.slint` is the single entry point compiled by `build.rs`

## Summary — what to hardcode and what not to

| Do this | Not this |
|---------|----------|
| `preferred-width: 100%` on modules | `width: 400px` on modules |
| `horizontal-stretch: 1` | `width: parent.width - 200px` |
| `min-width: 180px` | `width: 180px` (locks to fixed) |
| Breakpoints in `AppWindow` | `if root.width` deep in sub-components |
| `preferred-width: 1024px` on Window | `width: 1024px` on Window |

RESULT: Modules declare constraints — `AppWindow` owns all topology and breakpoints
REASON: Single ownership of layout means changing any child is safe; all breakpoint logic is in one file
