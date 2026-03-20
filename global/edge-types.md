---
tags: [edges, typed-graph, adjacency, architecture, dictionary, stereotypes]
concepts: [edge-types, adjacency-rules, typed-edges, graph-constraints]
requires: [global/stereotypes.md, global/mother-tree.md]
feeds: [global/topology.md, global/graph-position-paradigm.md]
related: [global/naming-suffix.md, uiux/mother-child.md, uiux/state-flow.md]
keywords: [edge, edge-type, adjacency, import, prop, callback, requires, feeds, related, dispatch, result, constraint, typed-graph]
layer: 1
---
# Edge Types — The Graph's Connection Dictionary

> A stereotype names a node. An edge type names a connection. Together they define the full typed graph.

---

## The Rule

VITAL: Every connection between nodes has a type — the edge stereotype
VITAL: Edge types are universal — same names in every project, every language
VITAL: A connection without a type is an architecture violation — it cannot be validated
BANNED: Unnamed or ad-hoc connections between modules
BANNED: Inventing new edge types for roles that already have one

## Edge Dictionary

### Code Edges

| Edge type | Direction | Meaning |
|-----------|-----------|---------|
| `import` | A → B | A depends on B (static module dependency) |
| `props` | parent → child | Data passed down (in property, function arg, struct field) |
| `callback` | child → parent | Event emitted up (callback, closure, return value) |
| `dispatch` | adapter → core | Business logic invocation |
| `result` | core → adapter | Return value from business logic |
| `io` | gateway → external | Crosses system boundary (disk, network, process) |
| `platform` | any → pal | Platform-abstracted operation |
| `sibling` | child → child | ✗ always invalid — routes through parent |

### Rule Edges

| Edge type | Meaning |
|-----------|---------|
| `requires` | Must be loaded before this node is safe to use |
| `feeds` | Will be affected by changes to this node |
| `related` | Read-only context — no edit authority |

## Adjacency Table

### Layer-to-Layer

| From | Edge | To | Valid |
|------|------|----|-------|
| `ui` | `callback` | `adapter` | ✓ events up |
| `adapter` | `props` | `ui` | ✓ data down |
| `adapter` | `dispatch` | `core` | ✓ |
| `core` | `result` | `adapter` | ✓ |
| `core` | `platform` | `pal` | ✓ |
| `adapter` | `io` | `gateway` | ✓ |
| `gateway` | `io` | external | ✓ |
| `gateway` | `platform` | `pal` | ✓ |
| `shared` | `import` | any layer | ✓ cross-cutting |
| `ui` | any | `core`, `gateway`, `pal` | ✗ |
| `core` | any | `ui`, `adapter`, `gateway` | ✗ |
| `pal` | any | any layer above | ✗ |
| `gateway` | any | `ui`, `adapter` | ✗ |

### Module-to-Module (within UI layer)

| From | Edge | To | Valid |
|------|------|----|-------|
| mother | `props` | any child | ✓ always |
| any child | `callback` | mother | ✓ always |
| `callbacks` | `import` | `views` (types only) | ✓ |
| `views` | `props` | `components` | ✓ |
| `components` | `callback` | parent view | ✓ |
| `tokens` | `import` | any UI node | ✓ read-only values |
| child | `sibling` | child | ✗ always |
| `overlays` | `import` | `views` | ✗ |

### Module-to-Module (within backend layers)

| From | Edge | To | Valid |
|------|------|----|-------|
| `mod.rs` | `props` | child module | ✓ mother wires children |
| child module | `result` | `mod.rs` | ✓ returns to mother |
| child module | `import` | sibling child | ✗ routes through mother |
| child module | `import` | `types` (same parent) | ✓ shared types |

## Lookup

```
1. Source node stereotype
2. Target node stereotype
3. Find the row → valid or not
4. No row → invalid
```

RULE: If a connection is not in the table, it is not allowed
RULE: The table is the single source of truth for valid edges
BANNED: Connections justified by "it works" — if the table says no, it is no

RESULT: Node types + edge types + adjacency = complete typed graph specification
REASON: A typed graph can be validated mechanically — the missing step is the graph builder


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
