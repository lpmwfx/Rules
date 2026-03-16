---
tags: [graph-position, traversal, session-protocol, edit-authority, boundary]
concepts: [graph-traversal, session-protocol, level-application]
requires: [global/graph-position-paradigm.md]
related: [global/read-before-write.md, global/know-before-change.md, global/startup.md]
keywords: [traversal, session, starting-node, requires, feeds, related, boundary, scope, file-level, module-level, session-level, project-level]
layer: 1
---
# Graph Traversal as Session Protocol

> A session is a traversal — start at a node, expand only along declared edges

---

## Session Protocol

When Claude Code begins a task, it does not scan the codebase.
It **traverses from a starting node**, loading only what the edges declare.

```
Session start
  │
  ├── Enter node (the file named in the task)
  ├── Load: requires edges  →  dependencies I must understand
  ├── Load: feeds edges     →  consumers I must not break
  ├── Read: related edges   →  context only — no edit authority
  └── Form solution         →  touch only: current node + requires nodes
```

Everything outside this traversal is **not in scope**.
Not because it is unimportant — because the AI cannot safely reason about it from this position.

This is the same principle as a tree search with a bounded depth:
the search does not explore nodes it cannot reach in `n` steps.
An AI session does not edit files it cannot reach via declared edges.

## What Changes at Each Level

### At the File Level
Every file knows its own address.
The suffix tag is not decoration — it is the machine-readable position in the graph.

```rust
// The type name IS the address
pub struct FeedAdapter_adp { ... }   // → src/adapter/  layer: adapter
pub struct FeedCore_core   { ... }   // → src/core/     layer: core
```

If you rename the type without moving the file, the address is wrong.
If you move the file without renaming the type, the address is wrong.
Tag and folder must always agree — this is a hard constraint, not a convention.

### At the Module Level
Every module has one job. One job means one set of edges.
A module that does two jobs has two edge sets — it is two nodes, not one.

```
Signal: a file's edges point in two different directions
Action: split the file — one node per direction
```

The module boundary and the file boundary are the same boundary.
When you split a module into a folder, the parent file becomes a composer:
it imports and arranges its children; it adds no new logic.

### At the Session Level
A session is a traversal. It starts at a node and expands only along declared edges.

```
BEFORE any edit:
  1. Identify the starting node (the task's target file)
  2. Load its requires edges  →  what must I understand?
  3. Identify its feeds edges  →  what will I affect?
  4. Confirm scope            →  is the task solvable within this boundary?
  5. If not: surface the boundary conflict to the user — do not expand unilaterally

DURING edit:
  - Touch only: the starting node + its requires-reachable nodes
  - Read-only:  related nodes (context, never edit authority)
  - Forbidden:  any node not reachable in the declared graph

AFTER edit:
  - Verify: does the edit break any feeds-declared consumer?
  - If yes: the edit is incomplete — surface this, do not silently fix feeds nodes
```

### At the Project Level
The codebase topology is the authoritative map.
It lives in `global/topology.md` and is enforced by suffix tags + import rules.
The import DAG is the graph. The suffix tags are the node addresses.
`index.yaml` is the generated address register — the lookup table for the full map.

RESULT: Every edit is bounded by declared edges — no silent cross-boundary changes
REASON: Unbounded traversal is the root cause of AI overwrite errors
