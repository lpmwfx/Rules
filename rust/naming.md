---
tags: [rust, naming, conventions, layer-tag]
concepts: [naming-conventions, readability]
requires: [global/consistency.md, global/topology.md]
related: [python/naming.md, css/naming.md, global/naming-suffix.md]
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

RULE: All types use a layer-tag suffix matching their architectural role
RULE: Tag = folder the type lives in — see [global/topology.md](../global/topology.md) for the canonical tag list
NOT: Computed hex checksums, project-brand codes, or arbitrary suffixes
SCOPE: All types (structs, enums, traits) — local variables and private helpers excluded

## Standard Conventions

```rust
mod my_module;              // snake_case modules
struct ConfigLoader;        // PascalCase types
fn load_config();           // snake_case functions
const MAX_RETRIES: u32 = 3; // SCREAMING_SNAKE constants
let file_path: PathBuf;     // snake_case variables
```
