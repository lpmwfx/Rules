# Compose UI Rules

> Pure functions, state hoisting, small composables

---

RULE: Composables are pure functions — no side effects
RULE: State hoisting — lift state up, pass down
RULE: Small composables — extract when > 50 lines
RULE: Preview all composables
RULE: Max 200-300 lines per file
RULE: One responsibility per file

## Screen Composable Structure

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onNavigate: (Route) -> Unit
) {
    val state by viewModel.state.collectAsState()

    HomeContent(
        state = state,
        onAction = viewModel::onAction,
        onNavigate = onNavigate
    )
}

@Composable
private fun HomeContent(
    state: HomeState,
    onAction: (HomeAction) -> Unit,
    onNavigate: (Route) -> Unit
) {
    // UI implementation
}

@Preview
@Composable
private fun HomeContentPreview() {
    AppTheme {
        HomeContent(
            state = HomeState(),
            onAction = {},
            onNavigate = {}
        )
    }
}
```

## State Hoisting

```kotlin
// BAD - state inside composable
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) { Text("$count") }
}

// GOOD - state hoisted
@Composable
fun Counter(
    count: Int,
    onIncrement: () -> Unit
) {
    Button(onClick = onIncrement) { Text("$count") }
}
```

## File Organization

```
eu.psid.citizen/
├── MainActivity.kt          # Entry point only
├── App.kt                   # App composition root
├── theme/
│   ├── Colors.kt
│   ├── Typography.kt
│   └── Theme.kt
├── ui/
│   ├── home/
│   │   ├── HomeScreen.kt
│   │   ├── HomeViewModel.kt
│   │   └── HomeComponents.kt
│   └── scanner/
│       ├── ScannerScreen.kt
│       └── ScannerViewModel.kt
├── data/
│   ├── api/
│   │   ├── ApiClient.kt
│   │   └── Endpoints.kt
│   └── models/
│       ├── Product.kt
│       └── Cart.kt
└── util/
    └── Extensions.kt
```
