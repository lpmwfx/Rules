---
tags: [structure, project-layout, topology]
concepts: [file-organization, architecture, topology-mapping]
requires: [global/consistency.md, global/topology.md]
feeds: [web/topology.md]
layer: 3
---
# Project Structure

> Package.json, scripts, file layout

---

## Directory Layout

```
project/
├── src/
│   ├── index.js          # Main entry
│   ├── module.js         # Feature module
│   └── module.test.js    # Tests alongside
├── dist/                 # Build output (gitignored)
├── jsconfig.json         # TypeScript config
├── eslint.config.js      # ESLint flat config
├── .prettierrc           # Prettier config
└── package.json          # type: module
```

## package.json Scripts

```json
{
  "type": "module",
  "scripts": {
    "typecheck": "tsc --project jsconfig.json",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write src/",
    "format:check": "prettier --check src/",
    "check": "npm run typecheck && npm run lint && npm run format:check",
    "test": "node --test src/**/*.test.js"
  }
}
```

## Prettier Config (.prettierrc)

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}
```

## Topology Layout

For WA/PWA web projects, the flat layout above expands to the full 6-layer topology.
See [web/topology.md](../web/topology.md) for the complete browser folder mapping.

```
project/
├── src/
│   ├── ui/           ← views, components (_ui)
│   ├── adapter/      ← ViewModel, event routing (_adp)
│   ├── core/         ← pure business logic (_core)
│   ├── gateway/      ← fetch, localStorage, IndexedDB (_gtw)
│   ├── pal/          ← Web API abstractions (_pal)
│   └── shared/       ← errors, result types (_x)
├── dist/
└── package.json
```

RULE: CLI projects use the flat layout — `src/index.js` + feature modules
RULE: WA/PWA projects use the full topology — all six layers under `src/`
RULE: Suffix tags apply: `feedAdapter_adp.js`, `storageGateway_gtw.js`

## Additional Tools

TOOL: knip — find unused exports, dependencies, files
TOOL: publint — validate package.json for publishing
TOOL: depcheck — find unused dependencies
TOOL: madge — detect circular dependencies
TOOL: husky + lint-staged for pre-commit hooks


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
