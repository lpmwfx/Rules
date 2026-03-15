---
tags: [slint, mother-child, property-direction, viewmodel, in-property, callback, in-out-property, structs]
concepts: [mother-child-pattern, property-direction, viewmodel-structs, stateless-children]
requires: [uiux/mother-child.md, slint/globals.md]
feeds: []
related: [slint/component-model.md, slint/responsive-layout.md, uiux/state-flow.md]
keywords: [mother, child, in property, in-out property, callback, AppWindow, inherits Window, struct, types.slint, overlay, viewmodel, state-owner, stateless]
layer: 3
---
# Slint Mother–Child

> Property direction is the enforcement mechanism — `in` receives, `callback` emits, `in-out` is state ownership

See [uiux/mother-child.md](../uiux/mother-child.md) for the general pattern. This file covers Slint-specific enforcement.

---

## Three-Tier Component Hierarchy

VITAL: The Slint UI has exactly three component tiers — Mother, View, Widget
VITAL: Before creating a new child component, check `widgets/` for an existing generic component that covers it
RULE: Generic component (only `in property` + `callback`, no view-specific logic) → `widgets/` not `views/`
RULE: Views may only be imported by Mother — never by another View or Widget
RULE: Widgets may be imported by Mother, Views, or other Widgets — they are the shared component library
BANNED: A View importing another View — route shared composition through Mother or extract to `widgets/`
BANNED: A Widget importing a View — Widgets are lower in the hierarchy and must never depend upward

```
Mother (app-window.slint — inherits Window)
├── imports Views     ← screens, view-specific, stateless
└── imports Widgets   ← generic, reusable, stateless

Views (ui/views/*.slint)
├── imports Widgets   ← OK — views compose from the widget library
└── ONLY importable by Mother — never by another View

Widgets (ui/widgets/*.slint or ui/components/*.slint)
├── imports Widgets   ← OK — widgets may compose other widgets
├── importable by Mother, Views, or Widgets
├── MUST be stateless — in property + callback only, no in-out property
└── MUST be zero-literal — all values via tokens
```

| Tier | Folder | State | Importable by |
|------|--------|-------|---------------|
| **Mother** | `app-window.slint` | Owns all (`in-out property`) | — top level |
| **View** | `ui/views/` | Stateless (`in` + `callback`) | Mother only |
| **Widget** | `ui/widgets/` | Stateless (`in` + `callback`) | Mother, Views, Widgets |

Decision flow for every new component:
1. Does `widgets/` already have something that covers this? → use it as-is
2. Is this component generic — no view-specific state or logic, only `in property` + `callback`? → create in `widgets/`
3. Only if truly view-specific → create as a child in `views/`

```slint
// CORRECT — Mother imports both Views and Widgets
import { HomeView }   from "views/home-view.slint";       // view — only Mother imports this
import { SearchBar }  from "widgets/search-bar.slint";     // widget — reusable everywhere

// CORRECT — View composes from widget library
import { Card }  from "widgets/card.slint";
import { Badge } from "widgets/badge.slint";
// import { SettingsView } from "views/settings-view.slint";  // ERROR: view imports sibling view

// ui/widgets/card.slint — WIDGET (generic, reusable, stateless)
export component Card {
    in property <string> title;
    in property <string> subtitle;
    callback selected();
    // NO in-out property — pure interface
    // NO literals — tokens only (Card.Sizes.*, Colors.*)
}
```

---

## Property Direction as Enforcement

In Slint, property direction is the enforcement mechanism for mother-child:

VITAL: Mother = the component that `inherits Window` — the only component that owns state
VITAL: Children use only `in property` (receive from mother) and `callback` (emit to mother)
BANNED: `in-out property` in any child component — this is state ownership, reserved for mother
RULE: The only exception for `in-out` in a child is `<=>` delegation (two-way binding from mother)
RULE: State values live in a Slint `global` file (see slint/globals.md) — separate from the Window layout
RULE: Children reference design tokens via `Theme.xyz` globals — never raw values

