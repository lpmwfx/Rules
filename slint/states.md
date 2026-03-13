---
tags: [slint, states, state-files, constants, enums, no-hardcoding, zero-literals, slintscanners]
concepts: [state-files, state-folder, zero-literals, named-constants, data-driven, slint-build-scan]
requires: [slint/validation.md, slint/themes.md]
feeds: [slint/globals.md, slint/init.md]
related: [slint/component-model.md, global/config-driven.md, uiux/state-flow.md, slint/init.md]
keywords: [state, states, enum, constant, hardcoded, variable, state-folder, Sizes, Durations, ViewStates, slintscanners, build-scan, cargo-scan]
layer: 3
---
# Slint State Files — Zero Literals in UI

> All hard values live in `state/` files. Components contain zero literals. Themes in `globals/theme/`.

---

VITAL: Any number in a component file is hardcoding — every value is a variable reference
VITAL: All hard state values (enums, constants, sizes, durations) live in `ui/state/` files
VITAL: Zero exemptions — `0px`, `1px`, `100%`, `200ms`, `0`, `2` are ALL hardcoded values
RULE: One state file per concern — never dump all constants in one file
RULE: Only `true`/`false` (boolean keywords) are allowed as literals in components
RULE: Themes are the ONE exception — theme tokens live in `ui/globals/theme/` (see slint/themes.md)
BANNED: ANY number in a component — integers, floats, px, %, ms, all of it
BANNED: `0px` — use `Sizes.zero`. `1px` — use `Sizes.hairline`. `100%` — use `Sizes.full`
BANNED: `200ms` — use `Durations.slide`. `/ 2` — use `/ Sizes.half-divisor`
BANNED: `0`, `1`, `2` as state values — use `ViewStates.nav-home`

## Slint Syntax Exceptions (3 total)

Three constructs REQUIRE literals — the compiler rejects property references:

| Construct | Reason | Example |
|-----------|--------|---------|
| `GridLayout` `row:` / `col:` | Compile-time constant | `col: 0;` |
| `@image-url("...")` | Compile-time string | `@image-url("icons/home.svg")` |
| `@tr("...")` template | Compile-time string | `@tr("Save {}", name)` |

RULE: These three are the ONLY allowed literals. The scanner exempts them automatically.

## Folder Structure

```
ui/state/
├── view-states.slint           ← navigation/view enums
├── sizes.slint                 ← fixed sizes, percentages, divisors
├── durations.slint             ← animation timings
└── limits.slint                ← max counts, thresholds
```

## State File Pattern

```slint
// ui/state/sizes.slint
export global Sizes {
    out property <length>  zero:           0px;
    out property <length>  hairline:       1px;
    out property <length>  full:           100%;
    out property <float>   half-divisor:   2;
    out property <length>  sidebar-width:  240px;
}

// ui/state/durations.slint
export global Durations {
    out property <duration> fade-in:       150ms;
    out property <duration> slide:         200ms;
}

// ui/state/view-states.slint
export global ViewStates {
    out property <int> nav-home:     0;
    out property <int> nav-settings: 1;
}
```

## What Goes Where

| Value type | Location | Example |
|------------|----------|---------|
| Colors, spacing, effects | `globals/theme/` | `Colors.bg-primary` |
| View/navigation enums | `state/` | `ViewStates.nav-home` |
| Animation durations | `state/` | `Durations.fade-in` |
| Fixed sizes, divisors | `state/` | `Sizes.sidebar-width` |
| Localization strings | `globals/strings.slint` | `Strings.save` |

RULE: "Is this visual identity?" → `globals/theme/`. Otherwise → `state/`.

RESULT: Every value has a named source — stateless, data-driven, zero-literal UI
REASON: The scanner catches ANY literal in a component as ERROR — making the architecture enforceable
