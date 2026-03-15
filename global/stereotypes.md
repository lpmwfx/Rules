---
tags: [stereotypes, naming, typed-graph, vocabulary, dictionary, architecture]
concepts: [stereotype-rule, typed-nodes, closed-vocabulary, role-naming]
requires: [global/mother-tree.md, global/graph-position-paradigm.md]
feeds: [global/topology.md, global/naming-suffix.md, global/module-tree.md, uiux/file-structure.md]
related: [uiux/mother-child.md, project-files/project-file.md]
keywords: [stereotype, dictionary, role, name, folder, label, type, graph, node-type, edge-type, vocabulary, banned-names]
layer: 1
---
# Stereotypes — The Graph's Type System

> A stereotype is a fixed name for a fixed role. Look it up. Never invent.

---

## The Rule

VITAL: Every folder, module, and file role has a canonical name — the stereotype
VITAL: Stereotypes are universal — same name in every project, every language, every layer
VITAL: Naming a node is not a design decision — it is a dictionary lookup
BANNED: Inventing new names for roles that already have a stereotype
BANNED: Using synonyms — `helpers`, `utils`, `common`, `misc`, `lib`, `services`, `managers`

## Why This Is a Graph Concept

In a typed graph, node labels determine which edges are legal.
When a node is labeled `callbacks/` and another is labeled `views/`, the graph knows:
- `callbacks` → `views` is valid (callbacks wire view events)
- `views` → `callbacks` is invalid (views are stateless, they do not import callbacks)

Stereotypes are not cosmetic. They are the type system of the architecture graph.

## Dictionary

### Layer Stereotypes (crate / top-level folder)

| Stereotype | Role | Never |
|-----------|------|-------|
| `ui` | Declarative UI surface | ~~frontend, presentation, display, web~~ |
| `adapter` | Data exchange hub, ViewModel | ~~controller, service, middleware, manager~~ |
| `core` | Pure business logic | ~~domain, logic, engine, processor~~ |
| `pal` | Platform abstraction | ~~platform, os, system, native~~ |
| `gateway` | IO adapter — disk, network, processes | ~~infra, persistence, data-access, repository, io~~ |
| `shared` | Cross-cutting types and errors | ~~common, utils, helpers, lib, base~~ |
| `mcp` | AI interface (MCP server as UI surface) | ~~api, rpc, bot~~ |

### Module Stereotypes (folder inside a layer)

| Stereotype | Role | Parent layer |
|-----------|------|-------------|
| `callbacks` | Mother's event registrations for UI | `ui` |
| `views` | Stateless view components (direct children of mother) | `ui` |
| `components` | Reusable UI building blocks | `ui` |
| `overlays` | Modals, dialogs, toasts | `ui` |
| `tokens` | Design values — colors, spacing, fonts | `ui` |
| `globals` | Slint global singletons | `ui` |
| `gateway` | IO sub-module within a layer | any |

### File Stereotypes (file inside a module)

| Stereotype | Role |
|-----------|------|
| `mod.rs` / `index.ts` / `__init__.py` | Mother — composes and wires children |
| `types` | Type definitions for the module |
| `config` | Configuration structs |
| Named by domain entity | Child — one entity per file (`story.rs`, `canvas.rs`, `project.rs`) |

### Suffix Tags (type-level)

| Tag | Layer |
|-----|-------|
| `_ui` | UI |
| `_adp` | Adapter |
| `_core` | Core |
| `_pal` | PAL |
| `_gtw` | Gateway |
| `_x` | Shared |
| `_sta` | State struct (any layer) |
| `_cfg` | Config struct (any layer) |

### Project File Stereotypes

| Stereotype | Role |
|-----------|------|
| `PROJECT` | Single source of truth — state, phase, stack |
| `TODO` | Current tasks |
| `FIXES` | Known problems — do not repeat |
| `RULES` | Active rules for this project |
| `UIUX` | UI/UX source of truth |

## Banned Names

BANNED: `helpers` — has no role; split into named children by what they actually do
BANNED: `utils` — same problem; every "util" belongs in a real module
BANNED: `common` — use `shared` with `_x` tag
BANNED: `lib` — use the layer name
BANNED: `services` — use `adapter` or `gateway` depending on IO involvement
BANNED: `managers` — a manager is a mother that does not know it; make it explicit
BANNED: `misc` — if it has no role, it has no place
BANNED: `infra` — use `gateway` for IO, `pal` for platform abstraction

## Composition — Stereotypes + Suffix Tags

Stereotypes name the **folder/module**. Suffix tags name the **type inside it**. They compose:

```
src/adapter/               ← layer stereotype: "adapter"
├── mod.rs                 ← file stereotype: mother (composes children)
├── canvas.rs              ← file stereotype: named by domain entity
│   └── CanvasAdapter_adp  ← suffix tag: _adp (matches layer folder)
│   └── CanvasState_sta    ← suffix tag: _sta (overrides layer — state struct)
└── inspector.rs
    └── InspectorAdapter_adp

src/ui/callbacks/          ← module stereotype: "callbacks" (inside ui layer)
├── mod.rs                 ← mother — register_all()
├── canvas.rs              ← child — register(ui, &state)
└── file_ops.rs            ← child — register(ui, &state)
```

RULE: Stereotype names the container (folder). Suffix tag names the content (type). Both are required.

RESULT: Any AI can navigate an unknown project instantly — the names are always the same
REASON: Stereotypes eliminate ambiguity; the dictionary replaces design discussions with lookups
