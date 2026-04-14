---
tags: [sid, code-hygiene, mutables, constants, build-time, categorical]
concepts: [code-hygiene, zero-literals, build-time-data, resolver, canonical-source]
requires: [sid-architecture/sid-identity.md]
feeds: [sid-architecture/working-in-data.md]
related: [global/data-driven-ui.md, rust/constants.md, js/constants.md, deprecated/persistent-state.md, deprecated/config-driven.md, deprecated/app-model.md]
keywords: [mutable, literal, hardcoded, symbols-json, config-toml, resolver, build-time, categorical, SID, zero-literal, anti-pattern]
layer: 1
binding: false
status: prototype
---
# Code Free of Mutables — Principle 02

> Source code contains no mutable values. All constants, labels, thresholds, defaults, colors, paths and URLs are SIDs. Coverage is categorical.
>
> **Supersedes (prototype):** `deprecated/persistent-state.md`, `deprecated/config-driven.md`, state isolation rules in `deprecated/app-model.md`

---

## How Principle 02 Relates to Principle 03

"Data" does not mean the same thing in both principles. Principle 02 is categorical: everything in source code gets a SID, no exceptions. Principle 03 is selective: only what needs to vary at runtime lives in the datastore. Same mechanics, different scope, different timing.

| | Principle 02 (this file) | Principle 03 |
|---|---|---|
| Scope | Everything in source code | Only what must vary at runtime |
| Coverage | Consistent, categorical | Selective, architecture-determined |
| Where SID records live | File in the repo | Live datastore |
| Read at | Build-time | Runtime |
| Change requires | Rebuild | Nothing |

A SID can start as a build-time constant (Principle 02) and move to a runtime datastore (Principle 03) without changing identity. Code using it does not change — only the resolver layer switches.

The four combinations:

| | Principle 02 no | Principle 02 yes |
|---|---|---|
| **Principle 03 no** | Traditional app | Well-organized monolithic app |
| **Principle 03 yes** | Messy engine with magic numbers | **The goal: clean engine + live data** |

---

VITAL: Principle 02 is categorical — everything addressable is a SID, no exceptions
VITAL: Data records live in files in the repo and are read at build time
RULE: All strings, numbers with domain meaning, colors, fonts, URLs, paths, defaults are SIDs
RULE: The data file is one canonical source — code accesses it only through the resolver layer
RULE: Resolver function is named consistently across the codebase (`resolve()`, `sym()`, `$()`)
RULE: Validation at build: every SID in code exists as a record, every record is referenced, types match
BANNED: Literal values in function bodies that carry domain meaning
BANNED: "Too small to deserve a SID" — padding of 8px is a SID
BANNED: Defaults in declarations (`let timeout = 5000`)
BANNED: Strings in comparisons (`if theme == "dark"`)
BANNED: Enum values defined in code that represent domain states

## What Is a SID

- Strings visible to the user (labels, error messages, tooltips)
- Numbers with domain meaning (thresholds, limits, timeouts)
- Colors, fonts, sizes, padding, margins
- URLs, paths, endpoint names
- Default values, enum values, feature flags

## What Is NOT a SID

- Control flow (if, loops, function calls)
- Types and structures
- Algorithms and transformations
- Operators (`*`, `+`, `>`, `&&`)

## Anti-Patterns

### Defaults in declarations
```rust
let timeout = 5000;  // VIOLATION — hardcoded
```

### Small numbers
```rust
const limit = threshold * 2;  // VIOLATION — "2" is a literal
// Fix:
let multiplier = resolve(fP8qW4);
let limit = threshold * multiplier;
```

### Strings in comparisons
```rust
if theme == "dark" { ... }  // VIOLATION — "dark" is hardcoded
```

### Contaminated local bindings
```typescript
const base = resolve(aK3qP9);
const result = base + 10;  // VIOLATION — "10" is a literal, entire chain contaminated
```

## The Resolver Layer

One and only one way to read SIDs. The function becomes a hotspot for cache, tooling and type checks. In Principle 02 it can be a function reading JSON loaded at build. In Principle 03 it is runtime infrastructure — but the contract is the same.

## What It Gives

- One canonical location per value — no duplicates
- Refactoring becomes trivial — change one place
- Code shows structure; data shows content
- AI conversation can work in isolation on data files
- Foundation for Principle 03 — SIDs can move to runtime without identity change


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
