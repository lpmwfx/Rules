---
tags: [uiux, mother-child, compose, jetpack, stateless]
concepts: [compose-mother-child, composition-pattern-compose]
requires: [uiux/mother-child.md]
related: [uiux/state-flow.md]
keywords: [AppShell, NavBar, Modifier, width, weight, Composable, Column, Row, state, onNavigate]
layer: 4
---
# Mother-Child — Jetpack Compose Implementation

> AppShell owns state and layout — children accept `Modifier` from mother

---

```kotlin
// AppShell.kt — MOTHER
@Composable
fun AppShell(state: AppState_adp) {
    Row {
        NavBar(
            modifier = Modifier.width(240.dp),  // size in mother
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
    Column(modifier = modifier) {  // accepts modifier from mother, adds nothing to size
        NavItem("list",   activeView, onNavigate)
        NavItem("editor", activeView, onNavigate)
    }
}
```

RULE: Mother passes `Modifier.width()` — child never sets its own width
RULE: Child accepts `modifier: Modifier = Modifier` as first parameter — applies it to root composable
RULE: `when` block in mother selects active view — children do not know about each other

RESULT: Adding a view = one new composable file + one `when` arm in mother — nothing else changes
REASON: Children with hardcoded `Modifier.width` create layout conflicts when mother rearranges them


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
