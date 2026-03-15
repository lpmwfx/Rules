---
tags: [global, quick-ref, reference, summary, architecture, topology, enforcement]
concepts: [reference, summary, architecture, enforcement]
requires: [global/topology.md, global/mother-tree.md]
related: [global/adapter-layer.md, global/app-model.md, global/config-driven.md, global/persistent-state.md, global/file-limits.md, global/language.md, global/error-flow.md, global/nesting.md, global/module-tree.md, global/naming-suffix.md, global/stereotypes.md, global/consistency.md, global/validation.md, rust/quick-ref.md, slint/quick-ref.md]
layer: 6
---
# Global Quick Reference

> Universal rules for all languages and all projects — scanners enforce these automatically

---

## Language

All code, identifiers, comments, documentation, file names, and commit messages must be in **English**.
Only ASCII characters in source code. UI strings start as English — localize at the boundary only.
AI-human conversation may be in any language — all repo content must be English.

## 6-Layer Topology

Every file lives in exactly one layer. Import direction is strictly one-way downward.

| Folder | Tag | Role |
|--------|-----|------|
| `src/ui/` | `_ui` | Declarative UI (Slint, React, etc.) or MCP server |
| `src/adapter/` | `_adp` | Data exchange hub — ViewModel, event routing |
| `src/core/` | `_core` | Pure business logic — no IO, no UI, no platform |
| `src/pal/` | `_pal` | Platform abstraction — OS, filesystem, clipboard |
| `src/gateway/` | `_gtw` | IO adapter — loads config+state, saves at shutdown |
| `src/shared/` | `_x` | Cross-cutting — errors, traits, shared types |

Import rules:
- **UI** talks only to Adapter (events up, props down)
- **Adapter** is the hub — imports from all layers, coordinates everything
- **Core** calls only PAL — never Adapter, UI, or Gateway
- **Gateway** calls only PAL — never Adapter or UI
- **PAL** is the bottom — calls platform APIs, imports nothing above
- **Shared** (`_x`) may be imported by any layer

## Type Naming — Layer Tag Suffix

Every public type carries its layer tag: `BuilderAdapter_adp`, `CoreState_sta`, `AppConfig_cfg`.
Tag and folder always agree — `_adp` lives in `src/adapter/`, `_gtw` lives in `src/gateway/`.
`grep _adp` finds every Adapter type across all files.
`_sta` and `_cfg` override the layer tag — state and config structs use their own suffix.

## Mother–Child Architecture

Every system has exactly **one origin** (mother) from which all edges emanate.
Only mother owns state — children are stateless transforms.

- Mother passes state down — children never fetch their own
- Children emit events up — mother decides what happens
- Siblings never communicate directly — all coordination through mother
- When a child grows too large, it becomes a sub-mother with its own children
- Complexity grows outward (new children), never inward (deeper monolith)

At **system level**: Adapter is mother (owns AppState), Core/Gateway/PAL are stateless children.
At **UI level**: Window/root component is mother, views are stateless children.
At **module level**: `mod.rs`/`__init__.py`/`index.ts` is mother, child files are stateless.

## File Size Limits

Size limits exist because AI loses context above ~200 lines — not for style reasons.
The line limit is the hard constraint — even a well-encapsulated single-concern module must be split at the limit.
One file = one encapsulated module. If it is growing, it has taken on a second job.

| File type | Hard limit | Action |
|-----------|-----------|--------|
| Slint component | 200 lines | Split — AI loses property graph |
| UI component (JS/TS/Kotlin) | 200 lines | Extract sub-component |
| CSS / SCSS | 150 lines | Split by component |
| Python module | 250 lines | Extract class or function group |
| JS / TS module | 250 lines | Extract to new module |
| Rust module | 300 lines | Split into submodules |
| C++ source file | 350 lines | Extract to new translation unit |

Count lines before writing. "Approaching" means within 20% of the limit.
A split always produces a **folder + mother file** — never just a sibling in the same directory.

## Module Tree

One module = one file — the file boundary is the encapsulation boundary.
"Nested modules" means a folder of files — never nested code inside one file.
When a module spawns sub-modules, it becomes a folder; its code moves to an index/root file.
The parent after a split is a compositor — it imports and arranges, adds no new logic.

## Config-Driven Design

Zero hardcoded values in business logic, UI, or adapter code.
Every configurable value lives in a `_cfg` struct, loaded by Gateway on startup.
Config structs are immutable after startup — passed as parameters, never accessed globally.
Default values are defined in Gateway's load function, not scattered in code.

