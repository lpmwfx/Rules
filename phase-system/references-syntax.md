---
tags: [phase-system, references, read-graph, anchors, onboarding, v0.4]
concepts: [read-graph, anchor-syntax, excerpt, knowledge-dag, change-notification]
keywords: [references, anchor, excerpt, rules-mcp, docs-mcp, onboarding, knowledge-dag]
requires: [phase-system/methodology.md, phase-system/folder-conventions.md]
feeds: [phase-system/session-resumption.md]
related: [phase-system/integration.md]
layer: 2
---

# References syntax (read-graph, v0.3)

A part's `references[]` block declares what it reads or needs to be aware of. It's distinct from:

- **Folder placement** (write-graph) — where I write
- **`concurrency.runs_after`** (sequential dep) — what must finish before I start
- **`anti_creep_check.invariants_touched`** (rules-graph) — what invariants my work touches

References is the **read-awareness graph**: what files/sections inform my work without me modifying them.

## Schema

```json
"references": {
  "items": [
    {
      "path": "src/server/auth/bearer.ts",
      "anchor": "",
      "why": "Server-OAuth-flow I read but don't modify"
    },
    {
      "path": "proj/data/architecture.json",
      "anchor": "invariants",
      "why": "Check invariants before commit"
    },
    {
      "path": "research/p1.5-mistral.json",
      "anchor": "decisions",
      "why": "Mistral-research decisions affect my auth-token storage choice"
    },
    {
      "path": "rules-mcp:global/edge-types.md",
      "anchor": "",
      "why": "Edge-type convention from rules MCP"
    }
  ]
}
```

## Path syntax

| Form | Meaning | Example |
|---|---|---|
| `relative/from/repo/root` | File in this repo | `src/server/auth/bearer.ts` |
| `relative/in/phase-data/` | File in same `<n>-data/` folder | `research/p1.5-mistral.json` (when self is in `pwa/`) |
| `<mcp-name>:<path>` | External MCP source | `rules-mcp:global/edge-types.md`, `docs-mcp:auth/oauth-flows.md` |
| `https://...` | External URL | `https://docs.mistral.ai/...` |

## Anchor syntax

The `anchor` field narrows the reference to a part of the file:

| Anchor | Resolves to | Example |
|---|---|---|
| empty `""` | Whole file | `path: 'src/MANUAL.md', anchor: ''` |
| markdown heading slug | `## Heading-Name` → `heading-name` | `path: 'src/MANUAL.md', anchor: 'oauth-flows'` |
| JSON-pointer-like key | Top-level JSON key | `path: 'proj/data/architecture.json', anchor: 'invariants'` |
| arbitrary section name | Whatever the file uses | `path: 'spec.md', anchor: 'state-machine'` |

The anchor is *advisory* — readers should look at the named section first but may need wider context. Anchor lookups don't have to be programmatic; their main value is documentation and change-notification scope.

## Three use modes

### 1. Session onboarding

When a new session takes over a part (because the previous session ended or the part was claimed by a different agent), the `references[]` list is the **bring-up stack**. Read those before reading the part's plan or content.

```
new session opens pwa/p1.5-oauth-fix.json:
  → read references[] in order:
    1. src/server/auth/bearer.ts (server-side OAuth, what I'm not changing)
    2. src/MANUAL.md#oauth-flows (canonical doc)
    3. proj/data/architecture.json#invariants (rules-of-system)
  → now read part_meta + scope + content + plan
  → I'm grounded
```

Without `references[]`, every new session re-discovers what to read, often missing critical context.

### 2. Change notification

When a referenced file is modified while I'm working, my assumptions may be stale. A future tool can scan all active parts (`status: in_progress`) and flag references that point to recently-changed files:

```bash
# pseudo-tool
for active_part in $(find proj/PHASE -name '*.json' | jq -r 'select(.status == "in_progress")'); do
  for ref in $(jq -r '.references.items[]' $active_part); do
    if git log --since="$(jq -r '.lockedAt' $active_part)" --name-only | grep -q "${ref.path}"; then
      echo "ALERT: $active_part references ${ref.path} which was modified since lock"
    fi
  done
done
```

This is opt-in tooling — the schema enables it.

### 3. Knowledge-DAG (audit trail)

When a phase closes, `references[]` documents *where the decisions came from*. Combined with `result.handoff_to`, you can trace knowledge flow:

- This part's decisions were informed by `proj/data/architecture.json#invariants` and `rules-mcp:global/edge-types.md`
- Its result handed off to `p2 decisions` and `proj/ink/surreal-json/edges.md`

For long-lived projects this is the only way to reconstruct *why* something was decided years later.

## Differences from related fields

| Field | Direction | Purpose | When to use |
|---|---|---|---|
| `references[]` | Read | Awareness, no sequencing | "I need to know about X but X doesn't need to wait for me, and I don't change X" |
| `concurrency.runs_after` | Sequencing | Logical dependency | "I cannot start until X completes" |
| `concurrency.blocks` | Sequencing (reverse) | Other parts depend on me | "Y waits for me to finish" |
| `anti_creep_check.invariants_touched` | Constraints | Rules my work must respect | "My work must uphold invariant X" |
| Folder placement | Write | What I modify | "My write-set is in this folder" |

A part can have all five filled in for the same target. Example:

```
pwa/p1.5-oauth-fix.json
  references: 'proj/data/architecture.json#invariants'  (I read it)
  anti_creep_check.invariants_touched: ['Frontend kalder aldrig DAL direkte']  (I'm bound by it)
  folder: 'pwa/'  (I write to pwa/)
  concurrency.runs_after: []  (no sequential dep)
```

These are different aspects of the same relationship. References is just the read-awareness slice — small, opt-in, but enables onboarding and change-notification tooling that the other fields don't.

## When to add a reference

Add an entry when:

- You read a file at session-start to ground yourself, AND
- A new session would need to read the same file to do this work, AND
- (Optionally) a change to that file would invalidate your assumptions

Don't add references for every file you happen to read while exploring. Reserve it for *load-bearing* knowledge dependencies.

## When to skip references

Some parts are purely self-contained (e.g. a research-only part producing a fresh document with no prior dependencies). Empty `items: []` is fine — that's an honest signal that the part is greenfield.

Don't fabricate references to look thorough. Empty is honest; padded is misleading.
