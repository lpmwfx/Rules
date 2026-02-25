---
tags: [naming, suffix, base62, collision-prevention]
concepts: [naming, collision-prevention]
keywords: [brand, base62, public-symbols]
layer: 1
---
# Naming Suffix Convention

> Base62 suffix on public symbols — prevents naming collisions across projects

---

## Format

FORMAT: `name_[brand]CODE`
- `name` = function/class/variable name
- `brand` = project/org/personal scope (chosen by project creator)
- `CODE` = 3+ char base62 suffix (0-9, a-z, A-Z)

## Rules

RULE: Public symbols MUST have 3+ char base62 suffix
RULE: Brand prefix is optional but recommended for scoping
RULE: Brand declared in project `.rulevalidator.json` under `naming.brand`
RULE: Project creator defines brand when bootstrapping project
RULE: Missing brand config = BLOCKING ISSUE (must fix before validation)

## Terminology

TERM: "hex" = base62 (0-9, a-z, A-Z) — NOT hexadecimal
REASON: User prefers short term, base62 allows case-sensitive suffixes

## Examples

```
# With brand (recommended):
Issue_rvA1b           # rv project + base62
ok_twb42Z             # twb brand + base62
bootstrap_ai1stXy3    # ai1st org + base62

# Without brand (still valid):
Issue_A1b             # just base62 suffix
parse_document_Qz9    # function with base62
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
    "alphabet": "base62",
    "suffix_min_length": 3
  }
}
```

## Why

- Prevents naming collisions across projects
- Identifies code origin at a glance
- 62³ = 238,328 combinations per name
- Works in all languages (Python, JS, Rust, etc.)
