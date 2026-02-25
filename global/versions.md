---
tags: [versions, lts, modern]
concepts: [language-versions, compatibility]
related: [global/consistency.md, devops/packaging.md]
layer: 1
---
# Modern Language Versions

> Not outdated, not bleeding edge — the middle path

---

RULE: Use highest version all modern browsers/runtimes support
RULE: AI knows latest LTS best — use it

## Current Versions

| Language | Version | Rationale |
|----------|---------|-----------|
| JavaScript | ES2024 | Modern browsers, Node 18+ |
| Python | 3.11+ | Current LTS, AI trained on it |
| CSS | Modern features | Custom properties, grid, :has() |

BANNED: Legacy syntax for old browser support (unless explicit requirement)
BANNED: Bleeding edge proposals not yet stable
REASON: AI trained on modern code — modern code gets best AI output

PRINCIPLE: The middle path has least resistance
```
Legacy (AI guesses) <-- Modern stable (AI knows) --> Bleeding edge (AI guesses)
```
