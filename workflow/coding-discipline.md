---
tags: [workflow, during, discipline, naming, sizing, errors]
concepts: [proactive-compliance, code-quality, naming, error-handling]
keywords: [discipline, topology, naming, constants, booleans, sizing, unwrap, magic-numbers, errors]
layer: 2
requires: [global/topology.md, global/file-limits.md, workflow/load-context.md]
feeds: [workflow/read-violations.md]
related: [rust/naming.md, rust/errors.md, rust/types.md, workflow/always-compliant.md]
---

# DURING: Coding Discipline

## Goal

Write code that is correct by design.
Violations become rare, not routine.

---

## 1. Topology Awareness While Coding

### Rule: Import only allowed layers

Check the import rules BEFORE you type the import statement.

From `global/topology.md`:
```
core    → pal, shared
adapter → core, gateway, pal, ui, shared
gateway → pal, shared
pal     → shared
shared  → nothing
```

**Bad (cycle):**
```rust
// core/engine.rs
use crate::adapter::Router;  // ❌ core can't import adapter
```

**Good:**
```rust
// core/engine.rs
use crate::pal::FileSystem;  // ✓ core can import pal
use crate::shared::Config;   // ✓ core can import shared
```

**Prevention:** Know the rules BEFORE importing. Never guess.

### Rule: Type suffix matches layer

Public types must carry layer suffix (from `global/topology.md`):

```
_core  — types from core/
_adp   — types from adapter/
_gtw   — types from gateway/
_pal   — types from pal/
_x     — types from shared/
_ui    — types from ui/
```

**Bad:**
```rust
// src/core/engine.rs
pub struct Engine { }  // ❌ missing _core suffix
```

**Good:**
```rust
// src/core/engine.rs
pub struct Engine_core { }  // ✓ suffix matches layer
```

**Override suffixes allowed (use sparingly):**
```
_sta   — static/stateless
_cfg   — configuration
_test  — test helper
```

**Prevention:** When defining `pub struct`, add suffix immediately.

---

## 2. Naming Discipline

### Constants: Always named

**Rule:** No magic numbers. Every constant gets a name.

**Bad:**
```rust
let timeout = 5000;  // ❌ magic number
```

**Good:**
```rust
const TIMEOUT_MS: u64 = 5000;
```

**Why:** Magic numbers don't explain themselves.
Named constants are self-documenting.

**Prevention:** Before typing a literal, ask: "Does this need a name?"
If yes (and it usually does) → define the constant first.

### Booleans: Correct prefix

**Rule:** Boolean names start with `is_`, `has_`, `can_`, `should_`.

| Prefix | Meaning | Example |
|--------|---------|---------|
| `is_` | state of being | `is_active`, `is_empty` |
| `has_` | possession | `has_permission`, `has_children` |
| `can_` | capability | `can_edit`, `can_delete` |
| `should_` | recommendation | `should_retry`, `should_warn` |

**Bad:**
```rust
let active = true;         // ❌ unclear
let user_count = 5;        // ❌ unclear if this is boolean
```

**Good:**
```rust
let is_active = true;      // ✓ clear
let has_children = true;   // ✓ clear
```

**Prevention:** When naming a boolean, use one of the 4 prefixes.

### Functions: No noise names

**Rule:** Function names describe what they do, not that they do something.

**Bad:**
```rust
fn do_thing() { }           // ❌ what thing?
fn helper() { }             // ❌ helper for what?
fn process() { }            // ❌ what are we processing?
```

**Good:**
```rust
fn validate_input() { }     // ✓ clear
fn fetch_user() { }         // ✓ clear
fn apply_discount() { }     // ✓ clear
```

**Prevention:** Before naming a function, ask: "Could someone understand this name in isolation?"

---

## 3. Size Discipline

### Rule: Count lines mentally, split BEFORE you hit the limit

File size limits (from `global/file-limits.md`):
- **Rust:** 300 lines → split at 240 lines (80%)
- **Python:** 250 lines → split at 200 lines (80%)
- **JavaScript:** 250 lines → split at 200 lines (80%)

**Prevention:** As you write, keep a rough line count.

```rust
// src/core/engine.rs — ~80 lines so far
// Adding 50 more lines of new feature...
// Now ~130 lines. ✓ Safe.

// vs.

// src/core/engine.rs — ~240 lines (80% of 300)
// Need to add 50 lines of new feature...
// ❌ File is at limit. STOP. Create new module in core/ first.
```

