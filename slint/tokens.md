---
tags: [tokens, design-tokens, no-hardcoding, globals, zero-literals]
concepts: [slint-token-globals, slint-design-tokens]
requires: [uiux/tokens.md, uiux/token-structure.md]
feeds: [slint/themes.md, slint/globals.md]
related: [slint/states.md, uiux/token-switching.md]
keywords: [Colors, Spacing, Type, global, out-property, slint-global, token, theme, zero-literal]
layer: 3
---
# Slint Token Implementation

> Token globals in Slint — `out property` values, zero literals in components

---

```slint
// tokens/colors.slint
export global Colors {
    out property <color> bg-primary:   #1a1a1a;
    out property <color> bg-surface:   #2d2d2d;
    out property <color> text-primary: #f0f0f0;
    out property <color> text-muted:   #888888;
    out property <color> accent:       #4a90d9;
}

// tokens/spacing.slint
export global Spacing {
    out property <length> xs:  4px;
    out property <length> sm:  8px;
    out property <length> md:  16px;
    out property <length> lg:  24px;
    out property <length> xl:  48px;
}

// tokens/typography.slint
export global Type {
    out property <length>  body-size:    14px;
    out property <length>  heading-size: 22px;
    out property <int>     body-weight:  400;
    out property <int>     bold-weight:  700;
}

// tokens/theme.slint — re-exports everything
export { Colors, Spacing, Type } from "colors.slint";
// (import from spacing.slint, typography.slint, etc.)
```

```slint
// Component uses tokens — ZERO literal values
import { Colors, Spacing, Type } from "../tokens/theme.slint";

component PrimaryButton inherits Rectangle {
    background: Colors.accent;             // token
    border-radius: Spacing.xs;            // token

    Text {
        font-size: Type.body-size;         // token
        color: Colors.bg-primary;          // token
        padding: Spacing.sm;               // token
    }
}

// BANNED — literals scattered in component
component PrimaryButton inherits Rectangle {
    background: #4a90d9;     // BANNED
    border-radius: 4px;      // BANNED
    Text { font-size: 14px; color: #1a1a1a; padding: 8px; }  // BANNED
}
```

RESULT: All Slint values live in token globals — components are pure structure
REASON: The scanner catches ANY literal in a component as ERROR — the paradigm is enforced
