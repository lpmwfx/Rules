---
tags: [rules, ai-coding, standards, overview]
concepts: [coding-standards, ai-rules]
layer: 6
---
# Rules — AI Coding Standards

Shared coding standards for AI-assisted development. Used by Claude Code, Cursor, Copilot, and any AI coding assistant.

## Three Paradigms

The rule system is built on three foundational ideas. Every other rule is a local expression of these.

### Mother-Tree Architecture

A system is a rooted tree. One mother owns state. Children are stateless.

```
Mother (state owner)
 ├── child(input) → output
 ├── child(input) → output
 └── child(input) → output
```

Three rules govern the tree:

1. **Root Rule** — every system has exactly one origin from which all edges emanate
2. **State Rule** — only the root owns state; children are stateless transforms
3. **Growth Rule** — complexity grows outward (new children), never inward (deeper monolith)

This applies recursively: system layers, UI composition, Rust modules, build scripts. See [global/mother-tree.md](global/mother-tree.md).

### Graph-Position Paradigm

A codebase is a directed graph. Every file is a node. Edges define what you may reach and edit.

- **Address** — layer + folder + suffix tag (`_adp`, `_core`, `_ui`, ...)
- **Boundary** — `requires`, `feeds`, `related` edges declare the legal neighbors
- **Scope** — one file, one job; if a file has two jobs, it is two nodes

Position determines authority. If a node is not reachable via declared edges, it is out of scope. See [global/graph-position-paradigm.md](global/graph-position-paradigm.md).

### Stereotypes — The Graph's Type System

Every folder, module, and file role has a canonical name — the stereotype. `gateway` not ~~infra~~. `callbacks` not ~~handlers~~. `shared` not ~~utils~~.

Stereotypes are not cosmetic — they are node labels in a typed graph. The label determines which edges are legal. Same names in every project, every language. Naming is a dictionary lookup, never a design decision. See [global/stereotypes.md](global/stereotypes.md).

### The Link Between Them

These are three aspects of one graph. Mother-Tree defines the **shape** (rooted tree). Graph-Position defines the **rules** (edges determine authority). Stereotypes define the **language** (typed nodes and edges). If the edges are correct and the names are canonical, the architecture is sound.

## Categories

| Category | Files | Topic |
|----------|-------|-------|
| [global/](global/) | 28 | Paradigms, topology, naming, state, file limits |
| [project-files/](project-files/) | 16 | Project files (PROJECT, TODO, FIXES, RULES) |
| [uiux/](uiux/) | 23 | Mother-child UI, state flow, theming, menus, input |
| [python/](python/) | 11 | Python 3.11+ |
| [js/](js/) | 11 | JavaScript (TS-like-JS) |
| [css/](css/) | 11 | CSS (cascade by design) |
| [cpp/](cpp/) | 11 | C++20/23 |
| [rust/](rust/) | 10 | Rust 2021 |
| [kotlin/](kotlin/) | 9 | Kotlin Compose + Amper |
| [slint/](slint/) | 7 | Slint DSL + Rust bridge |
| [automation/](automation/) | 6 | Session startup, context injection |
| [devops/](devops/) | 6 | CI/CD, publishing, packaging |
| [gateway/](gateway/) | 2 | IO adapter lifecycle |
| [adapter/](adapter/) | 2 | Data exchange hub |
| [core/](core/) | 2 | Business logic layer |
| [pal/](pal/) | 2 | Platform abstraction |
| [ipc/](ipc/) | 2 | Unix socket + JSON-RPC 2.0 |

## MCP Server

Install the companion MCP server for IDE integration:

```bash
pipx install git+https://github.com/lpmwfx/RulesMCP.git
claude mcp add -s user rules -- rules-mcp
```

## License

EUPL-1.2
