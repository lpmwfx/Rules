---
tags: [phase-system, methodology, lifecycle, workflow, research-first, signoff]
concepts: [one-product-per-phase, research-before-plan, usage-tests, ai-signoff, split-mode]
keywords: [phase, product, research, decisions, plan, usage-tests, verification, signoff, planner, worker]
requires: [phase-system/README.md]
feeds: [phase-system/folder-conventions.md, phase-system/references-syntax.md]
related: [phase-system/integration.md, project-files/phases-file.md]
layer: 2
---
# Methodology — what a phase is and how it flows

> A phase is a unit of work bounded by **one product**. Not a deliverable list — a single coherent thing a user (or AI as a user) can demonstrably use at the end.

If you can't point at it and say "this works, here's how to use it", you don't have a product — you have a partial component.

The full roadmap is `proj/PHASES` (human-facing index); the executable definition lives per phase in `proj/PHASE/<n>-<label>/p<n>.json`.

---

## Core rules

VITAL: One product per phase — if you have multiple products, you have multiple phases
VITAL: `product.user_can[]` is concrete and AI-demonstrable — if AI can't do it, the product isn't done
VITAL: Research happens before any plan step is written — no plans on guesses
VITAL: Every plan step has a testable `pass` — outcome, not implementation
VITAL: Usage-tests are scenarios AI must be able to perform with the running product — added throughout the phase
VITAL: Phase cannot close without AI signoff — `ai_verified=true` after a concrete "I did X, Y, Z and it works"
VITAL: User approval still required after AI signoff — signoff is not approval of own work

RULE: Decisions carry candidates (≥2), answer, rationale, and `lands_in` (where the answer is persisted)
RULE: Open decisions block plan — resolve via research or defer to a future phase in `issues_logged`
RULE: Issues discovered mid-phase that are out of scope go to `issues_logged` with `severity` and `moves_to`
RULE: New invariants or anti-patterns discovered go into `anti_creep_check.new_*_discovered` for snapshot at close
RULE: Pass criterion is the *outcome*, not the implementation — "tool returns SID for new scene" not "function at file.ts:42"

BANNED: Declaring a phase done because tests pass but the product has never been used
BANNED: Writing plan steps referencing behavior that was never researched
BANNED: Phases that produce "a bunch of components" rather than one coherent product
BANNED: Mid-phase scope creep — new ideas go to `issues_logged`, not into the current plan

---

## Lifecycle

```
planned → researching → ready → active → done
                                       ↘ aborted
```

- **planned**: identity + context + milestone + product written; nothing else
- **researching**: topics under investigation, decisions being resolved
- **ready**: research closed, decisions resolved, plan written, usage_tests defined, user has authorized start
- **active**: dev in progress; plan steps and usage_tests executing
- **done**: all verification.checks + usage_tests green, AI signed off, user approved
- **aborted**: phase abandoned; reasoning logged in `history`

---

## The seven workflow steps

### 1. Open with intent

Fill `identity` (number, id, title), `context` (problem, outcome), and `milestone` (the one definition-of-done criterion). This takes minutes. If you can't write it, you don't have a phase yet — you have an idea.

### 2. Define the product

Write `product`. Most-skipped section, catches the most scope creep. Force yourself to write `product.user_can[]` — concrete list of what AI can do with the finished thing. Fuzzy list = fuzzy phase.

### 3. Research before plan

Every unknown investigated **before** any plan step. Parallel sub-agents for distinct topics. Each `research.topics[]` entry: summary (in clear prose, not quotes), sources (URLs), open_questions. Open questions block plan; resolve via decisions or further research.

No plan built on guesses. If you can't get clarity, log it as an open question and resolve via a decision ("we'll use Mistral Small for now and accept the risk") or carve out research as a phase of its own.

### 4. Resolve decisions

OPS-level questions: which library, which domain, which auth provider, which storage. Each decision needs candidates (≥2), answer, rationale (why this not the others), and `lands_in` (where persisted). Open decisions block plan. Deferred decisions go to `issues_logged` with the phase name.

### 5. Write the plan

Step-by-step. Each `plan.steps[]`:

- `task`: what to do (for complex steps use `## Problem / ## Approach / ## Changes / ## Verification` markdown)
- `task_type`: `local_bash | local_agent | remote_agent | data | config | git`
- `files`: what this touches
- `code_changes`: prose summary; "none" is valid
- `depends_on`: other step ids
- `subagent_prompt`: self-contained briefing if delegated
- `pass`: concrete testable criterion
- `status`: `pending → in_progress → completed | failed | stopped`

