---
tags: [phase-system, methodology, lifecycle, workflow, research-first, signoff]
concepts: [one-product-per-phase, research-before-plan, usage-tests, ai-signoff, split-mode]
keywords: [phase, product, research, decisions, plan, usage-tests, verification, signoff, planner, worker]
requires: [phase-system/README.md]
feeds: [phase-system/folder-conventions.md, phase-system/references-syntax.md]
related: [phase-system/integration.md, project-files/phases-file.md]
layer: 2
---

# Methodology

## What a phase is

A phase is a unit of work bounded by **one product**. Not a deliverable list — a single coherent thing a user (or AI as a user) can demonstrably use at the end. If you can't point at it and say "this works, here's how to use it", you don't have a product, you have a partial component.

Phases come in series. What a project's phases are gets discovered phase by phase, not designed up front. Phase 2 emerges from what phase 1 produced. The full roadmap is `proj/PHASES` (a human-facing index); the executable definition lives per phase in `proj/PHASE/<n>-data/phase.json`.

## The lifecycle

```
planned → researching → ready → active → done
                                       ↘ aborted
```

- **planned**: identity + context + milestone + product written; nothing else
- **researching**: research topics being investigated, decisions being made
- **ready**: research closed, decisions resolved, plan written, usage_tests defined; user has reviewed and authorized start
- **active**: dev in progress; plan steps and usage_tests being executed
- **done**: all verification.checks + usage_tests green, AI signed off, user approved
- **aborted**: phase abandoned; reasoning logged in `history`

## The seven workflow steps

### 1. Open with intent

Fill `identity` (number, id, title), `context` (problem, outcome), and `milestone` (the one definition-of-done criterion). This takes minutes. If you can't write it, you don't yet have a phase — you have an idea.

### 2. Define the product

Write `product`. This is the most-skipped section and the one that catches the most scope creep. Force yourself to write `product.user_can[]` — a concrete list of what AI (or a user) can do with the finished thing. If the list is fuzzy, the phase is fuzzy.

### 3. Research before plan

Every unknown gets investigated **before** any plan step is written. Use parallel sub-agents for distinct topics. Each `research.topics[]` entry: summary, sources (URLs), open_questions. Open questions block plan; resolve via decisions or further research.

