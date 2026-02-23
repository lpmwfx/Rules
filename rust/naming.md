# Naming Rules

> Anti-variable-noise + hex-suffix convention

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

## Hex-Suffix Convention (Namespace Guarantee)

PURPOSE: Guarantee against namespace conflicts with Rust crates/stdlib
SCOPE: All pub items (structs, enums, traits, pub functions)
NOT: Local variables, private helpers
FORMAT: `Name_XXX` where XXX = `hex(sum(ascii(lowercase(name))) % 4096)`
SEPARATOR: Always underscore before hex-suffix
SUFFIX: Always 3 hex digits (zero-padded)

```rust
fn hex_suffix(name: &str) -> String {
    let sum: u32 = name.to_lowercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .map(|c| c as u32)
        .sum();
    format!("{:03X}", sum % 4096)
}
```

Examples:
- `Session` → `Session_304`
- `Engine` → `Engine_276`
- `LocalPty` → `LocalPty_6A7`
- `SessionBackend` → `SessionBackend_5F3`

## Standard Conventions

```rust
mod my_module;              // snake_case modules
struct ConfigLoader;        // PascalCase types
fn load_config();           // snake_case functions
const MAX_RETRIES: u32 = 3; // SCREAMING_SNAKE constants
let file_path: PathBuf;     // snake_case variables
```
