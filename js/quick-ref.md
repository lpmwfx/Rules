# JavaScript Quick Reference

> All rules at a glance

---

| Rule | Details |
|------|---------|
| Philosophy | Pure JS + JSDoc + tsc — no .ts files |
| Modules | ESM only, `"type": "module"` |
| Encapsulation | Modules are CLOSED, `#` for private fields |
| Types | JSDoc `@type`, `@param`, `@returns` |
| Type checking | `jsconfig.json` + `tsc --noEmit --checkJs --strict` |
| Linting | ESLint v9+ flat config, typescript-eslint strict |
| Validation | Zod/Valibot at boundaries |
| Returns | `{ success: true, data }` or `{ success: false, error }` |
| Testing | `node:test` + `node:assert/strict` |
| Formatting | Prettier, semi, single quotes |
