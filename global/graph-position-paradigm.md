---
tags: [graph-position, edit-authority, boundary, traversal, paradigm, overwrite-prevention, spatial-reasoning, session-protocol]
concepts: [graph-position-paradigm, edit-authority, node-boundary, session-traversal, position-determines-authority]
feeds: [global/topology.md, global/naming-suffix.md, global/module-tree.md, global/file-limits.md, global/read-before-write.md, global/know-before-change.md, global/index-system.md, global/startup.md, global/persistent-memory.md]
keywords: [position, authority, boundary, traversal, node, edit, scope, reachable, overwrite, graph, spatial, session, paradigm]
layer: 1
---
# Graph-Position Paradigm

> Every edit happens at a node. The node defines what you may touch.

---

## The Core Idea

A codebase is not a flat list of files.
It is a directed graph — nodes connected by typed edges (`requires`, `feeds`, `related`, `layer`).

When an AI session begins, it does not "open a project."
It **enters a node** — a specific, located position in the graph.

From that position, exactly three things are true:

1. **You know where you are** — the current node has an identity (file, layer, suffix tag)
2. **You know what you may reach** — edges define the traversal boundary
3. **You know what is out of bounds** — everything not reachable via declared edges

This is the Graph-Position Paradigm.
It is not a file convention. It is not a naming rule. It is a way of reasoning about every edit.

---

## Why This Produces 80% Fewer Overwrite Errors

The dominant cause of AI overwrite errors is not logic failure — it is **spatial confusion**.

The AI reads file A for context, notices something in file B that "looks related,"
and edits B without understanding B's position in the graph.
B may be consumed by five other nodes. The AI touched none of them.
The edit was local in appearance; it was global in effect.

The Graph-Position Paradigm prevents this by making **position primary**:

```
Without paradigm:   "This file looks relevant — I'll edit it."
With paradigm:      "This file is not reachable from my current node — I will not touch it."
```

Distance in the graph is not aesthetic. It is a hard constraint on edit authority.

---

## The Three Properties of a Node

Every node in the codebase — every file — carries three implicit properties:

### 1. Address
Where the node lives in the topology.

```
address = layer + folder + suffix tag
example: src/adapter/FeedAdapter_adp.rs  →  layer:adapter / tag:_adp
```

The suffix tag is the grep-searchable address.
`grep _adp` finds every Adapter node. No IDE required.

### 2. Boundary
What the node may reach.

```
boundary = declared edges in the rule graph
    requires  →  must load before this node is safe to edit
    feeds     →  will be affected by changes to this node
    related   →  informational — read-only context, not edit authority
    layer     →  topological rank — lower layers may not import higher layers
```

An edge is not a suggestion. It is the complete set of legal neighbors.

### 3. Scope
What the node is responsible for — and nothing else.

```
scope = one module, one job, one file
        if a file has two jobs, it is two nodes pretending to be one
        split it before editing
```

---

## Graph Traversal as Session Protocol

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

---

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

---

## The Rule That Was Missing

The existing rule system had:
- Node addresses (suffix tags)
- Edge types (requires, feeds, related, layer)
- Import direction enforcement (topology DAG)
- File size limits (module boundary enforcement)
- Read-before-write (session safety)
- Know-before-change (understanding requirement)

What it did not have was a rule that **coupled graph position to edit authority**:

```
VITAL: You may only edit files reachable from your current node via requires/feeds edges
VITAL: Reading a file for context does NOT grant edit authority over that file
VITAL: If a fix requires editing outside your boundary, stop and surface the boundary conflict
BANNED: Editing a file because it "looks related" — related is read-only
BANNED: Refactoring nodes you visited for context
BANNED: Expanding scope silently — boundary conflicts are user decisions, not AI decisions
```

This rule is the paradigm expressed as a constraint.
The paradigm is the reasoning. The rule is the enforcement.

---

## Relationship to Existing Rules

The Graph-Position Paradigm does not replace existing rules.
It is the conceptual frame that makes them coherent as a system:

| Existing Rule | Its role in the paradigm |
|---|---|
| `topology.md` | Defines the layer graph — the macro-level node positions |
| `naming-suffix.md` | Encodes node address in every type name |
| `module-tree.md` | Enforces one-node-per-file — the file IS the node |
| `file-limits.md` | Prevents nodes from growing beyond AI comprehension |
| `read-before-write.md` | Requires entering a node before editing it |
| `know-before-change.md` | Requires understanding a node's edges before touching it |
| `index-system.md` | Provides the address register — the traversable map |
| `startup.md` | Initializes the session at a known position in the graph |
| `persistent-memory.md` | Carries graph knowledge across session boundaries |

Each rule is a local expression of a single global principle:
**position determines authority**.

---

## Adding New Rules Under This Paradigm

When writing a new rule, ask three questions:

1. **Does it define a node property?**
   → It belongs in the address, boundary, or scope category.
   → Attach it to the relevant layer (global, language, uiux, etc.)

2. **Does it constrain traversal?**
   → It is an edge rule — add it to the requires/feeds/related/layer edge semantics.
   → It should produce a BANNED statement about editing outside the boundary.

3. **Does it govern session behavior?**
   → It belongs in the startup checklist or session protocol.
   → It should produce a VITAL statement about what happens before/during/after an edit.

Rules that cannot be placed in one of these three categories are not rules about the paradigm.
They are rules about something else — likely a language-specific or tool-specific convention.
Those rules belong in the language or tooling category, not in global.

---

## Summary

```
A codebase is a graph.
Every file is a node.
Every node has an address, a boundary, and a scope.
A session is a traversal — it starts at a node and expands only along declared edges.
Edit authority follows the traversal — nothing outside the boundary may be touched.
When a fix requires crossing a boundary, surface the conflict — do not expand unilaterally.

This is not a file convention.
This is how AI reasoning about code must be structured to be reliable.
```

---

*This document introduces the Graph-Position Paradigm as the unifying conceptual frame
for the rule system. Individual rule files implement specific constraints within this frame.
The paradigm itself lives here — the rules live in their respective category files.*
