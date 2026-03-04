---
tags: [startup, checklist, session, mandatory]
concepts: [workflow, initialization]
feeds: [project-files/workflow.md]
related: [global/graph-position-paradigm.md, global/read-before-write.md, global/know-before-change.md, global/file-limits.md]
layer: 1
---
# Mandatory Startup Checklist

> Do this BEFORE answering the user — every session

---

```
STOP. Before doing ANYTHING, run this checklist:

0. VERIFY index.yaml         → python tools/index_generator.py --verify (if exists)
1. READ proj/PROJECT      → Only source of truth: state, phase, stack, infra
2. READ proj/RULES        → Active MCP rules + project-specific conventions
3. READ proj/UIUX         → UI/UX source of truth (GUI projects — ALL UI work requires this)
4. READ proj/FIXES        → Known problems (DON'T repeat mistakes)
5. READ proj/TODO         → Current tasks (WHAT to do)
6. SCAN for oversized files  → find src/ -name "*.py" -o -name "*.ts" -o -name "*.css" | xargs wc -l | sort -rn | head -20
7. SCAN relevant code        → Understand current state
8. THEN form solution        → Simple, minimal, targeted

If you skip this: You WILL make mistakes that are already documented.
If you follow this: You will produce excellent results.
```

VITAL: Step 5 is mandatory for any session involving UI, CSS, or source files — oversized files must be split before new code is added

RULE: All project files live in `proj/` — never in the project root
RULE: Validate that proj/TODO phase matches proj/PROJECT Current.phase
RULE: If proj/ does not exist, create it and initialize the project files

These rules apply to ALL code — Python, JavaScript, CSS, and any other language.
They are non-negotiable habits that make AI collaboration reliable.
