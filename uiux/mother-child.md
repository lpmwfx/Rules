---
tags: [uiux, mother-child, composition-root, stateless, layout-ownership, modular]
concepts: [mother-child-pattern, composition-root, stateless-children, layout-ownership]
requires: [global/mother-tree.md, uiux/components.md, uiux/state-flow.md]
feeds: [uiux/file-structure.md, slint/mother-child.md]
related: [global/topology.md, global/adapter-layer.md, uiux/tokens.md, slint/globals.md, global/module-tree.md, slint/mother-child.md]
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

> **Rust**: the same mother-child pattern applied to module structure — see [global/topology.md](../global/topology.md)

## Proc-Macro Exemption (Rust)

Some proc macros require all handler functions in a single `impl` block — this is a compiler constraint,
not a design choice. The fn-count limit is waived for these cases.

RULE: When a proc macro requires all functions in one impl block, the fn-count limit does not apply —
      PROVIDED each fn body is a thin delegation (≤ ~5 lines) forwarding to a child module.
RULE: The impl block itself stays in the mother file — only the logic moves to children.
REASON: The macro is the constraint. Splitting the impl would break compilation. The developer
        has no choice — enforcing the limit here would be counterproductive.

Known bundling macros (scanner-exempt):
- `#[tool_router]` — rmcp MCP server tool dispatch (all tool handlers in one impl)
- `#[async_trait]` — trait impl with async methods (async-trait crate requirement)
- `#[tonic::async_trait]` — gRPC service impl (tonic framework requirement)

```rust
// lib.rs — MOTHER: tool router stays here (macro requires it), logic goes to children
#[tool_router]
impl MyMcpServer {
    #[tool(description = "Get selection")]
    async fn get_selection(&self, ...) -> ... {
        selection_ui::get(&self.state).await  // ← thin delegation: 1-2 lines
    }

    #[tool(description = "Insert block")]
    async fn insert_block(&self, ...) -> ... {
        build_block_ui::insert(&self.state, params).await  // ← thin delegation
    }
}

// src/ui/selection_ui.rs — CHILD: all logic here
pub async fn get(state: &AppState) -> Result<...> {
    // real implementation
}
```

BANNED: Tool handler fn bodies with business logic — delegate to a child module
BANNED: Tool handler fn bodies longer than ~5 lines — that is logic leaking into the router
