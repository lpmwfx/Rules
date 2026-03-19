---
tags: [workflow, dev-cycle, session, project-management, process]
concepts: [development-cycle, project-tracking, session-discipline]
keywords: [dev-cycle, understand, plan, implement, test, document, commit, phases, todo, project]
layer: 2
requires: [global/startup.md, workflow/always-compliant.md]
feeds: [workflow/load-context.md, workflow/coding-discipline.md, workflow/commit-clean.md]
related: [project-files/project-file.md, project-files/todo-file.md]
---

# Development Cycle — Full Session Workflow

## The Problem

AI agents lose context between sessions. Without a systematic cycle:
- Decisions evaporate — same discussions repeat
- Plans drift — no tracking of what phase we're in
- Testing is skipped — code ships untested
- Lessons are lost — same mistakes repeat

## The Solution

**One cycle. Every task. No exceptions.**

```
UNDERSTAND → PLAN → IMPLEMENT → TEST → DOCUMENT → COMMIT
```

**Principle:** Build without rules violations first time. All else is waste.

---

## The 6 Steps

### Step 0: UNDERSTAND

Read project state BEFORE forming any opinion.

```
1. Read global/startup.md            → session checklist
2. Read proj/PROJECT                 → identity, architecture, decisions, what works
3. Read proj/RULES                   → active rules for this project
4. Read proj/FIXES                   → known problems (don't repeat)
5. Read proj/TODO                    → current tasks and phase
6. Read proj/PHASES                  → phase tracking
```

RULE: Do NOT skip any file. Every file exists for a reason.
RULE: If a decision is documented in PROJECT, follow it — don't re-discuss.
RULE: If a problem is documented in FIXES, avoid it — don't re-discover.

**Output:** You understand current state, active constraints, known traps.

---

### Step 1: PLAN

Form approach BEFORE writing code.

```
1. Identify which TODO items to tackle
2. Check which rules apply (get_rule / get_context from MCP)
3. Verify approach doesn't conflict with PROJECT decisions
4. Confirm with user if approach is non-trivial
```

RULE: Plans reference specific rules — not vague "best practices"
RULE: If you need a rule you haven't read → read it now, before coding
RULE: Agreement with user on approach goes into proj/PROJECT

**Output:** Clear plan, rules loaded, user aligned.

---

### Step 2: IMPLEMENT

Write code that complies from the start.

```
1. Follow workflow/always-compliant.md → BEFORE/DURING/VERIFY
2. Follow workflow/load-context.md → know rules before editing
3. Follow workflow/coding-discipline.md → write correct code
4. Hooks catch violations immediately — fix them NOW, not later
```

RULE: Zero rework loops is the target
RULE: If hooks report a violation → stop, fix, then continue
RULE: Never add unplanned features (scope creep = delays)

VITAL: Read existing code before modifying it. Guess nothing.

**Output:** Code written, hooks passed, no known violations.

---

### Step 3: TEST

Run what you built. Prove it works.

```
1. Run the actual command / feature / change
2. Verify output matches expected behavior
3. If tests exist → run them
4. If no tests → describe what you tested and how
```

RULE: "It compiles" is not testing
RULE: Test the CHANGE, not just the build
RULE: Document test results — what worked, what didn't

BANNED: Skipping test step. Every change gets tested.

**Output:** Verified working. Test evidence documented.

---

### Step 4: DOCUMENT

Update project files with what happened.

```
1. proj/TODO        → mark completed items, add new if discovered
2. proj/PHASES      → update phase status
3. proj/PROJECT     → note what works now and HOW
4. proj/FIXES       → if you hit a problem, document it for next session
```

RULE: Documentation happens BEFORE commit, not after
RULE: Write for your future self — next session has zero context
RULE: Include the HOW, not just the WHAT

VITAL: This step prevents amnesia. Skip it → next session repeats your work.

**Output:** All proj/ files reflect current reality.

---

### Step 5: COMMIT

Clean commit with zero violations.

```
1. Follow workflow/commit-clean.md → check_staged, no bypass
2. Commit message describes the change clearly
3. If pre-commit blocks → fix violations, re-stage, commit again
4. Never use --no-verify
```

RULE: Only commit when all steps above are done
RULE: One logical change per commit
RULE: Commit message references the phase/task if applicable

BANNED: Committing untested code
BANNED: Committing with known violations
BANNED: Using --no-verify to bypass hooks

**Output:** Clean commit. Zero violations. Documented change.

---

## The Full Picture

```
Session start
  │
  ├─ UNDERSTAND: Read proj/ files (5 min)
  │
  ├─ PLAN: Form approach, load rules (5 min)
  │
  ├─ IMPLEMENT: Write code within rules (variable)
  │    └─ Hooks catch violations immediately
  │
  ├─ TEST: Run it, prove it works (5 min)
  │
  ├─ DOCUMENT: Update proj/ files (5 min)
  │    ├─ TODO: mark done, add new
  │    ├─ PHASES: update status
  │    ├─ PROJECT: note what works + how
  │    └─ FIXES: document any new problems
  │
  └─ COMMIT: Zero violations (1 min)
```

**Total overhead:** ~20 min per task for documentation.
**ROI:** Zero amnesia, zero repeated work, zero rework loops.

---

## Anti-Patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Skip UNDERSTAND | You repeat solved problems | Read proj/ first |
| Skip PLAN | Violations discovered late | Load rules before coding |
| Skip TEST | Broken code ships | Run it before committing |
| Skip DOCUMENT | Next session has amnesia | Update proj/ before commit |
| "I'll document later" | You won't | Document NOW |
| Guess code patterns | Violations guaranteed | Read existing code first |
| Add unplanned features | Scope creep, delays | Stick to TODO |

---

## Glossary

- **Dev cycle:** UNDERSTAND → PLAN → IMPLEMENT → TEST → DOCUMENT → COMMIT
- **Amnesia:** Loss of context between sessions (prevented by proj/ documentation)
- **Rework loop:** Write → scan → fix → re-stage (should be 0 iterations)
- **Proactive compliance:** Know rules BEFORE writing code
- **proj/ files:** Source of truth for project state, decisions, lessons
