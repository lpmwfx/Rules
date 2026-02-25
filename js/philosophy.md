---
tags: [javascript, philosophy, design-principles]
concepts: [design-principles, approach]
related: [global/consistency.md]
layer: 4
---
# Philosophy

> Pure JavaScript ES2024+ with TypeScript-level safety

---

RULE: Pure JavaScript (ES2024+) with TypeScript-level safety
RULE: No .ts files — JSDoc + TypeScript CLI for type checking
RULE: Runtime validation at boundaries (Zod/Valibot)
RULE: Zero build step for type safety

## The Stack

```
JSDoc Types     → Static type checking (design time)
TypeScript CLI  → Type verification (build time)
ESLint          → Code quality + type-aware rules
Zod/Valibot     → Runtime validation (execution time)
Prettier        → Consistent formatting
```

## Why This Beats TypeScript

ADVANTAGE: No build step required
ADVANTAGE: Native debugging (no source maps)
ADVANTAGE: Smaller bundles (native ES2024)
ADVANTAGE: Same error messages (uses tsc)
ADVANTAGE: Runtime validation included (Zod)
ADVANTAGE: Standard JS — lower learning curve
