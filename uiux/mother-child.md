---
tags: [uiux, mother-child, composition-root, stateless, layout-ownership, modular]
concepts: [mother-child-pattern, composition-root, stateless-children, layout-ownership]
requires: [global/mother-tree.md, uiux/components.md, uiux/state-flow.md]
feeds: [uiux/file-structure.md]
related: [global/topology.md, global/adapter-layer.md, uiux/tokens.md, slint/globals.md, global/module-tree.md]
keywords: [mother, child, root, shell, view, nav, editor, sidebar, layout, size, state-owner, props, stateless, modular, single-owner, in-out, in-property, callback, overlay, 3-level]
layer: 2
---
# Mother–Child UI Composition

> One mother owns everything — children know nothing except what mother gives them

---

VITAL: Every UI has exactly one mother — the root component that owns all state and all layout
VITAL: Children are stateless modules — they render what they receive, nothing more
VITAL: Children have no hardcoded sizes — mother controls all dimensions and positions
RULE: Mother passes state down to each child as props — children never fetch or derive their own
RULE: Children emit events up to mother — mother decides what to do with them
RULE: All styling that affects layout (size, position, flex, grid, padding between sections) lives in mother only
RULE: A child may style only its own internal presentation (font weight, icon color, inner padding)
BANNED: Child components querying global state, stores, or context directly
BANNED: Child components importing from sibling components — siblings never know each other
BANNED: Hardcoded width, height, or min/max-size in a child component
BANNED: Children sharing state with each other — all shared state routes through mother
BANNED: Mother delegating state ownership to a child and re-reading it back

## Why This Works for AI Development

An AI only ever needs to understand **one file at a time**:

- To change how a view looks → read the child view file — it is fully self-contained
- To change what data a view receives → read mother — that is the single source of truth
- To add a new view → write one new child file, wire it into mother — nothing else changes
- To debug a layout issue → read mother only — all sizes and positions are there

RULE: Every child file is independently understandable — no hidden state, no global dependencies
RESULT: AI can reason about each module in isolation — the surface area is exactly one file
REASON: When children are pure functions of their props, the entire UI is a tree of simple transforms

## Structure

```
AppShell (mother)
├── owns: activeView, sidebarOpen, selectedItem, windowSize, theme
├── owns: all layout tokens passed to children
│
├── NavBar (child)          ← receives: activeView, onNavigate
├── EditorPanel (child)     ← receives: selectedItem, onSave, onCancel
├── ViewA (child)           ← receives: items, onSelect
├── ViewB (child)           ← receives: stats, onFilter
└── ViewC (child)           ← receives: settings, onChange
```

RULE: Mother is the **only** place where `if activeView === 'A'` logic lives
RULE: NavBar does not know that ViewA exists — it only emits `navigate(viewId)`
RULE: EditorPanel does not know what selected the item — it only receives it

## 3-Level Hierarchy: Mother → View → Module

The pattern is recursive. A real app typically has 3 levels:

```
Mother (Window / AppShell — owns ALL state)
├── NavBar (view)             ← stateless, in property + callback
├── WorkspaceView (view)      ← stateless, but composes sub-modules
│   ├── LeftPanel (module)    ← stateless child of WorkspaceView
│   ├── Canvas (module)       ← stateless child of WorkspaceView
│   └── Inspector (module)    ← stateless child of WorkspaceView
├── OutputView (view)         ← stateless
└── Overlays (view-level)     ← modal/dialog children, visibility controlled by mother
```

VITAL: Views are direct children of mother — they see only what mother gives them
VITAL: Modules are children of views — they see only what their parent view gives them
RULE: A view that composes modules becomes mother for its own subtree
RULE: Overlays (modals, dialogs, toasts) are children of mother — not of the view that triggered them
RULE: Overlay visibility is state owned by mother — children emit `show-overlay()`, mother toggles it
BANNED: A module reaching up past its parent view to access mother state
BANNED: An overlay owned by or embedded inside a child view

## Layout Ownership

Mother decides where children are placed and how large they are:

```
// MOTHER controls layout
AppShell {
    sidebar-width: 240px   ← lives here, nowhere else
    content-height: 100%   ← lives here, nowhere else

    NavBar { /* fills the sidebar slot mother provides */ }
    ViewA  { /* fills the content slot mother provides */ }
}
```

