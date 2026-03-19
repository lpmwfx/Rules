---
tags: [workflow, violations, scanning, understanding, repair]
concepts: [violation-fixing, scanner-output, decision-tree]
keywords: [violations, groups, repair, scan-output, mother-child, literals, safety, hygiene, topology, purity]
layer: 3
requires: [workflow/always-compliant.md, workflow/coding-discipline.md]
feeds: [workflow/commit-clean.md]
related: [global/mother-tree.md, global/config-driven.md, global/file-limits.md, global/topology.md, rust/errors.md]
---

# DURING/VERIFY: Read Violations and Fix

## Goal

Understand what violations mean.
Fix them in the right order.
Use violations as learning.

---

## The 6 Violation Groups

When `scan_file()` or `check_staged()` returns violations, they are grouped by rule category.
Each group has a different root cause and fix strategy.

### Group 1: TOPOLOGY

**What it means:** Layer violation — importing from disallowed layer, or type in wrong place.

**Rule file:** `global/topology.md`

**Q&A:**
- Does import respect layer rules? (Check allowed imports for your layer)
- Is type in correct module? (core → core/, shared → shared/)
- Does public type have correct suffix? (_core, _adp, _x, etc.)

**Fix strategy:**
1. Identify the import or type causing violation
2. Check `global/topology.md` — what's allowed for THIS layer?
3. Either: move type to correct layer, OR remove import, OR restructure
4. Re-scan

**Example violation:**
```
TOPOLOGY/layer-violation: src/core/engine.rs:12
  Cannot import from adapter — core layer allows: pal, shared
  Import: use crate::adapter::Router
```

**Fix:**
```rust
// Move Router access through pal layer instead
use crate::pal::PalInterface;
```

---

### Group 2: MOTHER-CHILD

**What it means:** Function has too many child functions (mother function problem) OR function is defined inline instead of named.

**Rule file:** `global/mother-tree.md`

**Q&A:**
- Does function have more than 3-4 child functions?
- Should child functions be named and in same module?
- Is code nesting too deep?

**Fix strategy:**
1. Extract child function to module level (make it named)
2. OR split function into multiple functions (mother → smaller functions)
3. OR delegate to sub-module
4. Re-scan

**Example violation:**
```
MOTHER-CHILD/fn-definitions: src/core/parser.rs:45
  Too many nested functions (7 definitions at depth 3)
  Mother function: parse_expression
```

**Fix:**
```rust
// Before: one huge parse_expression with 7 helpers
// After: parse_expression calls parse_term, parse_factor, parse_operand, etc.
// Each helper is a named function at module level
```

---

### Group 3: SAFETY

**What it means:** Unsafe pattern detected — `.unwrap()`, `expect()`, `panic!()`, unsafe code, etc.

**Rule file:** Depends on language:
- Rust: `rust/errors.md`
- Slint: `slint/states.md`
- Python: `python/boundary-check.md`

**Q&A:**
- Is this `.unwrap()` in non-test code? (Should use `?` instead)
- Is this in code that can fail? (Result type, not panic)
- Is there proper error handling?

**Fix strategy:**
1. Change `.unwrap()` → `?` (propagate error)
2. OR wrap in Result type
3. OR only use in test code / main function setup
4. Re-scan

**Example violation:**
```
SAFETY/no-unwrap: src/core/engine.rs:23
  .unwrap() in non-test code
  let config = load_config().unwrap();
```

**Fix:**
```rust
// Change to error propagation
let config = load_config()?;
// Function return type must be Result
fn setup() -> Result<Config, ConfigError> { }
```

---

### Group 4: HYGIENE

**What it means:** Code cleanliness — file too large, too much nesting, unused imports, etc.

**Rule file:** `global/file-limits.md`, `global/nesting.md`

**Q&A:**
- Is file too large? (Split into modules)
- Is nesting too deep? (Extract to function)
- Are there unused imports? (Remove them)

**Fix strategy:**
1. If file too large → split into sub-modules
2. If nesting too deep → extract to named function
3. Remove unused imports / dead code
4. Re-scan

**Example violation:**
```
HYGIENE/file-limits: src/core/engine.rs:1
  File too large: 310 lines (max: 300)
  Split into: src/core/engine_*.rs
```

**Fix:**
```bash
# Create new module
# Move ~50 lines of related code
# Update imports
# File now ~250 lines ✓
```

---

### Group 5: TOPOLOGY/PURITY

