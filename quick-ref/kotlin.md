---
tags: [combo, kotlin]
concepts: [quick-ref, project-type]
keywords: [kotlin, compose, amper, coroutines]
requires: [global/quick-ref.md, kotlin/quick-ref.md, uiux/components.md]
layer: 6
binding: true
---
# Quick Reference: Kotlin Project

> Kotlin app with Compose UI. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | Kotlin: 250 lines max. Split into child composables | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## Kotlin-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | 100% Kotlin, no Java interop | [kotlin/encapsulation.md](../kotlin/encapsulation.md) |
| Build | Amper `module.yaml`, no Gradle files | [kotlin/encapsulation.md](../kotlin/encapsulation.md) |
| State | Central `AppState` data class — UI renders it, Adapter updates it | [kotlin/result-pattern.md](../kotlin/result-pattern.md) |
| Data | Immutable `data class`, `val` only, `copy()` | [kotlin/encapsulation.md](../kotlin/encapsulation.md) |
| Encapsulation | Private by default, `internal` for modules, one class per file | [kotlin/encapsulation.md](../kotlin/encapsulation.md) |
| Platform | Java imports ONLY in `platform/` layer | [kotlin/encapsulation.md](../kotlin/encapsulation.md) |
| Results | Sealed `Result<T>` with Success/Error | [kotlin/result-pattern.md](../kotlin/result-pattern.md) |
| Coroutines | `Dispatchers.IO` for I/O, `Dispatchers.Default` for CPU, never block main | [kotlin/coroutines.md](../kotlin/coroutines.md) |
| Testing | Fakes not mocks, test Adapter state transitions | [kotlin/result-pattern.md](../kotlin/result-pattern.md) |

## UI/UX rules (Compose)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Components | One file per component, stateless, state-in events-out | [uiux/components.md](../uiux/components.md) |
| Mother-child | Mother owns layout, children are self-contained composables | [uiux/mother-child-compose.md](../uiux/mother-child-compose.md) |
| State flow | State-in from Adapter, events-out to Adapter | [uiux/state-flow.md](../uiux/state-flow.md) |
| Tokens | Zero literal values — all values from design tokens | [uiux/tokens.md](../uiux/tokens.md) |
| Theming | System light/dark — live switching | [uiux/theming.md](../uiux/theming.md) |
| Keyboard | Standard shortcuts, keyboard navigation | [uiux/keyboard.md](../uiux/keyboard.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | Kotlin compiler, Compose preview |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all Kotlin checks |

## BANNED

- Java interop, JNI
- Mutable public properties
- Gradle files — use Amper
- God classes (classes over 250 lines)
- Files over 250 lines
- Deep nesting (4+ levels)
- `utils/`, `helpers/`, `common/` packages
- Non-English code, comments, or identifiers

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
