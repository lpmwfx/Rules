---
tags: [python, naming, conventions, snake-case]
concepts: [naming-conventions, readability]
requires: [global/consistency.md]
related: [rust/naming.md, css/naming.md, global/naming-suffix.md]
layer: 3
---
# Naming Conventions

> Consistent naming across Python codebase

---

RULE: Functions: `verb_noun` (`get_document`, `validate_content`, `push_result`)
RULE: Classes: `PascalCase` (`DocumentRecord`, `ParsedArgs`)
RULE: Constants: `UPPER_SNAKE` (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
RULE: Private: `_prefix` (`_row_to_record`, `_get_connection`)
