---
tags: [global, language, english, localization, ascii]
concepts: [code-language, english-first, localization, ascii]
keywords: [english, ascii, localization, i18n, documentation-language]
related: [global/consistency.md, global/validation.md]
layer: 1
---
# Language in Code

> All code and documentation is in English — localize UI strings, never source code

---

RULE: All code, identifiers, comments, and documentation must be written in English
RULE: Only ASCII characters are permitted in source code — no unicode in identifiers, strings, or comments
RULE: UI strings start as English literals — extract to localization files only when i18n is required
RULE: Variable names, function names, file names, and commit messages are always English
RULE: All rule files, project files, and repository content must be written in English
RULE: AI-human conversation may be in any language — all repo content must be English

BANNED: Non-ASCII characters in source code identifiers or comments
BANNED: Native-language strings hardcoded in logic layers — use English keys, localize at the boundary
BANNED: Mixing languages in the same file or module

## Why

- Maximum compatibility across tools, editors, CI, and AI assistants
- English is the shared language of all programming communities and standard libraries
- ASCII-only source code prevents encoding issues across platforms and shells
- Consistent language = consistent AI output

## Localization Pattern

```
# Wrong — native string in logic
label = "Gem fil"

# Right — English key, localized at boundary
label = t("save_file")  # en: "Save file", da: "Gem fil"
```

UI text starts as English. Add i18n only when the project explicitly requires it.
