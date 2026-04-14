---
tags: [sid, topology, data, structure, inner-platform, ai-readable]
concepts: [topology-as-data, structure-vs-logic, inner-platform-effect, ai-readability]
requires: [sid-architecture/working-in-data.md]
related: [global/topology.md, sid-architecture/meta-driven-ui.md]
keywords: [topology, structure, logic, nouns, verbs, inner-platform, richness, expressions, canonical, pattern-recognition, AI]
layer: 1
binding: false
status: prototype
---
# Topology as Data

> Data expresses what *is*. Code expresses what *happens*. Rich structure in data is good. Logic in data is bad.

---

VITAL: Structure yes, logic no — data is nouns, code is verbs
RULE: Data may be as rich as you want, as long as it stays in the noun category
RULE: Canonical names carry topology — AI reads the entire structure as a graph
RULE: When the data schema requires something beyond SID + value + named relations, the engine is missing a mechanism
BANNED: Expressions in data (`condition`, `if`, `when`, `evaluate`, `formula`, `script`, `rule_body`)
BANNED: Pseudocode disguised as JSON/TOML

## Rich Topology: Good

```json
{
  "aK3qP9": {
    "canonical": "ui.form.signup.field.email.label.default",
    "value": "Email"
  },
  "dR5tL1": {
    "canonical": "ui.form.signup.field.email.validation.required",
    "value": true
  }
}
```

Rich, explicit. AI can read the pattern, predict extensions, spot inconsistencies.

## Expressions in Data: Bad

```json
{
  "kX4mP2": {
    "condition": { "field": "state", "equals": "loading" },
    "then": "Sending...",
    "else": "Send"
  }
}
```

That is an if-statement in JSON. Fix: build the mechanism in the engine, let data point into it with SIDs and mappings.

## Three Mental Tests

1. **Is there a verb?** Data is nouns. Action words belong in code.
2. **Can the schema be described with only SID + value + relations?** If no, the engine is missing a mechanism.
3. **Can AI read this without running code?** If AI would need to simulate expressions to understand — logic in data.

## Canonical Names as a Superpower for AI

`ui.form.signup.field.email.label.error.required` is the system's structure encoded as a path:

- **Pattern recognition** without interpretation
- **Consistency checks** trivially ("does password also have error.format?")
- **Predictable extension** — replicate pattern from existing field
- **Refactoring as data operation** — search-and-update, not code change


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
