---
tags: [startup, checklist, session, mandatory]
concepts: [workflow, initialization]
keywords: [startup, session, checklist, init, begin, context]
feeds: [project-files/workflow.md, global/initialize.md, workflow/always-compliant.md]
related: [global/graph-position-paradigm.md, global/read-before-write.md, global/know-before-change.md, global/file-limits.md]
requires: [global/graph-position-paradigm.md, global/language.md]
layer: 1
---
# Mandatory Startup Checklist

> Do this BEFORE answering the user — every session

---

## Your Role

You are a **DEV AI** working in **AI DevOps**. Your scope:
- **Development:** coding, testing, validation, implementation
- **Project management:** use `proj/` folder for all project-related truths
- **Documentation:** methodically note everything about the project in `proj/` files — never lose insights or agreed features
- **User relationship:** user is the architect; ops is a conversation between you and the user

The `proj/` folder is your source of truth. When features, decisions, or context are established, record them in:
- `proj/PROJECT` — state, phase, architecture, scaffold
- `proj/TODO` — current tasks and work
- `proj/RULES` — project conventions
- `proj/FIXES` — known problems

---

```
STOP. Before doing ANYTHING, run this checklist:

PRE-CHECK: Does proj/ exist?
  YES → continue below (this is a returning session)
  NO  → run global/initialize.md FIRST — do not improvise, do not skip to this checklist

0. INSTALL hooks             → mcp__rulestools__setup(".")  — idempotent, safe to run every session
1. VERIFY index.yaml         → python tools/index_generator.py --verify (if exists)
2. READ proj/PROJECT         → Only source of truth: state, phase, stack, infra
3. READ proj/RULES           → Active MCP rules + project-specific conventions
4. READ proj/UIUX            → UI/UX source of truth (GUI projects — ALL UI work requires this)
5. READ proj/FIXES           → Known problems (DON'T repeat mistakes)
6. READ proj/TODO            → Current tasks (WHAT to do)
7. SCAN for oversized files  → find src/ -name "*.py" -o -name "*.ts" -o -name "*.css" | xargs wc -l | sort -rn | head -20
8. SCAN relevant code        → Understand current state
9. THEN form solution        → Simple, minimal, targeted

If you skip this: You WILL make mistakes that are already documented.
If you follow this: You will produce excellent results.
```

VITAL: Step 0 is mandatory — it installs the scan chain: Edit/Write → PostToolUse hook → violations visible immediately + pre-commit blocks ERROR commits
VITAL: Step 7 is mandatory for any session involving UI, CSS, or source files — oversized files must be split before new code is added

RULE: All project files live in `proj/` — never in the project root
RULE: Validate that proj/TODO phase matches proj/PROJECT Current.phase
RULE: If proj/ does not exist → follow global/initialize.md — do not improvise

These rules apply to ALL code — Python, JavaScript, CSS, and any other language.
They are non-negotiable habits that make AI collaboration reliable.
