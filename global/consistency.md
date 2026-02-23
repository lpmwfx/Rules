# Cross-Language Consistency

> Same patterns everywhere — one pattern learned = works in all languages

---

VITAL: Same patterns in Python, JavaScript, C++, Rust, Kotlin
VITAL: One pattern learned = works everywhere
VITAL: Syntax differs, structure identical

## Shared Patterns (All Languages)

- **Result types**: `{success, data/error}`
- **Closed modules**: one file, private state
- **Flat nesting**: max 3 levels
- **Explicit types**: annotate everything
- **Validation at boundaries**

RESULT: Less AI capability needed, better AI output
REASON: AI learns pattern once, applies everywhere

## Modules Are Classes

JS module = Python module = CSS file = Same structure:
- Own scope (private state / own domain)
- Clear interface (exports / class prefix)
- No side effects on others
- One file, one responsibility
