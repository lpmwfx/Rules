---
tags: [workflow, transitions, state-machine, process, fifo, living-queue, session]
concepts: [workflow, state-transitions, living-queues]
requires: [project-files/project-file.md, project-files/phases-file.md, project-files/todo-file.md, project-files/issues-file.md]
related: [project-files/goal-chain.md, project-files/fixes-file.md, project-files/done-file.md, project-files/workflow.md]
keywords: [fifo, queue, trigger, dones, transition, session, in_progress, resolved, committed]
layer: 2
---
# Project Process — State Machine

> TODO and ISSUES are living queues — items flow in constantly, completed items flow out

---

VITAL: TODO and ISSUES are living queues — not static phase documents
VITAL: Items only move DOWN across DONES — never back up
RULE: One task `in_progress` at a time per AI session

## Triggers

### Task flow (TODO)

| When | Do |
|------|----|
| Starting a task | Set `status: in_progress` |
| Task verified done | Move below `# --- DONES ---` in TODO |
| New task discovered mid-work | Add to ISSUES — not directly to TODO |
| All TODO tasks done | Archive to DONE → update PHASES + PROJECT → create new TODO |

### Issue flow (ISSUES → FIXES)

| When | Do |
|------|----|
| Problem discovered | Add to ISSUES `status: open` — do NOT fix immediately |
| Issue assigned to phase/task | Set `status: committed` |
| Issue fixed and verified | Set `status: resolved` → move below DONES → add FIXES entry |

### Phase flow (PHASES)

| When | Do |
|------|----|
| Phase starts | Set PHASES entry `status: active` — only ONE active at a time |
| Phase completes | Move PHASES entry below DONES → archive TODO to DONE → update PROJECT |

## Status Transitions

```
TODO task:  pending → in_progress → done
ISSUES:     open → committed → resolved
PHASES:     planned → active → done
DONE:       append-only — never edited
FIXES:      append-only — newest first
```

After `done`, two exceptional paths (each requires an ISSUE entry first):
```
done → FAIL      requires: what failed + what was learned
done → REFACTOR  requires: what to improve + what to reuse
```

Forbidden:
```
in_progress → FAIL       must reach done first
pending     → REFACTOR   must reach done first
in_progress → ISSUES     finish the task first
```

## DONES Mechanics

Three files use `# --- DONES ---`:

| File | Above DONES | Below DONES |
|------|-------------|-------------|
| TODO | pending, in_progress | done |
| ISSUES | open, committed | resolved |
| PHASES | planned, active, blocked | done |

RULE: Items move DOWN across DONES — never back up
RULE: Moving below DONES means evaluated and closed — no re-opening

## Session Workflow

```
1. Start session
   → Read proj/PROJECT   (understand state, phase, infra)
   → Read proj/PHASES    (know the active milestone)
   → Read proj/TODO      (know current tasks)
   → Read proj/FIXES     (avoid past mistakes)
   → Validate alignment (see below) — if mismatch: STOP, ask user

2. Work on task
   → Set TODO task status: in_progress
   → Code, test, verify

3. Complete task
   → Move TODO task below DONES
   → If problem solved → add to proj/FIXES
   → If learned something → add to proj/RAG

4. Complete phase (all tasks done)
   → Append completed phase to proj/DONE
   → Move PHASES entry below DONES
   → Update proj/PROJECT (Current phase + History)
   → Create new proj/TODO for next phase
```

## Session-Start Validation

RULE: `TODO.phase` must match `PROJECT.Current.phase`
RULE: `TODO.id` must match `PROJECT.Current.id`
RULE: Active phase in PHASES must match PROJECT phase
RULE: If any check fails → STOP and ask user before proceeding


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
