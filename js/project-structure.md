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

## Additional Tools

TOOL: knip — find unused exports, dependencies, files
TOOL: publint — validate package.json for publishing
TOOL: depcheck — find unused dependencies
TOOL: madge — detect circular dependencies
TOOL: husky + lint-staged for pre-commit hooks
