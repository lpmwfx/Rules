---
tags: [javascript, typescript, type-checking, jsconfig]
concepts: [type-checking, jsconfig]
related: [js/jsdoc.md, js/eslint.md]
keywords: [tsc, jsconfig, check-js]
layer: 4
---
# TypeScript CLI

> Type checking only — never transpile

---

CONFIG: `jsconfig.json` (not tsconfig.json)
COMMAND: `npx tsc --project jsconfig.json`
FLAG: `--noEmit` (never transpile)
FLAG: `--checkJs` (check .js files)
FLAG: `--strict` (all strict options)

## jsconfig.json (Required Settings)

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "checkJs": true,
    "strict": true,
    "noEmit": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": ["src/**/*.js"],
  "exclude": ["node_modules"]
}
```
