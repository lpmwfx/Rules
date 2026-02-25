---
tags: [kotlin, stability, compose-stability, immutable]
concepts: [build-system, ci]
requires: [kotlin/compose.md]
keywords: [stable, immutable, compose-compiler]
layer: 4
---
# Build Stability Guardrails

> Version pinning, CI truth, cache hygiene

---

NOTE: Amper uses Gradle internally for Android builds. These rules prevent "Gradle hell".

## Version Pinning

RULE: Pin ALL versions explicitly — Kotlin, Compose, AGP, JDK
RULE: Never use floating versions (`1.+`, `latest.*`)
RULE: Upgrade one dependency at a time, verify CI green
BANNED: Mixing JDK versions between IDE and CLI

## Known-Good Version Set

```
Kotlin: 2.0.x
Compose: 1.8.x (bundled with Amper)
AGP: (managed by Amper)
JDK: 21
```

## CI as Single Source of Truth

RULE: CI preflight build on every PR
RULE: CI builds clean (no local caches)
RULE: Build all targets: Android + JVM/Desktop
RULE: If CI green = it works, local issues are cache problems

## Cache Hygiene (When Things Break)

```bash
# 1. Stop daemons
./amper --stop-daemon  # or: pkill -f gradle

# 2. Clear project cache
rm -rf build/ .gradle/ .amper/

# 3. Clear user cache (last resort)
rm -rf ~/.gradle/caches/

# 4. Rebuild
./amper build
```

RULE: Don't debug "ghost errors" — clear cache first
RULE: If error persists after cache clear, it's a real bug

## Debugging Build Failures

```bash
./amper build --info              # Verbose output
./amper build --stacktrace        # Full stacktrace
./amper build --info --stacktrace # Both
```

RULE: Read actual error, not just "build failed"

## Testing

RULE: Test ViewModels independently
RULE: Use fakes, not mocks
RULE: Test state transitions
RULE: Preview composables for visual testing

```kotlin
class ProductViewModelTest {
    private val fakeRepository = FakeProductRepository()
    private val viewModel = ProductViewModel(fakeRepository)

    @Test
    fun `loadProducts updates state with products`() = runTest {
        fakeRepository.setProducts(listOf(testProduct))
        viewModel.loadProducts()
        assertEquals(listOf(testProduct), viewModel.state.value.items)
    }
}
```
