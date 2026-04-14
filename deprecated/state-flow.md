DEPRECATED — see sid-architecture/data-driven-runtime.md (prototype)

---
tags: [uiux, state-flow, state-in, events-out, adapter, reactive, declarative, slintscanners]
concepts: [state-management, event-flow, adapter-binding, reactive-ui, slint-build-scan]
requires: [global/adapter-layer.md, uiux/components.md, uiux/mother-child.md]
related: [global/persistent-state.md, global/app-model.md, uiux/file-structure.md, slint/init.md]
keywords: [state, events, binding, observable, adapter, props, emit, reactive, loading, error, empty, AdapterState, slintscanners, build-scan]
layer: 3
---
# UI State Flow

> State in from Adapter, events out to Adapter — components never own domain state

---

VITAL: UI components receive state from Adapter — never from Core or Gateway directly
VITAL: UI components emit events to Adapter — never call Core directly
RULE: Components are pure renderers — given the same state, they render the same output
RULE: The Adapter owns AdapterState_sta — UI reads it, never mutates it
RULE: Every loading, error, and empty state must be handled — no silent blanks
RULE: Local UI state (focus, hover, open/closed) is the only state a component may own
BANNED: Fetching data from inside a component
BANNED: Calling domain/business functions from inside a component
BANNED: Mutating shared state directly from the UI

## The Contract

```
Adapter                         Component
  │                                │
  │── state: AdapterState_sta ────►│ render()
  │                                │
  │◄─── event: UserAction ─────────│ onClick / onInput / onSubmit
  │                                │
  │  validates + dispatches        │
  │  updates AdapterState_sta ────►│ re-render
```

RULE: One-way data flow — state flows down, events flow up
RULE: Components declare what they need (typed props/state-in) — never reach up for it
RULE: Events carry only the data needed — not the full state object

## State Shape

Every view has a corresponding state struct in the Adapter:

```
AdapterState_sta {
    // Content
    items: List<ItemViewModel_adp>
    selected: Option<ItemViewModel_adp>

    // Status
    is_loading: bool
    error: Option<String>
    is_empty: bool   // derived: items.isEmpty && !is_loading

    // Pure UI state (scroll, panels)
    scroll_offset: u32
    active_tab: TabId_ui
}
```

RULE: `ItemViewModel_adp` is a flat, UI-ready struct — no domain objects reach the component
RULE: Status flags (`is_loading`, `error`, `is_empty`) are always explicit — never inferred in the component

## Handling All States

RULE: Every component that shows async data MUST handle: loading, error, empty, and content
BANNED: Rendering only the happy path and leaving loading/error as blank screen

### React

```tsx
function ItemList({ state, onSelect }: { state: ItemListState; onSelect: (id: string) => void }) {
  if (state.isLoading) return <LoadingSpinner />
  if (state.error)     return <ErrorMessage message={state.error} />
  if (state.isEmpty)   return <EmptyState label="No items yet" />

  return (
    <ul>
      {state.items.map(item => (
        <ItemCard key={item.id} item={item} onSelect={onSelect} />
      ))}
    </ul>
  )
}
```

### Compose

```kotlin
@Composable
fun ItemList(state: ItemListState_adp, onSelect: (String) -> Unit) {
    when {
        state.isLoading -> LoadingSpinner()
        state.error != null -> ErrorMessage(state.error)
        state.isEmpty -> EmptyState("No items yet")
        else -> LazyColumn {
            items(state.items) { item ->
                ItemCard(item = item, onSelect = onSelect)
            }
        }
    }
}
```

### QML

```qml
StackLayout {
    currentIndex: state.isLoading ? 0 : state.error ? 1 : state.isEmpty ? 2 : 3

    LoadingSpinner {}
    ErrorMessage    { message: state.error ?? "" }
    EmptyState      { label: "No items yet" }
    ItemListContent { model: state.items; onSelect: (id) => adapter.selectItem(id) }
}
```

### GTK4 / Python

```python
def _update_view(self, state: ItemListState):
    if state.is_loading:
        self._stack.set_visible_child_name("loading")
    elif state.error:
        self._error_label.set_text(state.error)
        self._stack.set_visible_child_name("error")
    elif state.is_empty:
        self._stack.set_visible_child_name("empty")
    else:
        self._populate(state.items)
        self._stack.set_visible_child_name("content")
```

## Local UI State

Components may own state that has no domain meaning and is not persisted:

RULE: Focus, hover, tooltip visibility, animation progress — fine as local state
RULE: Open/closed for a dropdown or modal within one component — fine as local state
BANNED: Local state for anything the Adapter or Core cares about
BANNED: Derived state re-computed in the component — compute it in the Adapter

```tsx
// OK — pure interaction state, no domain meaning
const [isOpen, setIsOpen] = useState(false)

// BANNED — domain state kept locally
const [items, setItems] = useState<Item[]>([])  // belongs in Adapter
```

RESULT: UI is a pure projection of Adapter state — predictable, testable, replaceable
REASON: When state only flows one direction, every render is reproducible from state alone


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
