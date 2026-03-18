---
tags: [uiux, mother-child, swiftui, ios, macos, stateless]
concepts: [swiftui-mother-child, composition-pattern-swiftui, state-ownership]
requires: [uiux/mother-child.md, global/mother-tree.md]
related: [uiux/mother-child-compose.md, uiux/mother-child-react.md, slint/mother-child.md]
keywords: [StateObject, Binding, ObservedObject, EnvironmentObject, AppShell, NavBar, mother, child, SwiftUI, View, ObservableObject]
layer: 5
---
# Mother-Child — SwiftUI Implementation

> Mother owns `@StateObject` — children observe via `@Binding` or `@ObservedObject`

---

RULE: Mother view owns `@StateObject` — single source of truth
RULE: Children receive `@Binding` or `@ObservedObject` — never own state
RULE: `@EnvironmentObject` for deep injection (theme, config) — not for component state
RULE: Mother is the only `View` that creates the `ObservableObject`

```swift
// AppState.swift — shared observable
class AppState: ObservableObject {
    @Published var activeView: ViewId = .list
    @Published var selectedItem: Item? = nil
    @Published var items: [Item] = []
}

// AppShell.swift — MOTHER (owns state)
struct AppShell: View {
    @StateObject private var state = AppState()

    var body: some View {
        NavigationSplitView {
            NavBar(activeView: $state.activeView)
        } detail: {
            if let item = state.selectedItem {
                EditorPanel(item: item, onSave: { state.save($0) })
            } else {
                ItemList(items: state.items, onSelect: { state.selectedItem = $0 })
            }
        }
    }
}

// NavBar.swift — CHILD (stateless, receives binding)
struct NavBar: View {
    @Binding var activeView: ViewId

    var body: some View {
        List(ViewId.allCases, id: \.self) { view in
            NavItem(id: view, isActive: activeView == view)
                .onTapGesture { activeView = view }
        }
    }
}
```

BANNED: `@State` in child views for data that belongs to mother
BANNED: `@StateObject` in children — they observe, never own
BANNED: Children fetching data directly — mother provides all inputs

RESULT: Each child is a pure function of its bindings — independently previewable
REASON: Scattered `@StateObject` creates multiple sources of truth that drift apart
