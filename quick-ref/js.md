---
tags: [combo, js]
concepts: [quick-ref, project-type]
keywords: [javascript, esm, jsdoc, node]
requires: [global/quick-ref.md, js/quick-ref.md]
layer: 6
binding: true
---
# Quick Reference: JavaScript Project

> JavaScript CLI, library, or Node.js service. All rules at a glance with links to full docs.

---

## Foundation — global rules (always apply)

| Rule | Key point | Full doc |
|------|-----------|----------|
| Language | English only — code, comments, identifiers, commits | [global/language.md](../global/language.md) |
| Topology | 6-layer: ui/adapter/core/pal/gateway/shared | [global/topology.md](../global/topology.md) |
| Layer tags | All pub types carry suffix: `_adp`, `_core`, `_gtw`, `_pal`, `_x` | [global/naming-suffix.md](../global/naming-suffix.md) |
| Mother-child | One owner (state), stateless children, no sibling coupling | [global/mother-tree.md](../global/mother-tree.md) |
| Stereotypes | `shared` not utils, `gateway` not infra — dictionary lookup | [global/stereotypes.md](../global/stereotypes.md) |
| File limits | JS: 250 lines max. Split into mother/child folder | [global/file-limits.md](../global/file-limits.md) |
| Nesting | Max 3 levels. Early returns. Guard clauses first | [global/nesting.md](../global/nesting.md) |
| No debt | No TODO/FIXME/HACK in committed code | [global/tech-debt.md](../global/tech-debt.md) |
| Config-driven | Zero hardcoded values — `_cfg` structs, loaded by gateway | [global/config-driven.md](../global/config-driven.md) |
| Error flow | Validate at boundary, classify, recover at adapter | [global/error-flow.md](../global/error-flow.md) |
| Read first | Read entire file before modifying | [global/read-before-write.md](../global/read-before-write.md) |
| Commit early | Commit every error-free file immediately | [global/commit-early.md](../global/commit-early.md) |

## JavaScript-specific rules

| Rule | Key point | Full doc |
|------|-----------|----------|
| Philosophy | Pure JS + JSDoc + tsc — no .ts files | [js/jsdoc.md](../js/jsdoc.md) |
| Modules | ESM only, `"type": "module"`, file extensions required | [js/modules.md](../js/modules.md) |
| Encapsulation | Modules are CLOSED, `#` for private fields | [js/modules.md](../js/modules.md) |
| Types | JSDoc `@type`, `@param`, `@returns` | [js/jsdoc.md](../js/jsdoc.md) |
| Type checking | `jsconfig.json` + `tsc --noEmit --checkJs --strict` | [js/jsdoc.md](../js/jsdoc.md) |
| Linting | ESLint v9+ flat config, typescript-eslint strict | [js/eslint.md](../js/eslint.md) |
| Validation | Zod/Valibot at boundaries | [js/validation.md](../js/validation.md) |
| Returns | `{ success: true, data }` or `{ success: false, error }` | [js/validation.md](../js/validation.md) |
| Testing | `node:test` + `node:assert/strict` | [js/testing.md](../js/testing.md) |
| Formatting | Prettier, semi, single quotes | [js/project-structure.md](../js/project-structure.md) |

## Verification

| Gate | Tools |
|------|-------|
| Local | `tsc --noEmit --checkJs`, `eslint src/`, `prettier --check` |
| Pre-commit | `rulestools check .` — scan + deny errors |
| Build | `rulestools scan .` — all JS checks |

## BANNED

- `.ts` files — use JSDoc + `jsconfig.json`
- `var` — use `const` or `let`
- `require()` / `module.exports` — ESM only
- `console.log` in production code
- `eval()` / `Function()`
- Files over 250 lines
- Deep nesting (4+ levels)
- `utils.js`, `helpers.js`, `common.js`
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
