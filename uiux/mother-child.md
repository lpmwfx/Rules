---
tags: [uiux, mother-child, composition-root, stateless, layout-ownership, modular]
concepts: [mother-child-pattern, composition-root, stateless-children, layout-ownership]
requires: [uiux/components.md, uiux/state-flow.md]
feeds: [uiux/file-structure.md]
related: [global/topology.md, global/adapter-layer.md, uiux/tokens.md]
keywords: [mother, child, root, shell, view, nav, editor, sidebar, layout, size, state-owner, props, stateless, modular, single-owner]
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
// AppShell.slint — MOTHER
component AppShell {
    in property <AppState> state;

    HorizontalLayout {
        NavBar {
            width: 240px;          // ← size lives in mother
            active-view: state.active-view;
            navigate => { state.navigate(view-id); }
        }
        Rectangle {
            width: parent.width - 240px;
            EditorPanel {
                visible: state.active-view == "editor";
                item: state.selected-item;
                save => { state.save-item(); }
            }
        }
    }
}

// NavBar.slint — CHILD (no width/height of its own)
component NavBar {
    in property <string> active-view;
    callback navigate(string);
    // fills the slot mother provides — no size declared here
    VerticalLayout { /* nav items */ }
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

RESULT: Changing any child is safe — it cannot affect siblings or parents
RESULT: Adding a new view requires touching exactly two files: the new child + mother's routing
REASON: Isolated modules with a single owner are the smallest possible unit of change
