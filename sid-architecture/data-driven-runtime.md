---
tags: [sid, data-driven, runtime, motor, datastore, selective, architecture]
concepts: [data-driven-runtime, motor-contract, runtime-resolver, selective-coverage]
requires: [sid-architecture/sid-identity.md]
feeds: [sid-architecture/meta-driven-ui.md]
related: [sid-architecture/working-in-data.md, sid-architecture/environments.md, deprecated/persistent-state.md, deprecated/app-model.md, deprecated/state-flow.md]
keywords: [runtime, datastore, motor, widget, resolver, event-routing, reactivity, selective, rebuild, live, SurrealDB, OPFS]
layer: 1
binding: false
status: prototype
---
# Data-Driven Runtime — Principle 03

> After compilation, the parts of the system that should be changeable must be determined by SID records in a live datastore, not by code or build-time data.
>
> **Supersedes (prototype):** `deprecated/state-flow.md`, runtime state rules in `deprecated/app-model.md`, `deprecated/persistent-state.md`

---

## How Principle 03 Relates to Principle 02

"Data" does not mean the same thing in both principles. Principle 02 is categorical: everything in source code gets a SID, data lives in repo files, read at build. Principle 03 is selective: only what needs to vary at runtime lives in a live datastore, read at runtime.

| | Principle 02 | Principle 03 (this file) |
|---|---|---|
| Scope | Everything in source code | Only what must vary at runtime |
| Coverage | Consistent, categorical | Selective, architecture-determined |
| Where SID records live | File in the repo | Live datastore |
| Read at | Build-time | Runtime |
| Change requires | Rebuild | Nothing |

A SID can start as a build-time constant (Principle 02) and move to a runtime datastore (Principle 03) without changing identity. The reverse also works — a runtime SID that never changes in practice can move back to build-time.

The four combinations:

| | Principle 02 no | Principle 02 yes |
|---|---|---|
| **Principle 03 no** | Traditional app | Well-organized monolithic app |
| **Principle 03 yes** | Messy engine with magic numbers | **The goal: clean engine + live data** |

---

VITAL: The engine knows *how*; the datastore says *what*
VITAL: Data-driven and declarative are different things — this is architectural, not linguistic
RULE: Coverage is selective — only what must vary at runtime lives in the datastore
RULE: The engine contains mechanics and infrastructure, no domain content for what is changeable
RULE: The datastore contains SID records for what the system must change without rebuild
RULE: UI always tends toward full coverage — UI changes more often than business logic
BANNED: Build-time import (`import symbols from './symbols.json'`) as "data-driven" — that is Principle 02
BANNED: Hardcoded enum domains for what should be runtime-configurable
BANNED: Expressions in data (`condition`, `if`, `when`, `formula`) — that is pseudocode

## Engine Contract

1. **Read SID records at runtime** — not import them at build
2. **Instantiate widgets/structure based on records** — the tree is read, not defined in code
3. **Route events via SID** — click emits a SID, engine looks up what should happen
4. **React to data changes** — records change, all references update without rebuild
5. **No runtime-configurable content in the engine** — no strings, numbers, colors hardcoded

## Selective Coverage

- Internal admin app: maybe 5% of SIDs in runtime data
- Configurable platform: maybe 90%
- SIDs can move between build-time and runtime over time

## What the Datastore Typically Contains

- Labels and text visible to the user
- Screen and widget trees
- Business rules and parameters
- Themes, colors, branding
- Feature flags
- Event routing

## Transient State Is Not Content

Runtime state from user interaction (count in a counter, input text) is neither code nor data. It is transient state in RAM. The principle applies to hardcoded values, not runtime state.

## What It Gives

- Changes without rebuild — new screen, changed label, adjusted threshold live
- One binary, many systems — same engine, different datastores
- Versioning the system as data — git, migrate, branch as records
- AI conversation can change the running system directly

## What It Requires

- Resolver infrastructure in the engine
- Datastore with reactivity, consistency, authorization
- Schema for widgets/screens/rules as data
- Discipline to never sneak content into engine code


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