**Split strategy:**
1. Create new module in SAME layer (e.g., `src/core/parser.rs`)
2. Move appropriate code from existing file
3. Update imports in existing file
4. Now you have room for new code

**Prevention:** Never code into a full file. Split first.

---

## 4. Constant Discipline

### Rule: Hardcoded values should be named

**Bad:**
```rust
if error_count > 5 {  // ❌ what is 5?
    panic!("too many errors");
}
```

**Good:**
```rust
const MAX_ERROR_THRESHOLD: usize = 5;

if error_count > MAX_ERROR_THRESHOLD {  // ✓ clear intent
    return Err(/* error */);
}
```

**Hardcoded values to avoid:**
- Duration literals: `5000` → `const TIMEOUT_MS`
- Path strings: `"/etc/config"` → `const CONFIG_PATH`
- URLs: `"http://example.com"` → `const DEFAULT_SERVER`
- Numeric thresholds: `10`, `100`, `1000` → named const

**Prevention:** Before typing a literal, name it.

---

## 5. Error Handling Discipline

### Rule: Use `?` and Result types, never `.unwrap()`

**Bad:**
```rust
let config = load_config().unwrap();  // ❌ panics if fails
```

**Good:**
```rust
let config = load_config()?;          // ✓ propagates error
```

**Bad:**
```rust
fn process() -> i32 {
    let value = risky_operation().expect("should work");  // ❌ panics
    value
}
```

**Good:**
```rust
fn process() -> Result<i32, MyError> {
    let value = risky_operation()?;   // ✓ Result type
    Ok(value)
}
```

**Rule from `rust/errors.md`:**
- `.unwrap()` allowed ONLY in:
  - Test code (testing framework, #[cfg(test)])
  - Examples (doc comments)
  - Main function setup (before actual work)
- Never in library code or core logic

**Prevention:** When you see `.unwrap()` in production code, use `?` instead.

### Rule: No stringly-typed matches

**Bad:**
```rust
match error_type.as_str() {
    "connection" => { /* */ },  // ❌ string-based dispatch
    "timeout" => { /* */ },
    _ => { }
}
```

**Good:**
```rust
match error {
    MyError::Connection => { /* */ },  // ✓ enum-based dispatch
    MyError::Timeout => { /* */ },
    _ => { }
}
```

**Prevention:** Define enums first. Dispatch on types, not strings.

---

## 6. Scanning During Development

### Rule: Run `scan_file()` after each logical edit

**Optional but recommended:** After each function or module, call:

```
scan_file("src/core/engine.rs")
```

The MCP tool returns violations immediately.

**If violations found:**
1. Read the violation group (TOPOLOGY, MOTHER-CHILD, SAFETY, etc.)
2. Call `get_rule(file)` to understand the rule
3. Fix the violation immediately
4. Re-scan to confirm

**Why:** Catch violations while they're fresh in your mind.
Rework loops are cheaper now than after you finish the entire file.

**PostToolUse hook:** The Edit/Write tools automatically run `scan_file()`.
If you see violations in hook output, handle them immediately.

---

## DURING-Phase Checklist

- [ ] Topology aware? (Imports from allowed layers only)
- [ ] Type suffixes correct? (_core, _adp, _x, etc.)
- [ ] All constants named? (No magic numbers)
- [ ] Boolean names correct? (is_, has_, can_, should_)
- [ ] Function names clear? (Not do_thing, helper)
- [ ] File size tracked? (Splitting at 80%?)
- [ ] Error handling correct? (? over .unwrap())
- [ ] No stringly-typed code? (Enums, not strings)
- [ ] Running scan_file() occasionally? (Optional but recommended)

---

## FAQ

**Q: Should I follow all of these at once?**

A: Start with topology + naming + errors (critical).
Gradually add sizing + constants discipline.
Master them together over time.

**Q: What if I make a mistake?**

A: scan_file() will catch it. Fix and move on.
The goal is to make violations rarer, not impossible.

**Q: Do I need scan_file() during development?**

A: No, but it accelerates learning. First few times: yes.
Once habits form: optional (pre-commit gate is enough).

---

## Next: VERIFY Phase

Read `workflow/commit-clean.md` for pre-commit discipline.
Read `workflow/read-violations.md` to understand scanner violations.
