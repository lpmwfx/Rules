---
tags: [graph-position, edit-authority, boundary, traversal, paradigm, overwrite-prevention, spatial-reasoning, session-protocol]
concepts: [graph-position-paradigm, edit-authority, node-boundary, session-traversal, position-determines-authority]
feeds: [global/topology.md, global/naming-suffix.md, global/module-tree.md, global/file-limits.md, global/read-before-write.md, global/know-before-change.md, global/index-system.md, global/startup.md, global/persistent-memory.md, global/graph-traversal.md, global/graph-rules.md]
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

Graph traversal protocol: [global/graph-traversal.md](graph-traversal.md)
Edit authority rules and relationships: [global/graph-rules.md](graph-rules.md)

---

*This document introduces the Graph-Position Paradigm as the unifying conceptual frame
for the rule system. Individual rule files implement specific constraints within this frame.
The paradigm itself lives here — the rules live in their respective category files.*
