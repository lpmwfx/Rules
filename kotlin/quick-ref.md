---
tags: []
concepts: []
related: [kotlin/result-pattern.md, kotlin/encapsulation.md, kotlin/coroutines.md, uiux/components.md]
layer: 6
---
# Kotlin Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Philosophy | 100% Kotlin, no Java interop |
| UI | See uiux/ — components stateless, state flows from Adapter |
| Build | Amper `module.yaml`, no Gradle files |
| State | Central `AppState` data class — UI renders it, Adapter updates it |
| Data | Immutable `data class`, `val` only, `copy()` |
| Encapsulation | Private by default, `internal` for modules, one class per file |
| Nesting | Packages = folders of files — no nested classes |
| Platform | Java imports ONLY in `platform/` layer |
| Results | Sealed `Result<T>` with Success/Error |
| Network | Ktor single client, ContentNegotiation |
| Coroutines | `Dispatchers.IO` for I/O, `Dispatchers.Default` for CPU, never block main |
| Testing | Fakes not mocks, test Adapter state transitions |
| Naming | PascalCase classes, camelCase functions, SCREAMING constants |
| BANNED | Java interop, JNI, mutable public props, Gradle files, god classes |