**What it means:** Layer contamination — shared layer has internal dependencies, or pal layer imports from wrong place.

**Rule file:** `global/topology.md` (layer rules)

**Q&A:**
- Is shared/ importing from another internal layer? (Should not)
- Is pal/ importing from non-shared? (Should not)
- Is adapter importing something it shouldn't? (Check rules)

**Fix strategy:**
1. Remove import from disallowed layer
2. Pass dependency as parameter instead
3. OR move code to correct layer
4. Re-scan

**Example violation:**
```
TOPOLOGY/shared-guard: src/shared/config.rs:5
  shared/ cannot import internal layers
  Import: use crate::core::Engine
```

**Fix:**
```rust
// Remove import from core
// Inject Engine as parameter instead
fn process(engine: &dyn MyTrait) -> Result { }
```

---

### Group 6: LITERALS & CONSTANTS

**What it means:** Magic numbers, hardcoded strings, or zero-literal usage without named constant.

**Rule file:** `global/config-driven.md`, `rust/constants.md`

**Q&A:**
- Is this a hardcoded number/string? (Should be named constant)
- Is this a timeout/duration? (Name it: TIMEOUT_MS)
- Is this a threshold? (Name it: MAX_RETRIES)

**Fix strategy:**
1. Define named constant at module/file top
2. Replace literal with constant name
3. Re-scan

**Example violation:**
```
LITERALS/no-magic-number: src/core/engine.rs:45
  Magic number: 5000
  Define as: const TIMEOUT_MS: u64 = 5000;
```

**Fix:**
```rust
const TIMEOUT_MS: u64 = 5000;

let remaining = TIMEOUT_MS - elapsed;
```

---

## Violation Priority: Fix in This Order

When you have multiple violations, fix in this order:

```
1. TOPOLOGY         — layer violations (structural issue)
2. MOTHER-CHILD     — function design (refactoring)
3. SAFETY           — error handling (correctness)
4. HYGIENE          — code cleanliness (maintainability)
5. LITERALS         — magic numbers (configuration)
```

**Why this order?**
- TOPOLOGY first: Structure must be correct before everything else
- MOTHER-CHILD second: Function design impacts error handling below
- SAFETY third: Errors must propagate correctly
- HYGIENE fourth: Clean code is easier to understand
- LITERALS last: Named constants are nice, but least critical

---

## Workflow: Understand and Fix

### Step 1: Read the violation group header

```
TOPOLOGY/layer-violation: src/core/engine.rs:12
  Cannot import from adapter — core layer allows: pal, shared
```

### Step 2: Ask the Q&A questions

Q: Am I importing from an allowed layer?
A: No. core can only import pal, shared. I imported adapter. ❌

### Step 3: Call get_rule() for the rule file

```
get_rule("global/topology.md")
```

Read the relevant section. Understand the rule.

### Step 4: Fix the violation

Apply the fix strategy for this group.

### Step 5: Re-scan

```
scan_file("src/core/engine.rs")
```

Confirm violation is gone.

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Blocks commit, must fix | Fix now |
| WARN | Noted, doesn't block | Fix during next sprint (or ignore if justified) |
| INFO | FYI | Reference only |

**Only [ERROR] violations block commits.**
`check_staged()` will prevent commit if [ERROR] violations exist in staged code.

---

## FAQ

**Q: Why fix in that specific order?**

A: Topology issues affect everything else. If structure is wrong, fixing other issues is harder.
Once structure is right, errors/hygiene/literals are straightforward.

**Q: What if I have 10 violations?**

A: Group them by category. Fix TOPOLOGY first (maybe 2-3), then MOTHER-CHILD, etc.
Usually: 5-10 violations → 3-4 groups.

**Q: Should I fix all violations before committing?**

A: Only [ERROR] violations block commits. [WARN] violations don't.
But fixing them is better than deferring.

**Q: What if I don't understand a violation?**

A: Call `get_rule(file)` for the relevant rule file. Read the rule.
If still unclear, check `workflow/always-compliant.md` for MCP tools to get help.

---

## Glossary

- **Violation:** Code that violates a rule
- **[ERROR]:** Must fix, blocks commit
- **[WARN]:** Should fix, doesn't block
- **[INFO]:** Nice to know
- **Group:** Category of violations (TOPOLOGY, SAFETY, etc.)
- **Rework loop:** Write → scan → fix → re-scan (N iterations)

---

## Next: VERIFY Phase

Read `workflow/commit-clean.md` for pre-commit gate enforcement.
