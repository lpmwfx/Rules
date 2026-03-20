---
tags: [create-before-use, workflow, tokens, state-files, zero-literals]
concepts: [create-before-use, slint-token-workflow]
requires: [slint/states.md, uiux/tokens.md]
related: [slint/globals.md, slint/themes.md]
keywords: [create-before-use, workflow, token, state, sizes, durations, view-states, strings, globals, theme, populate]
layer: 3
---
# Slint Create-Before-Use Workflow

> State globals start empty — YOU populate them as you build components

---

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

RESULT: Every value has a named source before it is used — no orphaned literals
REASON: Writing the literal "temporarily" always becomes permanent — the scanner catches it


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
