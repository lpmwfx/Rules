---
tags: [combo, js, web, css, uiux]
concepts: [quick-ref, project-type]
keywords: [javascript, web, pwa, components, css, topology]
requires: [global/quick-ref.md, js/quick-ref.md, css/quick-ref.md, web/topology.md, uiux/components.md]
layer: 6
binding: true
---
# Quick Reference: JavaScript Web Project

> WA/PWA web application with JS + CSS. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | JS: 250 lines, CSS: 150 lines. Split into child files | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — config loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## JavaScript rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | Pure JS + JSDoc + tsc — no .ts files | [js/jsdoc.md](../js/jsdoc.md) |
| Modules | ESM only, `"type": "module"`, file extensions required | [js/modules.md](../js/modules.md) |
| Encapsulation | Modules are CLOSED, `#` for private fields | [js/modules.md](../js/modules.md) |
| Types | JSDoc `@type`, `@param`, `@returns` | [js/jsdoc.md](../js/jsdoc.md) |
| Validation | Zod/Valibot at boundaries | [js/validation.md](../js/validation.md) |
| Testing | `node:test` + `node:assert/strict` | [js/testing.md](../js/testing.md) |

## CSS rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | Vanilla CSS, no frameworks | [css/cascade.md](../css/cascade.md) |
| Separation | Layout files: ZERO colors. Theme files: ONLY colors | [css/cascade.md](../css/cascade.md) |
| Tokens | `--color-bg-1/2/3`, `--color-text-1/2/3`, `--shadow-1/2/3` | [css/tokens.md](../css/tokens.md) |
| Themes | Light on `:root`, dark on `[data-theme="dark"]` | [css/themes.md](../css/themes.md) |
| Naming | BEM-inspired: `.block-element--modifier` | [css/naming.md](../css/naming.md) |

## UI/UX rules (Web Components)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Components | One file per component, stateless, state-in events-out | [uiux/components.md](../uiux/components.md) |
| Mother-child | AppShell is mother — views are stateless children | [web/mother-child.md](../web/mother-child.md) |
| State flow | State-in from Adapter, CustomEvents out | [uiux/state-flow.md](../uiux/state-flow.md) |
| Web Components | Custom elements, Shadow DOM, template | [web/components.md](../web/components.md) |

## Project layout (6-layer web topology)

```
src/
├── ui/           ← views, components, Web Components (_ui)
│   ├── views/    ← screen-level components (stateless)
│   ├── widgets/  ← reusable components (stateless)
│   └── shell.js  ← mother component (AppShell)
├── adapter/      ← ViewModel, event routing, state store (_adp)
├── core/         ← pure business logic (_core)
├── gateway/      ← fetch, localStorage, IndexedDB (_gtw)
├── pal/          ← Web API abstractions (_pal)
└── shared/       ← errors, result types (_x)
```

See [web/topology.md](../web/topology.md) for full ESM import rules and boot order.

## Verification

| Gate | Tools |
|------|-------|
| Local | `tsc --noEmit --checkJs`, `eslint`, `prettier`, Stylelint |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all JS + CSS checks |

## BANNED

- `.ts` files — use JSDoc + `jsconfig.json`
- `var`, `require()`, `module.exports`
- `console.log` in production, `eval()`
- `!important`, ID selectors, Tailwind/Bootstrap
- Hardcoded color values outside theme files
- UI importing Core directly
- Core importing UI, Adapter, or Gateway
- Files over their type's line limit
- Deep nesting (4+ levels)
- `utils/`, `helpers/`, `lib/` folders
- Non-English code, comments, or identifiers

## Project files

Every project has `proj/` — see [project-files/](../project-files/) for formats:
PROJECT, TODO, FIXES, RULES, PHASES, `rulestools.toml`


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
