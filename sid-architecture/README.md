---
tags: [sid, architecture, identity, data-driven, code-hygiene, foundation]
concepts: [sid-identity, data-driven-runtime, code-hygiene, working-in-data]
related: [global/topology.md, global/data-driven-ui.md]
keywords: [SID, identifier, 6-char, resolve, symbols, mutable, data-driven, motor, datastore, runtime, build-time, AI-operable]
layer: 1
---
# SID Architecture — PROTOTYPE

> Design philosophy for data-driven systems built for conversation-based development
>
> **STATUS: PROTOTYPE — not adopted as rules. These principles are under evaluation and must not be enforced by scanners, hooks, or compliance checks. Treat as reference material, not binding rules.**

SID architecture solves name collisions in AI-assisted development by removing naming as a coordination problem. A generator issues random, globally unique 6-character identifiers. Stereotypical names move to data as fields on the SID, where collisions are cosmetic rather than functional.

---

## Structure

| File | Content |
|---|---|
| `sid-identity.md` | Foundation: what a SID is, format, generation |
| `code-free-of-mutables.md` | Principle 02: categorical source code hygiene (includes orthogonality) |
| `data-driven-runtime.md` | Principle 03: selective architecture after compile (includes orthogonality) |
| `working-in-data.md` | The third area: AI's native workspace |
| `topology-as-data.md` | Rich structure good, expressions-in-data bad |
| `environments.md` | Compiled vs. interpreted; the medium draws the line |
| `meta-driven-ui.md` | Widget records, screen compositions, parser |

## Core Insights

- **SIDs are found, not designed.** A generator produces random strings and checks uniqueness. The SID is the entity; names are fields on the SID.
- **"Data" means two things.** Build-time files (Principle 02) and live datastore (Principle 03) are orthogonal.
- **Richness in data is good, logic in data is bad.** Structure yes, pseudocode no.
- **The medium draws the line.** HTML+JS are easy on disk, JSON is easy in database.
- **UI is always Principle 03.** Regardless of language and environment, UI tends toward full data-driven architecture.

## Reading Order

1. `sid-identity.md` — the foundation
2. `two-principles.md` — the two applications
3. `working-in-data.md` — why it's all worth doing
4. `code-free-of-mutables.md` and `data-driven-runtime.md` — the details

> Source: `https://git.lpmintra.com/ai/SID-architecture`


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