```slint
// MOTHER — app-window.slint (inherits Window, owns all state)
export component AppWindow inherits Window {
    in-out property <string>  active-view: "home";     // ← state ownership OK here
    in-out property <bool>    sidebar-open: true;       // ← state ownership OK here
    callback navigate(string);

    NavBar {
        breadcrumb: root.active-view;                   // ← in property: read-only
        go-back => { root.navigate("home"); }           // ← callback: event up
    }
}

// CHILD — navbar.slint (stateless, receives everything)
export component NavBar inherits Rectangle {
    in property <string>  breadcrumb: "";               // ← receive from mother
    callback go-back();                                  // ← emit to mother
    // NO in-out property here — this is a stateless child
}
```

## ViewModel Structs

When mother owns many related fields for an editor or overlay, they MUST be grouped into a struct.

RULE: Group related editor/overlay state into ViewModel structs in `types.slint` — never pass individual fields as separate properties
RULE: A ViewModel struct is the unit of transfer between mother and a child overlay or editor
BANNED: Passing more than 3 individual fields for the same conceptual state — define a struct instead
BANNED: Declaring the same logical fields in mother AND OverlayHost AND the target view — one struct eliminates all three

```slint
// types.slint — define structs here, not inline in components
export struct UiNodeEditState {
    visible: bool,
    node-id: string,
    label: string,
    x: float,
    y: float,
    node-type: string,
    color: color,
    locked: bool,
    tags: [string],
    description: string,
}

export struct UiPlaybackState {
    playing: bool,
    speed: float,
    current-frame: int,
    total-frames: int,
    loop: bool,
    muted: bool,
}
```

```slint
// WRONG — mother with 16 individual fields for 2 concepts
export component AppWindow inherits Window {
    in-out property <bool>    node-edit-visible;
    in-out property <string>  node-edit-id;
    in-out property <string>  node-edit-label;
    in-out property <float>   node-edit-x;
    // ... 12 more fields
    OverlayHost {
        node-edit-visible: root.node-edit-visible;   // repeated in 3 layers
        node-edit-id:      root.node-edit-id;
        // ...
    }
}

// CORRECT — 2 fields replace 16
export component AppWindow inherits Window {
    in-out property <UiNodeEditState>  node-edit-state;
    in property    <UiPlaybackState>   playback-state;

    OverlayHost {
        node-edit-state: root.node-edit-state;       // one line, not 10
        playback-state:  root.playback-state;
    }
}
```

RESULT: Mother's property block is self-documenting — each struct name reveals its purpose
RESULT: Child interfaces shrink from 10+ `in property` lines to 1 per logical concept
REASON: Struct boundaries are semantic contracts — they enforce cohesion and prevent field sprawl

## Full Example: App Window + Views

```slint
// app-window.slint — MOTHER (inherits Window = state owner)
import { Theme } from "globals/theme.slint";
import { NavBar } from "views/navbar.slint";
import { WorkspaceView } from "views/workspace-view.slint";

export component AppWindow inherits Window {
    in-out property <string>  active-view: "home";
    in-out property <bool>    sidebar-open: true;
    in-out property <string>  selected-item-id;

    background: Theme.bg-primary;

    VerticalLayout {
        NavBar {
            height: Theme.navbar-height;     // ← size lives in mother
            breadcrumb: root.active-view;
            go-back => { root.active-view = "home"; }
        }
        WorkspaceView {
            visible: root.active-view == "workspace";
            item-id: root.selected-item-id;
            item-selected(id) => { root.selected-item-id = id; }
        }
    }
}

// views/navbar.slint — CHILD (stateless: in property + callback only)
export component NavBar inherits Rectangle {
    in property <string>  breadcrumb: "";
    in property <bool>    can-go-back: false;
    callback go-back();
    callback navigate(string);
    // NO in-out property — fills the slot mother provides
}
```