This is the discipline the methodology enforces: no plan built on guesses. If it's unclear how Mistral handles a specific edge case, you research it. If you can't get clarity, you log it as an open question and either resolve via a decision (we'll use Mistral Small for now and accept the risk) or you carve out research as a phase of its own.

### 4. Resolve decisions

OPS-level questions: which library, which domain, which auth provider, which storage. Each decision needs candidates (at least two), an answer, a rationale (why this candidate), and `lands_in` (where the decision is persisted so future sessions can find it).

Open decisions block plan. Decisions deferred to a future phase get logged as `issues_logged` with that phase named.

### 5. Write the plan

Step-by-step. Each `plan.steps[]` has:

- `task`: what to do (use markdown `## Problem / ## Approach / ## Changes / ## Verification` for complex steps)
- `task_type`: `local_bash | local_agent | remote_agent | data | config | git`
- `files`: which files this touches
- `code_changes`: prose summary; "none" is a valid value
- `depends_on`: other step IDs
- `subagent_prompt`: if delegated, the self-contained briefing
- `pass`: concrete testable criterion
- `status`: `pending → in_progress → completed | failed | stopped`

No step without a testable pass. If you can't write one, the step isn't concrete enough.

### 6. Define usage tests

`usage_tests[]` are scenarios AI must be able to perform with the running product. Different from `verification`:

- **verification**: does the system reach the right end-state? (curl /health → 200)
- **usage_tests**: can AI use the system for its purpose? (AI calls whoami via Claude.ai connector and gets ai@lpmwfx.com)

Add usage tests up front for the product, then add more as functionality lands. AI runs them and reports `actual` + `status`. Failing usage tests block phase-done.

### 7. Execute, verify, sign off

While `status: active`:
- Step statuses progress
- AI runs usage tests as features land
- Issues discovered get logged in `issues_logged` with severity
- New invariants/anti-patterns get logged in `anti_creep_check.new_*_discovered`

Before phase-done:
- ALL `verification.checks` green (or explicitly moved)
- ALL `usage_tests` green (or product is incomplete)
- AI writes `ai_signoff.ai_statement`: concrete, "I did X, Y, Z and it works" — not "looks good"
- AI sets `ai_verified: true`
- User reviews and sets `user_approved: true`
- Snapshot of `proj/data/architecture.json` saved into `data_layer_changes.architecture_snapshot_path`
- Status → `done`

## Principles in tension

### Research vs. momentum

The discipline is research-first. The temptation is to start coding. The trick is to spawn parallel research sub-agents while you write the easy sections (identity, context, milestone, product) — so research fills in by the time you need it for the plan.

### Concreteness vs. flexibility

Every plan step needs a testable pass. But over-specification kills agility. The rule of thumb: pass is the *outcome* not the *implementation*. "scene_create tool returns SID for new scene" is a good pass; "function exported from src/server/tools/scene.ts at line 42" is over-specified.

### Phase boundaries vs. continuous work

Strong phase boundaries (one product per phase, signoff required) seem heavy. They're not — they exist precisely to keep individual phases small. If a phase grows past one product, split it. If a phase needs research mid-execution to continue, pause status to `researching` and resume when resolved.

### AI signoff vs. human autonomy

The signoff is AI saying "I have run the tests and the product works for me as a user". This is *not* AI approving its own work — the user still approves. The point is to force AI to actually use the product before declaring success, instead of claiming success because tests passed. Tests pass and products are still broken every day; usage_tests + signoff catch that gap.

### Three roles: DevOps-session, Orchestrator-session, Agents (most important)

In practice, there are *two* kinds of main-session a user runs with, plus ephemeral agents spawned by either. Keeping these three roles distinct is the single most important workflow discipline in agent-heavy projects.

| Role | What it is | What it does | Talks to user? |
|---|---|---|---|
| **DevOps-session** | The strategic main-session the user holds aidevops-dialog with | Decisions, approvals, arguments, memory maintenance, updating `CLAUDE.md` + upstream methodology, choosing direction. Persists across sessions via memory + project docs. | **Yes** — this is where dialog lives |
| **Orchestrator-session** | A separate main-session that executes phases | Takes locks on part-files, runs plan-steps, closes parts, commits. Only talks to user where schema requires it (decision-resolution, usage_tests review, user_approved). Not a strategist. | Only for schema-driven checkpoints |
| **Agents** (Explore, Plan, general-purpose, specialized workers) | Ephemeral workers spawned by *either* main-session | One scoped task: search, write code, verify, research. No memory across invocations. | **Never** |

**Concrete rules:**

- **Sub-agents do**: search codebase, write code, run verification, draft research summaries, produce structured reports
- **Main sessions do**: present options to user, ask clarifying questions, accept decisions, request approvals, argue a position
- **Sub-agents must not**: ask the user for input, wait on human decisions, treat the user as a loop partner
- **DevOps-session must not**: silently cross into phase-execution. If phase-steps need running, either spawn an agent for the narrow piece OR flag to the user that an orchestrator-session should pick it up.
- **Orchestrator-session must not**: drift into strategic dialog outside schema checkpoints. If strategy is needed, surface it back to the DevOps-session via memory or explicit hand-off.

Why: the user engages aidevops-dialog with a main Claude that carries conversational context and persistent memory. Agent outputs are filtered and structured — useful as input to a main session's reasoning, but not a substitute for it. An agent asking "should I do X or Y?" fragments the conversation and loses the why-tree the user has built up. Equally, mixing strategic dialog into an orchestrator-session that's mid-execution turns the phase-artifact into chat scratch.

**The minimal rule to remember**: if a task requires a yes/no or judgment call from the user, it belongs in a main-session — and specifically the right one (DevOps for strategy, Orchestrator only for schema-mandated checkpoints). Agents investigate and report; they never decide.

This principle is workflow-cultural, not schema-enforced. It appears here because most drift in agent-heavy workflows starts with "the agent asked the user" or "the orchestrator drifted into strategy", and ends with fragmented context and contradictory decisions across threads.

## Anti-patterns this methodology prevents

- **Phantom done**: tests pass, declared done, product doesn't actually work for its intended use. Caught by usage_tests + ai_signoff.
- **Drift between sessions**: each new session re-discovers what's been decided. Caught by persisted decisions with `lands_in`.
- **Plans built on guesses**: research never happened, plan steps reference unknown behavior. Caught by research-before-plan ordering.
- **Scope creep mid-phase**: feature ideas grow during execution. Caught by single-product-per-phase + issues_logged for deferral.
- **Untracked discoveries**: AI finds an issue or invariant during work, doesn't capture it. Caught by `issues_logged` and `anti_creep_check.new_*_discovered`.

## Parallelism via folder placement (v0.3)

A phase can be a single file or a directory tree of part-files organized by write-domain. The structure enables a fundamental workflow split: **planners build phases; workers execute parts in parallel.**

### The planner/worker workflow

| Role | Session-type | What they do |
|---|---|---|
| **Planner** | One Claude in plan-mode | Creates `p<n>.json` + sub-orchestrators + part-files. Fills research, decisions, plan, usage_tests, references. Sets `status: ready`. Adds no locks. The phase is now "shelf-ready" — fully informed, executable, can sit untouched until a worker picks it up. |
| **Worker** | Any Claude Code CLI session (or human-AI pair) | Opens `proj/PHASE/<n>-data/`, finds an unclaimed part-file (`locked_by_session: null`), takes the lock, reads `references[]` as onboarding stack, executes plan-steps, updates status, runs usage-tests, releases lock. |
| **Parallel worker** | Another Claude Code CLI session simultaneously | Picks a part in a *different folder* — assumed safe by construction (no write-conflict). Reads its own `references[]`. Runs concurrently. |
| **Orchestrator-keeper** | Any session that touches a part | Updates the orchestrator's `parts.items[].status` to mirror the part's own status. The orchestrator is the at-a-glance view of phase progress. |

This is what folder-as-write-domain + advisory locks + references-as-read-graph enables: phases become **artifacts** that one Claude can build offline and other Claudes can pick up later, in parallel, without coordination overhead.

### When to split (use split-mode)

- Multiple Claude Code sessions or human-AI pairs need to work on the same phase concurrently
- One Claude wants to spawn parallel sub-agents on independent slices (research vs implementation vs verification)
- Different domains within one phase have minimal write-coupling (e.g. PWA bug-fix vs Mistral-research)
- A long-running research part shouldn't block the start of dev work in another folder

When in doubt, start single-mode and split when parallelism actually appears as a need.

### Folder-as-write-domain (parallelism is structural)

See [folder-conventions.md](folder-conventions.md) for full rules. Summary:

- One folder per major phase: `<n>-data/` holds all `p<n>.x` files (no `<n.5>-data/` etc.)
- Sub-folders inside `<n>-data/` are write-domains, named after layers from `proj/data/architecture.json`
- Two parts in **different sub-folders** can run concurrently — assumed disjoint write-sets
- Two parts in the **same sub-folder** are serial by default — assumed write-conflict
- `parallel_with` is **gone** in v0.3. Folder placement is the parallelism declaration.

### Concurrency block (runtime state only)

In v0.3 the `concurrency` block carries only:

- `runs_after: string[]` — logical sequencing (this part waits on another's result, even across folders)
- `blocks: string[]` — reverse: who waits on me
- `locked_by_session: string | null` — advisory lock with session/agent ID
- `locked_at: ISO timestamp | null` — when the lock was taken
- `lock_policy: 'advisory_24h'` — others may steal a lock older than 24h with no status change

No `parallel_with` — that's derived from folder.

### References (read-graph)

See [references-syntax.md](references-syntax.md). Each part's `references[]` lists what it reads/needs-to-be-aware-of:

- Session onboarding: a worker taking a part reads `references[]` as bring-up stack
- Change notification: tooling can flag when a referenced file is modified during active work
- Knowledge-DAG: documents where decisions came from for audit

References uses anchor syntax `path#section` to point into a specific section of a file. External MCP sources prefix with `rules-mcp:`, `docs-mcp:`, etc.

### Splitting a phase into parts (planner workflow)

1. Decide the write-domains (which folders does this phase touch?). Sub-folders should match `architecture.json` layers.
2. Set `parts.mode: 'split'` in `p<n>.json`.
3. For each part:
   - Pick the folder (write-domain). Pick the slug (free naming).
   - Create `<folder>/p<n>-<slug>.json` from `standard-phase-part.json`
   - Fill `part_meta` (incl. `folder`), `scope` (in/out), `references` (read-deps), `content` (relevant slice of orchestrator content)
   - Add an entry to orchestrator's `parts.items[]` with `file: '<folder>/p<n>-<slug>.json'`, `folder`, `slug`, `runs_after` (if any logical dep)
4. Orchestrator keeps: identity, context, milestone, product, ai_signoff, parts index. Each part keeps its own status, history, result.

### Aggregated signoff

In split-mode, `ai_signoff.ai_verified=true` in the orchestrator requires:

- All `parts.items[].status === 'completed'`
- All part-files' verification + usage_tests green
- AI's `ai_statement` references each part's `result.summary`

User approval still required after AI signoff.

### Anti-pattern: hidden coupling between parts

If two parts constantly modify each other's state across folders, they're not actually independent — re-decompose. Parts coordinate through `result.handoff_to` and `references[]`, not through reaching across files.

### Anti-pattern: planner doing worker work

If the planner-session ends up executing plan-steps instead of just describing them, the planner/worker split breaks down. Plan-mode produces a complete artifact; execution happens in subsequent sessions. (Exception: trivial phases where there's no benefit to splitting roles.)

## Closing a part — attribution is forever (v0.4.2)

A part-close is not a cleanup. It is an archival step. Two rules are easy to miss and easy to get wrong:

### Rule 1: Preserve `locked_*` as attribution — do not clear

At close, the closing session's instinct is to clear locks ("the work is done, the lock should go"). That is wrong. The `concurrency.locked_by_session` + `locked_session_log` + `locked_at` fields are the **primary attribution record** for who picked the part up and when. They remain for the life of the file.

```jsonc
// WRONG close:
"concurrency": {
  "locked_by_session": null,   // ← lost the attribution
  "locked_session_log": null,
  "locked_at": null
}

// CORRECT close:
"concurrency": {
  "locked_by_session": "718a2c70-9398-4981-bcd9-e9cf353aa028",  // ← worker's session
  "locked_session_log": "~/.claude/projects/-home-dev-foo/718a2c70-....jsonl",
  "locked_at": "2026-04-15T11:55"
}
```

The `parts.items[<slug>]` mirror in the orchestrator follows the same rule — sync from the part-file, never null out.

### Rule 2: Append to `worked_by_sessions[]` — once per session, per part

Every session that touched the part appends an entry to `worked_by_sessions.items[]`. The closing session MUST append its own entry before setting `status: completed`. This is append-only — you never rewrite history here, only add.

Common roles observed in practice:
- `code-writer` — wrote the implementation (one or more sessions)
- `verifier` — ran usage_tests
- `closer+committer` — finalized status, wrote result, made the git commit
- `code-writer+closer` — same session did both (common for small parts)
- `aborted-worker` — took the lock, produced no output (API crash, blocked, scope shift). Still belongs in the log.

### Why this matters

Without attribution:
- You can't answer "which session produced this code?" weeks later
- Session logs (`~/.claude/projects/.../*.jsonl`) become unreachable without a pointer
- Multi-session parts (parallel workers, planner→worker handoff, crash+resume) lose their handoff audit trail
- Retro-fill is possible but costly and embarrassing

The schema (`standard-phase-part.v4.2`) enforces these fields structurally. The close_protocol steps in the schema list them explicitly. Read the schema's `$hint` fields at close-time if uncertain.

See `examples/close-with-attribution.md` for a worked before/after example.

## When this methodology is overkill

- Scratch experiments where the product is "I learn what's possible" — use a notebook
- One-off bug fixes where the product is "the bug is fixed" — use a commit
- Research-only work where there's no product — use docs/

When you have a product to ship and an AI that needs to help build and verify it: that's when this earns its weight.