- Config files: `~/.config/<app>/config/` — read-only during session
- State files: `~/.config/<app>/state/` — read on startup, written on shutdown
- Gateway discovers paths via PAL — never hardcodes `~/.config`

## Persistent State

Gateway is the only layer that reads from or writes to disk for state.
Each layer owns exactly one `_sta` struct for its persistent state.

| Struct | Owner | Content |
|--------|-------|---------|
| `AdapterState_sta` | Adapter | UI view state (selections, scroll, loading flags) |
| `CoreState_sta` | Core | Domain session state (caches, computed results) |
| `GatewayState_sta` | Gateway | IO state (connections, retry counts, timestamps) |

Gateway loads all state on startup, distributes to layers. Saves all state on shutdown.
If a value changes while the app runs → it is state (`_sta`).
If a value only changes between runs → it is config (`_cfg`).

## Adapter Layer

Adapter is the data exchange hub — the only layer that knows all others.
Adapter receives UI events, validates them, dispatches to Core.
Adapter reads Core results, maps to view model structs, stores in `AdapterState_sta`.
UI reads exclusively from `AdapterState_sta` — never from Core directly.
View model types are tagged `_adp` — flat, serializable structs with no domain logic.

## Error Flow

Validation **prevents** errors at boundaries. Error flow **handles** what gets through.
Pipeline: validate input → classify error → recover at Adapter boundary.

| Class | Strategy |
|-------|----------|
| Transient | Retry with backoff, then escalate |
| UserError | Show actionable feedback, app stays valid |
| SystemError | Disable affected feature, keep app running |
| Bug | Capture context, crash reporter, exit cleanly |

Match error variants exhaustively — no wildcard arm that silently discards.
Each subsystem runs inside its own error boundary — a failed subsystem does not crash the app.
User-facing messages at Adapter boundary — never a stack trace, never silence.
When classifying third-party exceptions: retryable? → Transient. User's fault? → UserError. Infrastructure down? → SystemError. Should never happen? → Bug.

## Flat Code — Nesting

Max 3 nesting levels — all languages, no exceptions.
Early returns (guard clauses) at the top. Extract helpers for complex logic.
If/else on the same level, not nested.

## Naming Conventions

A name must explain **why** the variable exists — not just what it contains.
Lifecycle names: `*_input`, `*_parsed`, `*_validated`, `*_resolved`, `*_final`.
Booleans: `is_`, `has_`, `can_`, `should_`.
Collections: always plural. Iterator uses role: `for user in users`.

## Stereotypes — Fixed Names for Fixed Roles

Every folder and module role has a canonical name — the stereotype.
Use the dictionary, never invent new names.

| Use | Instead of |
|-----|-----------|
| `shared` (`_x`) | `common`, `lib` |
| `adapter` or `gateway` | `services` |
| mother (explicit compositor) | `managers` |
| named children by role | `helpers`, `utils` |
| layer name | `infra`, `misc` |

## Cross-Language Consistency

Same patterns in Python, JavaScript, C++, Rust, Kotlin.
Syntax differs, structure identical. One pattern learned = works everywhere.

## Diagrams

All diagrams in Mermaid format — text-based, version-controlled, AI-readable.
No ASCII art, no external tools (draw.io, Lucidchart), no image-only diagrams.

## Technical Debt

No debt markers in committed code. Fix it or file a ticket.
`TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX`, `NOCOMMIT` — all banned in commits.

## Secrets

Secrets live in `~/.env/` — never copied into projects.
Reference via symlink or env var, not duplication. Never commit secrets.

## Read Before Write

Never modify files without reading them first — read the entire file.
90% of refactoring is understanding — 10% is changing.
Map dependencies, exports, imports before touching code.

## Validation

Install rulestools in every project — scan on every commit, watch on every edit.
Fix all errors before committing — warnings inform, errors block.

## BANNED — Universal

- Files over their type's line limit
- Deep nesting (4+ levels)
- Public types without layer tag suffix
- Non-English code, comments, or identifiers
- Hardcoded values in business logic or UI
- Mutable state outside `_sta` structs
- Disk IO outside Gateway
- UI importing Core directly
- Core importing UI, Adapter, or Gateway
- `utils/`, `helpers/`, `misc/`, `common/` folders
- `TODO`/`FIXME`/`HACK` in committed code
- Wildcard error arms that discard without action
- Writing to files without reading them first

## Contract

This ruleset is binding for humans and AI agents — not subject to interpretation.
Rule violations are flagged by scanners and block builds and commits.
