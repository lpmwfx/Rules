---
tags: [uiux, mother-child, composition-root, stateless, layout-ownership, modular]
concepts: [mother-child-pattern, composition-root, stateless-children, layout-ownership]
requires: [global/mother-tree.md, uiux/components.md, uiux/state-flow.md]
feeds: [uiux/file-structure.md, slint/mother-child.md, uiux/mother-child-react.md, uiux/mother-child-compose.md, rust/proc-macro-exemption.md, web/mother-child.md]
related: [global/topology.md, global/adapter-layer.md, uiux/tokens.md, slint/globals.md, global/module-tree.md, slint/mother-child.md, global/data-driven-ui.md]
keywords: [mother, child, root, shell, view, nav, editor, sidebar, layout, size, state-owner, props, stateless, modular, single-owner, in-out, in-property, callback, overlay, 3-level]
layer: 2
---
# Mother-Child UI Composition

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

## 3-Level Hierarchy: Mother → View → Widget

The pattern is recursive. A real app typically has 3 levels:

```
Mother (Window / AppShell — owns ALL state)
├── imports Views              ← screens/pages, view-specific, stateless
└── imports Widgets            ← generic, reusable across views, stateless

Views (views/)
├── NavBar                     ← stateless, in property + callback
├── WorkspaceView              ← stateless, composes widgets
└── OutputView                 ← stateless

Widgets (widgets/ or components/ or shared/)
├── Card, Badge, SearchBar     ← generic UI — in property + callback only
├── reusable across any view   ← promoted here when used in 2+ views
└── zero-literal               ← tokens only, no hardcoded values
```

VITAL: Views are direct children of mother — they see only what mother gives them
VITAL: Widgets are the shared component library — generic, stateless, importable by anyone
RULE: Views may only be imported by Mother — never by another View
RULE: A component used in 2+ views must be promoted to `widgets/` — never copied
RULE: Overlays (modals, dialogs, toasts) are children of mother — not of the view that triggered them
RULE: Overlay visibility is state owned by mother — children emit `show-overlay()`, mother toggles it
RULE: When a view grows beyond ~10 children, check `widgets/` before creating more view-specific children
BANNED: A View importing another View — extract shared components to `widgets/` instead
BANNED: Copying a component into multiple views — promote to widgets/
BANNED: An overlay owned by or embedded inside a child view

Decision flow for every new child component:
1. Does `widgets/` (or `shared/`) already cover this? → use it
2. Is this component generic — no screen-specific logic? → create in `widgets/`
3. Only if truly screen-specific → create as a view child

> **Slint**: Views live in `ui/views/`, widgets in `ui/widgets/` — see [slint/mother-child.md](../slint/mother-child.md)

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

> **Slint**: property direction (`in`, `in-out`, `callback`) and ViewModel structs — see [slint/mother-child.md](../slint/mother-child.md)

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

> **Rust**: the same mother-child pattern applied to module structure — see [global/topology.md](../global/topology.md)

Cross-toolkit implementations: [uiux/mother-child-react.md](mother-child-react.md) | [uiux/mother-child-compose.md](mother-child-compose.md)
Proc-macro exemption (Rust): [rust/proc-macro-exemption.md](../rust/proc-macro-exemption.md)
