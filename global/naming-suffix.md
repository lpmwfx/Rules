---
tags: [naming, suffix, code-suffix, collision-prevention]
concepts: [naming, collision-prevention]
related: [global/consistency.md, automation/tool-configs.md]
keywords: [brand, code-suffix, identifiers]
layer: 1
---
# Naming Suffix Convention

> Brand + code suffix on all identifiers — same code for the entire project

---

## Format

FORMAT: `name_BRANDCODE`
- `name` = variable, function, class, constant name
- `BRAND` = project/org scope (chosen by project creator)
- `CODE` = 3+ chars from a-z, A-Z, 0-9 — fixed per project

VITAL: One code suffix per project — every identifier uses the same code
VITAL: Applies to all identifiers created by the coder inside code files
BANNED: Suffix on file names — only code identifiers

## Rules

RULE: All identifiers (variables, functions, classes, constants) MUST have brand+code suffix
RULE: The code suffix is chosen once per project and reused everywhere
RULE: Code characters: a-z, A-Z, 0-9 (case-sensitive)
RULE: Minimum 3 characters for the code part
RULE: Brand declared in project `.rulevalidator.json` under `naming.brand`
RULE: Project creator defines brand+code when bootstrapping project
RULE: Missing brand config = BLOCKING ISSUE (must fix before validation)
BANNED: Different codes for different symbols in the same project
BANNED: Suffixes on file names or directory names

## Examples

```
# Project: RulesValidator, brand=rv, code=A1b
# → Every identifier in this project uses _rvA1b

Issue_rvA1b              # class
parse_document_rvA1b     # function
total_count_rvA1b        # variable
MAX_RETRIES_rvA1b        # constant

# Project: TwistedBrain, brand=twb, code=42Z
ok_twb42Z                # function
config_twb42Z            # variable

# Project: AI1st, brand=ai1st, code=Xy3
bootstrap_ai1stXy3       # function
```

## Known Brands

- `twb` — TwistedBrain (personal)
- `lpm` — lpm username
- `ai1st` — AI1st organization
- `rv` — RulesValidator project

## Config (.rulevalidator.json)

```json
{
  "naming": {
    "brand": "rv",
    "code": "A1b",
    "suffix_min_length": 3
  }
}
```

## Why

- Prevents naming collisions across projects
- Identifies code origin at a glance
- Same suffix everywhere = easy to search/replace
- Works in all languages (Python, JS, Rust, etc.)
