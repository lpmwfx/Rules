---
tags: [rust, naming, conventions, layer-tag]
concepts: [naming-conventions, readability]
requires: [global/consistency.md, global/topology.md]
related: [python/naming.md, css/naming.md]
layer: 3
---
# Naming Rules

> Anti-variable-noise + layer-tag convention

---

## Overriding Principle

RULE: A name must explain WHY the variable exists — not just WHAT it contains

## Forbidden Names (without domain suffix)

BANNED: `data`, `info`, `value`, `item`, `object`, `temp`, `state`, `ctx`, `result`, `res`, `var`

ALLOWED with domain: `payment_state`, `parse_result`, `request_context`

## Lifecycle Names

RULE: Names must reflect phase:
- `*_input` — raw external input
- `*_parsed` — structured but unvalidated
- `*_validated` — semantically valid
- `*_resolved` — all references resolved
- `*_final` — ready for side-effects

## Scope Rules

RULE: Scope < 5 lines: short names ok (`i`, `id`, `len`)
RULE: Scope >= 5 lines: semantic names REQUIRED

## Collections

RULE: Plural MANDATORY for collections: `users`, `tokens`
RULE: Iterator uses role, not type: `for user in users`

## Booleans

RULE: Must start with `is_`, `has_`, `can_`, `should_`

## Functions

RULE: Verbs first
RULE: No type-leak in name
BANNED: `get_user_data()` → GOOD: `load_user()`

## Layer-Tag Suffix

RULE: All types use a layer-tag suffix matching their architectural role — see global/topology.md
RULE: Use the tag that matches where the type lives in the folder structure
NOT: Computed hex checksums, project-brand codes, or arbitrary suffixes
SCOPE: All types (structs, enums, traits) — local variables and private helpers excluded

| Tag | Layer | Rust example |
|-----|-------|-------------|
| `_ui` | UI | `LoginView_ui`, `AppWindow_ui` |
| `_adp` | Adapter | `UserAdapter_adp`, `AppState_adp` |
| `_core` | Core | `AuthLogic_core`, `PriceCalc_core` |
| `_pal` | PAL | `WindowManager_pal`, `Clipboard_pal` |
| `_gtw` | Gateway | `ConfigLoader_gtw`, `FileStore_gtw` |
| `_sta` | State struct | `AppState_sta`, `CoreState_sta` |
| `_cfg` | Config struct | `AppConfig_cfg`, `NetworkConfig_cfg` |
| `_x` | Shared/cross-cutting | `AppError_x`, `Persistable_x` |

## Standard Conventions

```rust
mod my_module;              // snake_case modules
struct ConfigLoader;        // PascalCase types
fn load_config();           // snake_case functions
const MAX_RETRIES: u32 = 3; // SCREAMING_SNAKE constants
let file_path: PathBuf;     // snake_case variables
```
