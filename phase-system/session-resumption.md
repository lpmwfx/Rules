---
tags: [phase-system, session-resumption, locks, audit-trail, claude-resume, v0.4]
concepts: [session-lock, audit-trail, stale-lock-recovery, multi-instance]
keywords: [locked_by_session, locked_session_log, jsonl, claude --resume, advisory_24h, recovery]
requires: [phase-system/methodology.md, phase-system/folder-conventions.md]
related: [phase-system/references-syntax.md]
layer: 2
---
# Session resumption — audit trails and `claude --resume` recovery (v0.4)

> Every Claude Code session has a JSONL log at `~/.claude/projects/<project-path-encoded>/<session-id>.jsonl`. Phase-system uses this for audit trail and for resuming interrupted sessions instead of starting from scratch.

---

## How a worker claims a part

When a Claude session starts working on a part, it writes three fields into the part's `concurrency` block:

```json
"concurrency": {
  "locked_by_session": "96b1778b-3ff3-4981-bcd9-e9cf353aa028",
  "locked_session_log": "~/.claude/projects/-home-dev-AIGame-authoring-system/96b1778b-3ff3-4981-bcd9-e9cf353aa028.jsonl",
  "locked_at": "2026-04-15T10:15:00Z"
}
```

RULE: Session ID equals the JSONL filename (minus `.jsonl`)
RULE: The session claiming a part MUST populate all three lock fields — `locked_by_session`, `locked_session_log`, `locked_at`
RULE: Clearing all three lock fields releases the lock (done by `close_protocol` at completion)
RULE: `lock_policy: 'advisory_24h'` — another session may reclaim a lock that's older than 24h with no status change

BANNED: Partial lock state — never set only some of the three fields

---

## Finding your own session ID

Your session log lives at `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` where `<encoded-cwd>` is your current working directory with `/` replaced by `-`. Working in `/home/dev/AIGame/authoring-system` gives `-home-dev-AIGame-authoring-system`.

```bash
ls -t ~/.claude/projects/$(pwd | sed 's:/:-:g')/*.jsonl | head -1 | xargs basename | sed 's/.jsonl$//'
```

---

## Audit trail

The JSONL contains the full message history of the session that worked on the part: tool calls, reasoning, file edits. Useful for:

- Understanding *why* a decision was made when only `result` is visible in the part
- Debugging when something the session changed is later questioned
- Onboarding to a half-done part: read the previous session's log before resuming

---

## Resumption

When a part's lock is older than expected and the worker session has died, resume with:

```bash
claude --resume <session-id>
```

VITAL: Work-in-progress is never lost as long as the JSONL exists — this is the core resilience pattern

The new instance restarts with the full conversation history including all tool results and file context. It picks up exactly where the old one stopped — answering the pending question, continuing the next plan-step, completing the half-done usage-test.

---

## Stale-lock recovery procedure

RULE: When encountering a stale lock, first try `claude --resume <locked_by_session>` — if the previous session was just paused (laptop slept, network hiccup), this picks up cleanly
RULE: If resume isn't desired or fails, the new session overwrites `locked_by_session` and `locked_session_log` with its own values
RULE: The previous session's JSONL stays — it's still audit trail and can be referenced from `history` entries on the part

---

## Workflow summary

```
Worker A claims pwa/p1.5-oauth-fix.json:
  → writes locked_by_session, locked_session_log, locked_at
  → executes plan-steps, runs usage-tests
  → on completion: clears all three lock fields, writes result.summary, sets status: done
  → JSONL log persists at ~/.claude/projects/.../<session-id>.jsonl

Worker A's laptop dies mid-step:
  → lock remains in part-file
  → next day: Worker B opens part, sees stale lock
  → Worker B runs: claude --resume 96b1778b-3ff...
  → Claude restarts with full context, finishes the work
  → Worker B's session takes over the lock seamlessly
```

---

## Multi-instance work

Each Claude session has its own JSONL. A single user running multiple Claude Code instances on different parts of the same phase produces a separate audit trail per part:

- Three Claudes working in parallel on `pwa/`, `server/`, `research/` parts of phase 2
- Each with its own log
- All visible in the orchestrator's `parts.items[]` via their `locked_session_log` fields
- Phase-status aggregates from individual part statuses

VITAL: The session log is the unit of recoverable work; the part-file is the unit of coordination


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
