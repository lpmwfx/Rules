---
tags: [slint, states, state-files, constants, enums, no-hardcoding, zero-literals, slintscanners, create-before-use]
concepts: [state-files, state-folder, zero-literals, named-constants, data-driven, slint-build-scan, create-before-use, workflow, string-comparison]
requires: [slint/validation.md, slint/themes.md, uiux/tokens.md]
feeds: [slint/globals.md, slint/init.md]
related: [slint/component-model.md, global/config-driven.md, uiux/state-flow.md, slint/init.md, rust/constants.md, uiux/tokens.md]
keywords: [state, states, enum, constant, hardcoded, variable, state-folder, Sizes, Durations, ViewStates, Strings, slintscanners, build-scan, cargo-scan, create-before-use, workflow, create-token, string-comparison]
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

## Create-Before-Use Workflow

VITAL: State globals start empty — YOU populate them as you build components.
VITAL: When you need a value, create the token FIRST, then reference it.

```
Before writing ANY value in a .slint component:

1. IDENTIFY where the value belongs:
   - Color, spacing, visual effect → globals/theme/  (see uiux/tokens.md)
   - Size, percentage, divisor     → state/sizes.slint
   - Animation duration            → state/durations.slint
   - View/navigation enum          → state/view-states.slint
   - Text label, discriminator     → globals/strings.slint

2. SEARCH the target file for an existing token
   - Need 100%?  → search Sizes for "full"
   - Need 240px? → search Sizes for "sidebar-width"
   - Need 200ms? → search Durations for "slide"

3. Token EXISTS → reference it:  Sizes.full, Durations.slide

4. Token does NOT EXIST →
   a. OPEN the state/global file (e.g. ui/state/sizes.slint)
   b. ADD:  out property <length> sidebar-width: 240px;
   c. SAVE the file
   d. THEN use Sizes.sidebar-width in your component

5. NEVER write the literal in the component — not even as a placeholder
```

RULE: The developer creates state tokens — they are not pre-populated
RULE: "Token not found" means "create it now" — not "use the literal instead"

## String State Comparisons

VITAL: All string comparisons in .slint must reference Strings.* constants — never bare string literals

```slint
// globals/strings.slint
export global Strings {
    out property <string> kind-dialogue:  "dialogue";
    out property <string> kind-panel:     "panel";
    out property <string> mode-edit:      "edit";
    out property <string> mode-view:      "view";
    out property <string> tab-general:    "general";
    out property <string> tab-settings:   "settings";
}
```

```slint
// BANNED:  root.kind == "dialogue"
// CORRECT: root.kind == Strings.kind-dialogue

// BANNED:  if active-tab == "settings" { ... }
// CORRECT: if active-tab == Strings.tab-settings { ... }
```

RULE: Create the string constant in Strings global FIRST, then reference it
RULE: State discriminators (kind-*, mode-*, tab-*) always go in Strings
BANNED: `== "any-string-literal"` in component code — use Strings.* constant

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

## Why — Data-Driven Paradigm

This is not cosmetic. It is an architectural separation: **data vs. structure**.

Components are structure — they describe WHAT exists and HOW it is arranged.
State files are data — they hold every concrete value (sizes, durations, enums, strings).

```
WITHOUT state files:
  Rectangle { width: 240px; animate x { duration: 200ms; } }
  → Component mixes structure and data. Values are trapped in layout code.

WITH state files:
  Rectangle { width: Sizes.sidebar-width; animate x { duration: Durations.slide; } }
  → Component is pure structure. All concrete values live in state/ files.
  → Change Sizes.sidebar-width in ONE place → every sidebar updates.
```

The state files are the data layer. The components are declarative consumers of that data. This is what makes the system dynamic — swap the data (different sizes, different durations) and the UI changes without touching a single component.

Same principle in Rust: `state/` modules hold all concrete values → function bodies are declarative expressions. See [rust/constants.md](../rust/constants.md).

RESULT: Every value has a named source — the entire UI is data-driven and declarative
REASON: The scanner catches ANY literal in a component as ERROR — the paradigm is enforced, not optional
