---
tags: [phase-system, integration, anti-scope-creep-rigging, snapshot, claude-md]
concepts: [rules-of-system, changes-through-system, snapshot-evolution, two-file-rigging]
keywords: [architecture.json, dsl-guide.json, anti_creep_check, snapshot, proj/data, invariants]
requires: [phase-system/methodology.md]
related: [phase-system/folder-conventions.md, project-files/phases-file.md]
layer: 2
---

# Integration with anti-scope-creep-rigging

[`ai/anti-scope-creep-rigging`](https://git.lpmintra.com/ai/anti-scope-creep-rigging) and `phase-system` are two halves of the same approach to AI-assisted development:

- **anti-scope-creep-rigging** captures the *rules of the system* — what exists, what must not be done, what the right moves look like. It's slow-changing, dense, locked.
- **phase-system** runs *changes through the system* — what we're building now, why, and how AI verifies it works. Fast-moving, per-product.

You can use either alone; they shine together.

## The two-file rigging recap

A project using anti-scope-creep-rigging has:

```
proj/data/
  architecture.json    ← layers, nodes, edges, forbidden, invariants
  dsl-guide.json       ← glossary, anti_patterns, how_to_add, minimal_example
```

These are **the project's mental model for AI**. Read them at session start.

Recommendation: lock `proj/data/` readonly (`chmod -R a-w proj/data/`). Changes go through phase-system snapshots, not direct edits.

## How phases reference rigging

Every phase JSON has an `anti_creep_check` section:

```json
"anti_creep_check": {
  "invariants_touched": [
    "Frontend kalder aldrig SurrealDB direkte"
  ],
  "anti_patterns_to_avoid": [
    "from-scratch MCP/OAuth/PWA-boilerplate",
    "schema-først migration"
  ],
  "how_to_add_recipes_used": [
    "Nyt authoring-MCP-tool"
  ],
  "new_anti_patterns_discovered": [],
  "new_invariants_discovered": []
}
```

When AI plans a step, it cross-references the rigging:

1. **Which invariant does this touch?** → `invariants_touched`
2. **Is this an anti_pattern I'm about to commit?** → check `anti_patterns_to_avoid`
3. **Which `how_to_add` recipe applies?** → `how_to_add_recipes_used`
4. **Did I just learn something the rigging doesn't capture yet?** → log in `new_*_discovered`

The self-check questions in `dsl-guide.json → for_ai_sessions.self_check_*` are the AI's pre-commit filter.

## The snapshot pattern

`proj/data/` is locked. So how do invariants and anti-patterns evolve?

Through **snapshots at phase-done**. When a phase closes:

1. AI proposes new entries based on `anti_creep_check.new_*_discovered`
2. User reviews and approves
3. New snapshot directory created: `proj/data-<YYYYMMDD-HHMM>/` (or version like `proj/data-v2/`)
4. New JSONs written there, with the proposed additions merged in
5. The new snapshot becomes the current `proj/data/` (old one renamed to `proj/data-<previous>/` or kept as version)
6. Path stored in `data_layer_changes.architecture_snapshot_path`

This forces deliberate evolution. The rigging doesn't drift — it gets revised between phases by explicit decision.

## CLAUDE.md as the entry point

Both methodologies converge in `CLAUDE.md` at repo root:

```markdown
# <project>

Before proposing or changing anything, read:

- `proj/data/current/architecture.json` — structural map (locked)
- `proj/data/current/dsl-guide.json` — glossary, anti_patterns, how_to_add (locked)
- `proj/RULES` — phase-system workflow + project-local methodology
- `proj/PHASE/<active>-data/phase.json` — what we're working on right now

The current phase status, plan, usage_tests, and known issues all live in the active phase JSON.
```

A new session reads these four files and is grounded.

## Workflow with both

```
1. New phase needed
   ↓
2. Copy standard-phase.json → proj/PHASE/<n>-data/phase.json
   ↓
3. Fill identity + context + milestone + product
   ↓
4. Research (parallel sub-agents) ──→ load proj/data/ for context
   ↓
5. Resolve decisions
   ↓
6. Write plan ──→ for each step, run anti_creep_check against proj/data/
   ↓
7. Define usage_tests
   ↓
8. status: ready → user authorizes → status: active
   ↓
9. Execute steps, run usage_tests, log issues + new_*_discovered
   ↓
10. All checks green → AI ai_signoff → user approves
    ↓
11. If new_*_discovered non-empty → propose new proj/data-<date>/ snapshot
    ↓
12. status: done. Onward to next phase.
```

## Why both

The rigging answers: **what does this system look like and what mustn't be done in it?**

The phase JSON answers: **what are we building right now, and how do we know it works?**

A project with rigging but no phase system: the AI knows the rules but every session re-litigates what to build.

A project with phases but no rigging: each phase is well-planned but the AI keeps drifting back to default-app reflexes inside each phase.

Together: the rules of the system are stable and clear; the changes through it are persistent and verified.
