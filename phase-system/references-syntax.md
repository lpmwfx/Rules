---
tags: [phase-system, references, read-graph, anchors, onboarding, v0.4]
concepts: [read-graph, anchor-syntax, excerpt, knowledge-dag, change-notification]
keywords: [references, anchor, excerpt, rules-mcp, docs-mcp, onboarding, knowledge-dag]
requires: [phase-system/methodology.md, phase-system/folder-conventions.md]
feeds: [phase-system/session-resumption.md]
related: [phase-system/integration.md]
layer: 2
---
# References syntax — the read-graph (v0.3+, v0.4 excerpts)

> A part's `references[]` declares what it reads or needs to be aware of. Distinct from folder placement (write-graph), `concurrency.runs_after` (sequential deps), and `anti_creep_check.invariants_touched` (rules-graph).

References is the **read-awareness graph**: what files/sections inform the part without it modifying them.

---

## Schema

```json
"references": {
  "items": [
    {
      "path": "src/server/auth/bearer.ts",
      "anchor": "",
      "why": "Server-OAuth flow I read but don't modify",
      "excerpt": "",
      "excerpt_stale": false
    },
    {
      "path": "proj/data/architecture.json",
      "anchor": "invariants",
      "why": "Check invariants before commit",
      "excerpt": "Top invariants: Frontend never calls DAL directly. All SID-generation in one generator. PWA login cookie SameSite=Lax.",
      "excerpt_stale": false
    },
    {
      "path": "rules-mcp:global/edge-types.md",
      "anchor": "",
      "why": "Edge-type convention from rules MCP",
      "excerpt": "",
      "excerpt_stale": false
    }
  ]
}
```

---

## Core rules

RULE: References is distinct from `runs_after` (sequencing) and from folder placement (write)
RULE: Anchor points to a section of the file; it is *advisory*, not programmatically enforced
RULE: Excerpt (v0.4) is a pre-distilled quote or summary (~500 chars max) so new sessions get insight without chasing every link
RULE: Planner fills `excerpt` once; later sessions get insight for free
RULE: When a referenced file changes after the excerpt was written, set `excerpt_stale: true` (paired with change-notification tooling)
RULE: External MCP sources prefix the path with `<mcp-name>:` — e.g. `rules-mcp:global/edge-types.md`, `docs-mcp:auth/oauth-flows.md`

BANNED: Adding references for every file you happen to read while exploring — reserve for load-bearing knowledge dependencies
BANNED: Fabricating references to look thorough — empty `items: []` is an honest signal for greenfield parts

---

## Path syntax

| Form | Meaning | Example |
|---|---|---|
| `relative/from/repo/root` | File in this repo | `src/server/auth/bearer.ts` |
| `relative/in/phase-data/` | File in same `<n>-<label>/` folder | `research/p1.5-mistral.json` (when self is in `pwa/`) |
| `<mcp-name>:<path>` | External MCP source | `rules-mcp:global/edge-types.md`, `docs-mcp:auth/oauth-flows.md` |
| `https://...` | External URL | `https://docs.mistral.ai/...` |

---

## Anchor syntax

| Anchor | Resolves to | Example |
|---|---|---|
| empty `""` | Whole file | `{path: 'src/MANUAL.md', anchor: ''}` |
| markdown heading slug | `## Heading-Name` → `heading-name` | `{path: 'src/MANUAL.md', anchor: 'oauth-flows'}` |
| JSON-pointer-like key | Top-level JSON key | `{path: 'proj/data/architecture.json', anchor: 'invariants'}` |
| arbitrary section name | Whatever the file uses | `{path: 'spec.md', anchor: 'state-machine'}` |

---

## Three use modes

### 1. Session onboarding

When a new session takes over a part, `references[]` is the **bring-up stack**. Read before plan or content.

```
new session opens pwa/p1.5-oauth-fix.json:
  → read references[] in order:
    1. src/server/auth/bearer.ts (server-side OAuth, what I'm not changing)
    2. src/MANUAL.md#oauth-flows (canonical doc)
    3. proj/data/architecture.json#invariants (rules-of-system)
  → now read part_meta + scope + content + plan
  → grounded
```

RULE: Without `references[]`, every new session re-discovers what to read and often misses critical context

v0.4 improvement: with pre-filled `excerpt` fields, the session reads the part-file inline and already has the gist — only opens referenced files when diving deeper.

### 2. Change notification

When a referenced file is modified while the part is active, assumptions may be stale. A tool can scan active parts (`status: in_progress`) and flag references pointing at recently-changed files:

```bash
# pseudo-tool
for active_part in $(find proj/PHASE -name '*.json' | jq -r 'select(.status == "in_progress")'); do
  for ref in $(jq -r '.references.items[]' $active_part); do
    if git log --since="$(jq -r '.locked_at' $active_part)" --name-only | grep -q "${ref.path}"; then
      echo "ALERT: $active_part references ${ref.path} modified since lock"
      # set references.items[].excerpt_stale = true
    fi
  done
done
```

This is opt-in tooling — the schema enables it.

### 3. Knowledge-DAG (audit trail)

When a phase closes, `references[]` documents *where the decisions came from*. Combined with `result.handoff_to`, you can trace knowledge flow across phases — the only way to reconstruct *why* something was decided years later.

---

## Differences from related fields

| Field | Direction | Purpose | When to use |
|---|---|---|---|
| `references[]` | Read | Awareness, no sequencing | "I need to know about X but X doesn't wait for me, and I don't change X" |
| `concurrency.runs_after` | Sequencing | Logical dependency | "I cannot start until X completes" |
| `concurrency.blocks` | Sequencing (reverse) | Others depend on me | "Y waits for me" |
| `anti_creep_check.invariants_touched` | Constraints | Rules my work must respect | "My work must uphold invariant X" |
| Folder placement | Write | What I modify | "My write-set is in this folder" |

A part can fill all five for the same target — they're different aspects of the same relationship. References is the read-awareness slice.

---

## When to add / skip

RULE: Add a reference when you read a file at session-start to ground yourself AND a new session would need to read the same AND (optionally) a change to that file would invalidate your assumptions
RULE: Empty `items: []` is honest for greenfield research-only parts

BANNED: Padded references that mask a part with no real knowledge dependencies


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
