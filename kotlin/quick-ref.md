# Kotlin Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Philosophy | 100% Kotlin, no Java interop |
| UI | Jetpack Compose, state hoisting, pure functions |
| Build | Amper `module.yaml`, no Gradle files |
| State | Sealed actions + data class state + StateFlow |
| Data | Immutable `data class`, `val` only, `copy()` |
| Encapsulation | Private by default, `internal` for modules |
| Platform | Java imports ONLY in `platform/` layer |
| Results | Sealed `Result<T>` with Success/Error |
| Network | Ktor single client, ContentNegotiation |
| Coroutines | `viewModelScope`, `Dispatchers.IO`, never block main |
| Testing | Fakes not mocks, test state transitions |
| Naming | PascalCase classes, camelCase functions, SCREAMING constants |
| BANNED | Java interop, JNI, mutable public props, Gradle files, god classes |
