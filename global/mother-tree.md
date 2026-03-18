---
tags: [mother-tree, root, stateless, state-owner, architecture, paradigm, vector, dag, growth]
concepts: [mother-tree-architecture, root-rule, state-rule, growth-rule, stateless-children, recursive-ownership]
requires: [global/graph-position-paradigm.md]
feeds: [global/topology.md, uiux/mother-child.md, uiux/state-flow.md, global/module-tree.md, global/file-limits.md, web/mother-child.md]
related: [global/adapter-layer.md, global/persistent-state.md]
keywords: [mother, child, root, state, stateless, tree, vector, edge, node, origin, growth, complexity, expansion, compositor, owner]
layer: 1
---
# Mother-Tree Architecture

> A system always has an origin from which edges emanate. That origin owns state. Everything else is stateless.

---

## The Three Rules

VITAL: **Root Rule** — Every system has exactly one origin (Mother) from which all edges emanate
VITAL: **State Rule** — Only Mother owns state — children are stateless transforms
VITAL: **Growth Rule** — Complexity grows outward (new children), never inward (deeper monolith)

These are not patterns. They are the topology itself. Everything else in the rule system is a local expression of this structure.

## Edges Are the System

Nodes are containers. Edges define the architecture.

A healthy system has exactly two edge directions per node:

```
Mother ──props──► Child       (data down)
Mother ◄──event── Child       (signal up)
```

VITAL: If the edges are correct, the system is sound — regardless of what the nodes contain
VITAL: If the edges are wrong, the system is broken — regardless of how good the nodes are

This applies identically to code, to this rule system, and to AI retrieval:

| Domain | Node | Edge |
|--------|------|------|
| Code | file | import, prop, callback |
| Rules | `.md` file | requires, feeds, related |
| AI/RAG | retrieved document | graph traversal to next document |

RULE: Mother passes state down — children never fetch their own
RULE: Children emit events up — Mother decides what happens
RULE: Siblings never share edges — all coordination routes through Mother
RULE: When a child grows too large, it becomes a sub-mother with its own children
BANNED: Children querying global state, stores, or context directly
BANNED: Children importing from siblings — horizontal edges break the tree
BANNED: Extending capability by making Mother or an existing child larger

## Why O(n) Not O(n²)

Monolith: nodes can reach every other node → edges ≈ n²
Mother-Tree: every child has exactly one edge (to its mother) → edges = n

Adding child #100 is exactly as safe as adding child #3.

## Where the Rules Live

Each rule is enforced in its own file — this file only states the shared foundation.

| Rule | Detailed enforcement |
|------|---------------------|
| Root Rule | `topology.md` (6-layer DAG), `mother-child.md` (single compositor) |
| State Rule | `mother-child.md` (props down, events up), `persistent-state.md` (state ownership) |
| Growth Rule | `file-limits.md` (max lines), `module-tree.md` (split strategy) |

RESULT: AI can modify any child without understanding the whole system
REASON: The surface area for any edit is exactly one file with no hidden dependencies
