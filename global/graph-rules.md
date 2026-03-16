---
tags: [graph-position, edit-authority, boundary, rules, overwrite-prevention]
concepts: [edit-authority-rules, graph-position-rules, rule-relationship]
requires: [global/graph-position-paradigm.md]
related: [global/topology.md, global/naming-suffix.md, global/module-tree.md, global/file-limits.md]
keywords: [edit-authority, boundary, requires, feeds, related, VITAL, BANNED, position-determines-authority, adding-rules]
layer: 1
---
# Graph-Position Rules and Relationships

> Position determines authority — the edit boundary is the graph, not intuition

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

RESULT: Every rule has a clear role in the paradigm — no orphaned conventions
REASON: Rules without a position in the system become cargo-cult — followed but not understood
