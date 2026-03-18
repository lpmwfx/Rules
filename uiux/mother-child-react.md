---
tags: [uiux, mother-child, react, solidjs, jsx, stateless]
concepts: [react-mother-child, composition-pattern-react]
requires: [uiux/mother-child.md, web/mother-child.md]
related: [js/modules.md, uiux/state-flow.md]
keywords: [AppShell, NavBar, EditorPanel, props, stateless, React, SolidJS, JSX, className, onNavigate]
layer: 4
---
# Mother-Child — React/SolidJS Implementation

> AppShell owns state and layout — children are pure functions of props

---

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

RULE: Mother sets `style` variables for layout — children fill their slot with `100%` or `flex: 1`
RULE: Children accept a props interface — never import from sibling components or context

RESULT: Each component file is independently testable — pass props, assert output
REASON: Global state in children creates hidden coupling that breaks when views are reordered