### 6. Define usage tests

`usage_tests[]` are scenarios AI must be able to perform with the running product. Different from `verification`:

- **verification**: does the system reach the right end-state? (`curl /health → 200`)
- **usage_tests**: can AI use the system for its purpose? (AI calls `whoami` via Claude.ai connector and gets `ai@lpmwfx.com`)

Add tests up front for the product, then more as functionality lands. AI runs them and reports `actual` + `status`. Failing usage tests block phase-done.

### 7. Execute, verify, sign off

While `status: active`:
- Step statuses progress
- AI runs usage tests as features land
- Issues go to `issues_logged` with severity
- New invariants / anti-patterns go to `anti_creep_check.new_*_discovered`

Before phase-done:
- All `verification.checks` green (or explicitly moved)
- All `usage_tests` green (or product is incomplete)
- AI writes concrete `ai_signoff.ai_statement`: "I did X, Y, Z and it works" — not "looks good"
- Sets `ai_verified: true`
- User reviews and sets `user_approved: true`
- Snapshot of `proj/data/architecture.json` saved into `data_layer_changes.architecture_snapshot_path`
- Status → `done`

---

## Principles in tension

**Research vs. momentum.** The discipline is research-first; the temptation is to code. Spawn parallel research sub-agents while writing the easy sections (identity, context, milestone, product). Research fills in by the time you need it.

**Concreteness vs. flexibility.** Over-specified pass kills agility. Rule of thumb: pass is the *outcome* not the *implementation*.

**Phase boundaries vs. continuous work.** Strong boundaries (one product per phase, signoff required) exist to keep phases small. If a phase grows past one product, split it. If it needs research mid-execution, pause status to `researching` and resume when resolved.

**AI signoff vs. human autonomy.** Signoff is AI saying "I have run the tests and the product works for me as a user". NOT AI approving its own work — user still approves. Point: force AI to actually *use* the product before declaring success, instead of claiming success because tests passed.

---

## Anti-patterns this prevents

- **Phantom done**: tests pass, declared done, product doesn't actually work for its intended use. Caught by usage_tests + ai_signoff.
- **Drift between sessions**: each new session re-discovers what's been decided. Caught by persisted decisions with `lands_in`.
- **Plans built on guesses**: research never happened. Caught by research-before-plan ordering.
- **Scope creep mid-phase**: feature ideas grow during execution. Caught by single-product rule + `issues_logged`.
- **Untracked discoveries**: AI finds an issue or invariant, doesn't capture it. Caught by `issues_logged` + `new_*_discovered`.

---

## Parallelism via folder placement (v0.3+)

A phase can be a single file or a directory tree of part-files organized by write-domain. This enables the **planner/worker split**:

| Role | Session-type | What they do |
|---|---|---|
| **Planner** | One Claude in plan-mode | Creates `p<n>.json` + sub-orchestrators + part-files. Fills research, decisions, plan, usage_tests, references. Sets `status: ready`. Adds no locks. |
| **Worker** | Any Claude Code CLI session | Opens `proj/PHASE/<n>-<label>/`, finds unclaimed part (`locked_by_session: null`), takes lock, reads `references[]` as onboarding stack, executes, runs usage-tests, releases lock. |
| **Parallel worker** | Another Claude session simultaneously | Picks a part in a *different folder* — assumed safe by construction. |
| **Orchestrator-keeper** | Any session touching a part | Updates orchestrator's `parts.items[].status` to mirror the part's status. |

RULE: Planner produces a shelf-ready phase artifact; execution happens in later sessions
RULE: Use split-mode when multiple sessions will work concurrently, or when one session spawns parallel sub-agents on independent slices
RULE: When in doubt, start single-mode; split when parallelism actually appears as a need

BANNED: Planner session executing plan-steps — that collapses the planner/worker split (exception: trivial phases)
BANNED: Parts constantly modifying each other's state across folders — that means they're not independent; re-decompose

### Aggregated signoff (split-mode)

- All `parts.items[].status === 'completed'`
- All part-files' verification + usage_tests green
- `ai_statement` references each part's `result.summary`

See [folder-conventions.md](folder-conventions.md) for write-domain rules and [references-syntax.md](references-syntax.md) for the read-graph.

---

## When this methodology is overkill

- Scratch experiments where the product is "I learn what's possible" — use a notebook
- One-off bug fixes where the product is "the bug is fixed" — use a commit
- Research-only work with no product — use `docs/`

When you have a product to ship and an AI that needs to help build and verify it: that's when this earns its weight.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
