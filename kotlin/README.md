---
tags: []
concepts: [kotlin-rules]
related: [kotlin/result-pattern.md, kotlin/encapsulation.md, kotlin/data-classes.md, kotlin/coroutines.md, kotlin/ktor.md, kotlin/amper.md, kotlin/stability.md, uiux/components.md, uiux/state-flow.md, global/module-tree.md]
layer: 6
---
# Kotlin Rules

> Amper — 100% pure Kotlin, encapsulation-first

---

## Philosophy

RULE: Pure Kotlin API — Java imports only in platform layer, encapsulated behind Kotlin interfaces
RULE: Amper for builds (Gradle hidden for Android, Gradle-free for Desktop)
RULE: Encapsulation and modularity first — `private` by default, expose only at module boundary
RULE: Null-safe, type-safe, AI-friendly code
RULE: One class/object per file — nesting = package of files, not nested classes
RULE: Stateless — all app state in a central `AppState` data class; UI layer receives state, emits events
RULE: No state in functions or components — functions transform, never store

See: [global/module-tree.md](../global/module-tree.md) | [uiux/state-flow.md](../uiux/state-flow.md)

## Files

| File | Topic |
|------|-------|
| [data-classes.md](data-classes.md) | Immutable data classes |
| [encapsulation.md](encapsulation.md) | Private by default + platform encapsulation |
| [result-pattern.md](result-pattern.md) | Sealed Result type |
| [amper.md](amper.md) | Amper build system |
| [ktor.md](ktor.md) | Ktor client |
| [coroutines.md](coroutines.md) | Coroutines + dispatchers |
| [stability.md](stability.md) | Build stability guardrails |
| [quick-ref.md](quick-ref.md) | Quick reference |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
