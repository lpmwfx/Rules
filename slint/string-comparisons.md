---
tags: [strings, string-comparison, constants, zero-literals]
concepts: [string-state-comparisons, strings-global]
requires: [slint/states.md]
related: [slint/globals.md, slint/create-before-use.md]
keywords: [Strings, string-comparison, kind-dialogue, kind-panel, mode-edit, mode-view, tab-general, tab-settings, global, constant]
layer: 3
---
# Slint String State Comparisons

> All string comparisons must reference Strings.* constants — never bare string literals

---

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

RESULT: All string discriminators have a single source — rename in one place, updates everywhere
REASON: A typo in a string literal is a silent bug — a missing Strings.* property is a compile error
