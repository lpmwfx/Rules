# Language Detection

> Detect project languages and load relevant rules

---

## Python Indicators

- `pyproject.toml`
- `requirements.txt`
- `*.py` files

## JavaScript Indicators

- `package.json`
- `jsconfig.json`
- `*.js` files

## CSS Indicators

- `*.css` files
- `static/css/` directory

## Key Rules Summary

### Python (6 Critical Rules)

```
• from __future__ import annotations — ALL files
• Modern unions: str | None (never Optional)
• ACK pattern: {success: True, data} or {success: False, error}
• Max 3 nesting levels — extract to helper if deeper
• Max 20 lines per function, 200-350 per file
• Real DBs in tests (SQLite), no mocks
```

### JavaScript (6 Critical Rules)

```
• TS-like-JS: JSDoc types + tsc --noEmit for checking
• ESM only: import/export, 'type': 'module'
• Modules are CLOSED — internal state not shared
• Zod/Valibot at boundaries for runtime validation
• Result types: {success: true, data} or {success: false, error}
• jsconfig.json with strict: true, checkJs: true
```

### CSS (6 Critical Rules)

```
• Separation: layout files have ZERO colors
• Theme files have ONLY colors (--color-*, --shadow-*)
• One file per component/module
• Cascade by design: each file ADDS, none overwrites
• Mobile-first, single breakpoint: 768px
• BEM-inspired: .block-element--modifier
```
