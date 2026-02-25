---
tags: [kotlin, viewmodel, state-management, mvvm]
concepts: [state-management, mvvm]
requires: [kotlin/compose.md]
keywords: [viewmodel, state-flow, ui-state]
layer: 4
---
# ViewModel Pattern

> Sealed actions, data class state, StateFlow

---

RULE: Sealed class for actions
RULE: Data class for state
RULE: StateFlow for reactive state
RULE: No Android imports in shared ViewModels

```kotlin
data class HomeState(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

sealed class HomeAction {
    data object Refresh : HomeAction()
    data class SelectItem(val id: String) : HomeAction()
    data object ClearError : HomeAction()
}

class HomeViewModel(
    private val repository: ItemRepository
) {
    private val _state = MutableStateFlow(HomeState())
    val state: StateFlow<HomeState> = _state.asStateFlow()

    fun onAction(action: HomeAction) {
        when (action) {
            is HomeAction.Refresh -> refresh()
            is HomeAction.SelectItem -> selectItem(action.id)
            is HomeAction.ClearError -> clearError()
        }
    }

    private fun refresh() {
        // Implementation
    }
}
```