```
// CHILD fills its slot — no own sizing
NavBar {
    /* only internal: icon size, label font, item spacing */
    /* never: width, height, position */
}
```

BANNED: `width: 240px` inside `NavBar.tsx` — that measurement belongs to mother
BANNED: `position: absolute` inside a child that fixes itself to a screen edge
RULE: Children use `width: 100%`, `flex: 1`, `fill-available`, or the equivalent — they fill their slot

## Slint-Specific Enforcement

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

## Slint ViewModel Structs

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

## Cross-Toolkit Examples

### React / SolidJS

```tsx
// AppShell.tsx — MOTHER
export function AppShell({ state }: { state: AppState_adp }) {
  return (
    <div className="shell" style={{ '--sidebar-w': '240px' }}>
      <NavBar activeView={state.activeView} onNavigate={state.navigate} />
      <main className="content">
        {state.activeView === 'editor' && (
          <EditorPanel item={state.selectedItem} onSave={state.saveItem} />
        )}
        {state.activeView === 'list' && (
          <ItemList items={state.items} onSelect={state.selectItem} />
        )}
      </main>
    </div>
  )
}

// NavBar.tsx — CHILD (stateless, no sizes)
export function NavBar({ activeView, onNavigate }: NavBarProps) {
  return (
    <nav>  {/* fills 100% of whatever slot mother provides */}
      <NavItem id="list"   active={activeView === 'list'}   onNavigate={onNavigate} />
      <NavItem id="editor" active={activeView === 'editor'} onNavigate={onNavigate} />
    </nav>
  )
}
```

### Slint

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

### Jetpack Compose

```kotlin
// AppShell.kt — MOTHER
@Composable
fun AppShell(state: AppState_adp) {
    Row {
        NavBar(
            modifier = Modifier.width(240.dp),  // ← size in mother
            activeView = state.activeView,
            onNavigate = state::navigate
        )
        Box(modifier = Modifier.weight(1f)) {
            when (state.activeView) {
                "editor" -> EditorPanel(item = state.selectedItem, onSave = state::saveItem)
                "list"   -> ItemList(items = state.items, onSelect = state::selectItem)
            }
        }
    }
}

// NavBar.kt — CHILD (no Modifier.width — fills what mother passes)
@Composable
fun NavBar(modifier: Modifier = Modifier, activeView: String, onNavigate: (String) -> Unit) {
    Column(modifier = modifier) {  // ← accepts modifier from mother, adds nothing to size
        NavItem("list",   activeView, onNavigate)
        NavItem("editor", activeView, onNavigate)
    }
}
```

## The Topology Rule Applied to UI

The same DAG that governs layers governs components:

```
Mother (root)
  └── props down ──► Child
  ◄── events up ───┘ Child

Children never communicate horizontally.
All cross-child coordination happens in mother.
```

RULE: This pattern mirrors the Adapter → UI relationship — Adapter is "mother" for the whole UI layer
RULE: Apply this pattern recursively — if a child has sub-children, the child becomes mother for its subtree
RULE: At each level there is exactly one owner of state and layout for that subtree

## Rust Backend Mother–Child

The same pattern applies to Rust module structure (see global/topology.md):

RULE: `mod.rs` / `main.rs` / `lib.rs` are mother files — they compose and wire children
RULE: Child modules are stateless — they receive state as parameters, return results
BANNED: Mother files with many `fn` definitions — extract to child modules
BANNED: Child modules with `static`, `lazy_static!`, `thread_local!`, or `OnceLock` — state belongs in mother

```rust
// callbacks/mod.rs — MOTHER (composes children, owns SharedState)
pub struct SharedState { /* all shared state lives here */ }

pub fn register_all(ui: &AppWindow, state: SharedState) {
    canvas::register(ui, &state);    // ← delegate to child
    inspector::register(ui, &state); // ← delegate to child
    file_ops::register(ui, &state);  // ← delegate to child
}

// callbacks/canvas.rs — CHILD (stateless, receives what it needs)
pub fn register(ui: &AppWindow, state: &SharedState) {
    // NO static, NO lazy_static, NO OnceLock here
    // receives state as parameter, emits results via ui callbacks
}
```

RESULT: Changing any child is safe — it cannot affect siblings or parents
RESULT: Adding a new view requires touching exactly two files: the new child + mother's routing
REASON: Isolated modules with a single owner are the smallest possible unit of change
