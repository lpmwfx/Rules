---
tags: [phase-system, session-resumption, locks, audit-trail, claude-resume, v0.4]
concepts: [session-lock, audit-trail, stale-lock-recovery, multi-instance]
keywords: [locked_by_session, locked_session_log, jsonl, claude --resume, advisory_24h, recovery]
requires: [phase-system/methodology.md, phase-system/folder-conventions.md]
related: [phase-system/references-syntax.md]
layer: 2
---

# Session resumption (v0.4)

Every Claude Code session has a JSONL log at `~/.claude/projects/<project-path-encoded>/<session-id>.jsonl`. The phase-system uses this for two things: an audit-trail of what was thought and done, and the ability to **resume an interrupted session** instead of starting from scratch.

## How a worker claims a part

When a Claude session starts working on a part, it writes three fields into the part's `concurrency` block:

```json
"concurrency": {
  "locked_by_session": "96b1778b-3ff3-4981-bcd9-e9cf353aa028",
  "locked_session_log": "~/.claude/projects/-home-dev-AIGame-authoring-system/96b1778b-3ff3-4981-bcd9-e9cf353aa028.jsonl",
  "locked_at": "2026-04-15T10:15:00Z"
}
```

The session ID is derivable from the JSONL filename — they're the same. The session must populate all three fields on claim; clearing them on completion releases the lock.

## Finding your own session ID

Inside Claude Code, your session log lives at `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` where `<encoded-cwd>` is your current working directory with `/` replaced by `-`. For example, working in `/home/dev/AIGame/authoring-system` gives `-home-dev-AIGame-authoring-system`.

A simple bash one-liner to find your current session ID:

```bash
ls -t ~/.claude/projects/$(pwd | sed 's:/:-:g')/*.jsonl | head -1 | xargs basename | sed 's/.jsonl$//'
```

## Audit trail

Anyone (human or another Claude) can open the JSONL and see the full message history of the session that worked on the part: tool calls, reasoning, file edits. Useful for:

- Understanding *why* a decision was made when only the result is visible in the part's `result` field
- Debugging when something the session changed is later questioned
- Onboarding to a half-done part: read the previous session's log before resuming

## Resumption

When a part's lock is older than expected and the worker session has died (no recent activity on its JSONL), a new session can resume the dead one with:

```bash
claude --resume <session-id>
```

This restarts Claude Code with the full conversation history of the dead session, including all tool results and file context. The new instance can pick up exactly where the old one stopped — answer the question that was pending, continue the next plan-step, complete the usage-test that was halfway done.

This is the core resilience pattern of the phase-system: **work-in-progress is never lost** as long as the JSONL exists.

## Stale-lock recovery

`lock_policy: 'advisory_24h'` means another session may take a stale lock. Recommended procedure when encountering a stale lock:

1. **First, try to resume.** `claude --resume <locked_by_session>` — if the previous session was just paused (laptop slept, network hiccup), this picks up cleanly.
2. **If resume isn't desired or fails**, the new session sets its own `locked_by_session` and `locked_session_log` over the stale ones. The previous session's JSONL stays — it's still useful audit-trail and can be referenced from `history` entries on the part.

## Workflow summary

```
Worker A claims pwa/p1.5-oauth-fix.json:
  → writes locked_by_session, locked_session_log, locked_at
  → executes plan-steps, runs usage-tests
  → on completion: clears lock, writes result.summary, sets status: done
  → JSONL log persists at ~/.claude/projects/.../<session-id>.jsonl

Worker A's laptop dies mid-step:
  → lock remains in part-file
  → next day: Worker B opens part, sees stale lock
  → Worker B runs: claude --resume 96b1778b-3ff...
  → Claude restarts with full context, finishes the work
  → Worker B's session takes over the lock seamlessly
```

## Multi-instance work

Because each Claude session has its own JSONL, a single user running multiple Claude Code instances on different parts of the same phase produces a separate audit trail per part. Useful for:

- Three Claudes working in parallel on `pwa/`, `server/`, `research/` parts of phase 2
- Each with its own log
- All visible in the orchestrator's `parts.items[]` via their respective `locked_session_log` fields
- Phase-status aggregates from individual part statuses

The session log is the unit of recoverable work. The part-file is the unit of coordination.
