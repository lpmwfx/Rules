---
tags: []
concepts: [javascript-rules]
requires: [global/module-tree.md]
related: [js/modules.md, js/jsdoc.md, js/validation.md, js/safety.md, js/eslint.md, js/testing.md, js/philosophy.md, js/typescript-cli.md, js/project-structure.md, global/module-tree.md, uiux/state-flow.md, uiux/mother-child.md, php/laravel/stack-svelte.md]
layer: 6
---
# JavaScript Rules (TS-like-JS)

> Pure JavaScript with TypeScript-level safety — zero build step

---

## Philosophy

RULE: One module per file — nesting = folder of files, not nested function closures
RULE: Stateless modules — all app state in a central state object; modules transform, never store
RULE: Encapsulate behind explicit exports — nothing public unless in the module's export list
RULE: UI components receive props and emit events — they own no state

See: [global/module-tree.md](../global/module-tree.md) | [uiux/state-flow.md](../uiux/state-flow.md)

## Files

| File | Topic |
|------|-------|
| [philosophy.md](philosophy.md) | TS-like-JS, zero build step |
| [modules.md](modules.md) | ESM, closed modules, encapsulation |
| [jsdoc.md](jsdoc.md) | JSDoc type annotations |
| [typescript-cli.md](typescript-cli.md) | tsc + jsconfig.json |
| [eslint.md](eslint.md) | ESLint flat config |
| [validation.md](validation.md) | Zod/Valibot runtime validation |
| [testing.md](testing.md) | Node.js test runner |
| [project-structure.md](project-structure.md) | Package.json, scripts, structure |
| [quick-ref.md](quick-ref.md) | Quick reference table |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
