---
tags: [phase-system, methodology, research-first, ai-signoff, parallelism, foundation]
concepts: [phase-management, one-product-per-phase, write-domains, split-mode]
keywords: [phase, orchestrator, part, product, usage-tests, signoff, folder-as-write-domain, session-resumption]
related: [project-files/phases-file.md, sid-architecture/README.md, workflow/dev-cycle.md]
layer: 6
---

# phase-system

**Research-first phase definitions with AI-signoff** — a JSON schema and methodology for breaking projects into phases that "just work" before they're called done.

A phase is a unit of work that produces **one product** (a coherent usable thing, not a checklist). The phase begins with research, persists decisions, plans concretely, runs use-application tests by AI throughout, and never closes without explicit AI verification.

Designed to compose with [`ai/anti-scope-creep-rigging`](https://git.lpmintra.com/ai/anti-scope-creep-rigging) — phases reference its `architecture.json` + `dsl-guide.json` for invariants and anti-patterns.

## The problem

LLM-driven dev sessions drift. Without a persistent plan grounded in the actual project, every session starts over: re-discovering decisions, re-investigating known unknowns, re-arguing about scope. "Tasks" in chat disappear when the session ends. TODO files are too thin — they list tasks but not why, what was researched, what was decided, what counts as done, or whether AI itself can use the result.

A **phase JSON** captures all of it in one machine-readable file: identity, context, milestone, **the product** (what works at the end), research, decisions, plan, **use-application tests AI runs**, anti-creep checks, MCP/data-layer changes, verification, and **AI-signoff** (AI must verify before phase can close). Future sessions can pick up cold.

## Core principles

1. **One product per phase.** A coherent usable experience, not a checklist of components. If you have multiple products, you have multiple phases.
2. **AI must demonstrate the product.** `product.user_can[]` lists what AI can do with the finished thing. If AI can't do it, the product isn't done.
3. **Research before plan.** Every unknown gets investigated (web/docs/sub-agents) and summarized with sources before any plan step is written. No plans built on guesses.
4. **Decisions are persisted.** Each open question gets candidates, an answer, a rationale, and a `lands_in` field telling future sessions where the answer was written down.
5. **Use-application tests, not just unit tests.** `usage_tests[]` are scenarios AI must be able to perform with the running product. Added throughout the phase. AI runs and reports.
6. **No phase closes without AI signoff.** `ai_signoff.ai_verified=true` requires AI to have run usage_tests + verification and made a concrete statement: "I did X, Y, Z and it works."
7. **Failed verification blocks done.** Either fix or explicitly move to a new phase with reasoning in `issues_logged`.

## Quick start

### 1. Copy the template

```bash
cp standard-phase.json your-project/proj/PHASE/<n>-data/phase.json
```

### 2. Fill in order

```
identity → context → milestone → product
        → research (parallel sub-agents per topic)
        → decisions (close all open ones)
        → plan (steps with concrete pass criteria)
        → usage_tests (what AI must be able to do)
        → anti_creep_check (invariants, anti_patterns)
        → mcp_rules + data_layer_changes
```

Set `identity.status: 'ready'` when the above is complete. Then start work; status becomes `active`.

### 3. Run the phase

Each `plan.steps[]` has a `pass` criterion. Status moves `pending → in_progress → completed`. AI runs `usage_tests` continuously as functionality lands.

### 4. Close the phase

When all `verification.checks` and `usage_tests` are green:

- AI writes `ai_signoff.ai_statement` (concrete: "I did X, Y, Z, it works")
- Sets `ai_verified: true`
- User reviews and sets `user_approved: true`
- Snapshot of project's `architecture.json` saved into `data_layer_changes.architecture_snapshot_path`
- Phase status → `done`

## Schema

See [`standard-phase.json`](standard-phase.json). Every section has `$hint` (what to write) + `$example` (concrete sample).

Top-level sections:

| Section | Purpose |
|---|---|
| `identity` | phase number, id, title, status, owner, timestamps |
| `context` | problem, outcome, blockedBy, blocks |
| `milestone` | the one measurable end-state criterion (definition of done) |
| `product` | what works at the end; `user_can[]` lists AI-demonstrable capabilities |
| `delivers` | concrete artifacts produced |
| `research` | topics investigated before planning, with sources + open_questions |
| `decisions` | OPS-level decisions with candidates, answer, rationale, lands_in |
| `plan` | step-by-step, with task_type, files, pass-criteria, depends_on |
| `usage_tests` | scenarios AI must be able to perform |
| `anti_creep_check` | invariants touched, anti_patterns to avoid, new ones discovered |
| `mcp_rules` | tools added/changed, AIUX help required, OAuth roles affected |
| `data_layer_changes` | tables, edges, constants, invariants added; snapshot path |
| `verification` | command-level checks proving milestone reached |
| `ai_signoff` | AI's concrete verification statement; user approval |
| `issues_logged` | issues discovered, deferred to other phases |
| `history` | append-only event log |

## Vocabulary alignment with Anthropic Claude Agent SDK

Where the SDK has a term, we use it; where it doesn't, we invent.

| phase-system | Anthropic Agent SDK | Source |
|---|---|---|
| `identity.status` | (analogous to TaskNotificationStatus, extended) | extends with `pending`/`in_progress`/`researching`/`ready`/`active` |
| `identity.description` | `AgentDefinition.description` | match |
| `identity.metadata` | `metadata` | match |
| `context.blockedBy` / `blocks` | DAG via task IDs | match camelCase |
| `plan.steps[].task_type` | `TaskStartedMessage.task_type` | extended for our domain |
| `plan.steps[].subagent_prompt` | `AgentDefinition.prompt` | self-contained briefing |
| `plan.steps[].status` | `TaskNotificationStatus` (`completed`/`failed`/`stopped`) + `pending`/`in_progress` | aligned |
| `phase` (the unit itself) | (no SDK equivalent) | invented |
| `product` | (no SDK equivalent) | invented |
| `milestone.criterion` | "definition of done" (best-practice prose) | invented as schema |
| `usage_tests` | (no SDK equivalent) | invented |
| `ai_signoff` | (no SDK equivalent) | invented |
| `anti_creep_check` | (composes with [anti-scope-creep-rigging](https://git.lpmintra.com/ai/anti-scope-creep-rigging)) | external compose |

Plan-step `task` field can be structured as markdown using Claude Code's Plan Mode convention: `## Problem | ## Approach | ## Changes | ## Verification`.

## Composing with anti-scope-creep-rigging

The two methodologies are designed to work together:

- **anti-scope-creep-rigging** sets the *rules of the system* (architecture, invariants, anti-patterns) — frozen, slow-changing, locked
- **phase-system** runs *changes through the system* — fast-moving, per-feature, persistent

Each phase JSON has an `anti_creep_check` section that points back to `proj/data/current/architecture.json` + `proj/data/current/dsl-guide.json`. New invariants or anti-patterns discovered during a phase are logged in `new_*_discovered[]` and proposed as a snapshot update at phase-done (since `proj/data/` is locked readonly).

## Naming convention (v0.3)

Three rules:

1. **One folder per major phase.** All `p<n>.x` files (orchestrators + sub-orchestrators + parts) live in `proj/PHASE/<n>-<label>/` where `<label>` is either the literal `data` (default, generic) or a meaningful name (`fundament`, `ink-tools`, `voice-pipeline`). The leading `<n>-` is the only fixed part — pick whichever label gives the best at-a-glance scanning. **Never** create `<n.5>-…/` or `<n.6>-…/` — sub-phases share the major folder.
2. **All filenames start with `p<n>-` prefix.** `phase.json` is forbidden — collides across phases and gives no parallelism affordance.
3. **Sub-folders inside `<n>-data/` are write-domains.** Each sub-folder name should match a layer (or sub-layer) in your project's `proj/data/current/architecture.json`. Same sub-folder = serial work. Different sub-folders = parallel by construction.

```
proj/PHASE/
  standard-phase-orchestrator.json   ← orchestrator template
  standard-phase-part.json           ← part template (split-mode)
  1-fundament/                       ← <n>-<label>/ — label is free
    p1.json                          ← phase-1 orchestrator (single or split)
    p1.5.json                        ← sub-orchestrator (split-mode index)
    p1.6.json                        ← sub-orchestrator
    pwa/                             ← write-domain folder (matches arch layer)
      p1.5-oauth-fix.json
    research/
      p1.5-mistral.json
      p1.6-ink-as-surreal-json.json
    ops/
      (intet aktivt)
  2-ink-tools/                       ← named for at-a-glance scanning
    p2.json
    pwa/
      p2-tts-ui.json
    server/
      p2-tts-pipeline.json
    external/
      p2-mistral-tts-integration.json
```

The `<label>` after `<n>-` is free: `1-data`, `1-fundament`, `1-setup` — pick what helps a fresh reader scan `ls proj/PHASE/`. The orchestrator's `identity.title` is the canonical title; the folder label is just a navigation aid.

## Folder-as-write-domain (v0.3)

Parallelism is **derived**, not declared:

- Two parts in **different** sub-folders can run concurrently (assumed disjoint write-sets).
- Two parts in the **same** sub-folder are serial by default (assumed write-conflict).
- If two same-folder parts genuinely don't conflict, the folder is too coarse — split it (`pwa/auth/` + `pwa/editor/`).
- Folder names should match an existing layer in `proj/data/current/architecture.json` from anti-scope-creep-rigging. If a folder doesn't map to a layer, either add the layer first or rename the folder. This couples phase-system to your project's structural map.

`parts.items[].parallel_with` is gone in v0.3. Folder placement is the parallelism declaration.

## References (read-graph, v0.3)

A part's `references[]` block lists what it reads/needs-to-be-aware-of — distinct from `concurrency.runs_after` (sequential dep) and from folder-derived write-conflicts.

```json
"references": {
  "items": [
    {"path": "src/server/auth/bearer.ts", "anchor": "", "why": "Server-OAuth-flow I read but don't modify"},
    {"path": "proj/data/current/architecture.json", "anchor": "invariants", "why": "Check invariants before commit"},
    {"path": "research/p1.5-mistral.json", "anchor": "decisions", "why": "Mistral-research decisions affect my auth choice"},
    {"path": "rules-mcp:global/edge-types.md", "anchor": "", "why": "Edge-type convention from rules MCP"}
  ]
}
```

Anchor syntax: `path#section` for fine-grained reference into part of a file (markdown headings, JSON-pointer-style keys). External MCP references prefix with `rules-mcp:`, `docs-mcp:`, etc.

Three use modes:

1. **Session onboarding**: a new session taking over a part reads `references.items[]` as the bring-up stack
2. **Change notification**: when a referenced file updates while I'm working, re-check assumptions
3. **Knowledge-DAG**: documents where my decisions came from (audit trail)

## Single vs split mode

- **Single-mode** (default): `parts.mode: 'single'`. All phase content lives in `p<n>.json`. Use for small phases, single-author work.
- **Split-mode**: `parts.mode: 'split'`. `p<n>.json` becomes a thin orchestrator holding identity/context/milestone/product/ai_signoff and `parts.items[]` indexing the part-files. Each part lives in a write-domain folder and can be worked on concurrently with parts in other folders.

Use split-mode when:
- Multiple sessions or human-AI pairs work on the same phase concurrently
- One session spawns sub-agents on independent parts (research vs implementation vs verification)
- Different domains within one phase have minimal coupling

## Repo layout for projects using this

```
your-project/
  proj/
    data/                                       ← anti-scope-creep-rigging (locked)
      architecture.json
      dsl-guide.json
    PHASE/
      standard-phase-orchestrator.json
      standard-phase-part.json
      1-fundament/
        p1.json                                 ← phase 1 orchestrator
        p1.5.json                               ← sub-orchestrator
        p1.6.json
        pwa/p1.5-oauth-fix.json
        research/p1.5-mistral.json
        research/p1.6-ink-as-surreal-json.json
      2-ink-tools/
        p2.json
        ...
    PHASES                                      ← human-facing index
    RULES                                       ← project-local methodology
```

## Status

v0.4.2 — attribution-bug fix: locked_session_log is now retained as attribution after completion (was being cleared, losing audit-trail). New `worked_by_sessions[]` array accumulates every session that touched the part.

## v0.4.2 additions over v0.4

- **`worked_by_sessions[]`** on parts: append-only log of every Claude-session that worked on the part (session_id, log_path, period, role, summary). Multiple sessions touching same part = multiple entries. Primary audit-trail.
- **`close_protocol` revised**: `locked_by_session` / `locked_session_log` / `locked_at` are NOT cleared on completion — they remain as attribution for the last/closing session. Lock-status is communicated via `part_meta.status` instead (`in_progress` = active lock; `completed`/`stopped` = released, but session info preserved).
- **Bug-fix rationale**: previous `close_protocol` cleared the lock-fields on completion, which lost the session-log link to the work that was actually done. v0.4.2 keeps the link forever.

## v0.4 additions over v0.3

- **`concurrency.locked_session_log`** on parts: absolute path to the worker's `~/.claude/projects/.../<session-id>.jsonl`. Enables `claude --resume <session-id>` recovery for interrupted work — a stale lock is no longer a stuck lock.
- **`references.items[].excerpt`** on parts: pre-distilled quote/summary (~500 chars max) from the referenced file. New sessions get insight without chasing every link.
- **`references.items[].excerpt_stale`** on parts: bool flag set when the referenced file changes after the excerpt was written (combined with change-notification tooling).
- **`close_protocol`** on both orchestrator and part: explicit step-by-step close-out the agent executes WITHOUT asking the user. "Should I close this now?" prompts are eliminated — the protocol fires automatically when criteria are met. User approval (separate step) still required after AI signoff.
- **Computed `identity.status` aggregation**: in split-mode, orchestrator status is derived from parts statuses (`planned` → `active` → `done`).

## Files

- [`standard-phase-orchestrator.json`](standard-phase-orchestrator.json) — orchestrator template (single or split mode)
- [`standard-phase-part.json`](standard-phase-part.json) — part template
- [`docs/methodology.md`](docs/methodology.md) — full workflow, principles, parallelism patterns
- [`docs/integration.md`](docs/integration.md) — how to combine with anti-scope-creep-rigging
- [`docs/folder-conventions.md`](docs/folder-conventions.md) — folder-as-write-domain rules + layer mapping
- [`docs/references-syntax.md`](docs/references-syntax.md) — anchor syntax + excerpt for the read-graph
- [`docs/session-resumption.md`](docs/session-resumption.md) — `~/.claude/.../<session-id>.jsonl` audit + `claude --resume` recovery
- [`examples/`](examples/) — phase JSON examples from real projects
