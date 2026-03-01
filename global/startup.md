---
tags: [startup, checklist, session, mandatory]
concepts: [workflow, initialization]
feeds: [project-files/workflow.md]
related: [global/read-before-write.md, global/know-before-change.md]
layer: 1
---
# Mandatory Startup Checklist

> Do this BEFORE answering the user — every session

---

```
STOP. Before doing ANYTHING, run this checklist:

0. VERIFY index.yaml         → python tools/index_generator.py --verify (if exists)
1. READ proj/PROJECT.md      → Understand state, phase, stack, infra
2. READ proj/PHASES.md       → Know the active milestone and delivers
3. READ proj/TODO.md         → Current tasks (WHAT to do)
4. READ proj/FIXES.md        → Known problems (DON'T repeat mistakes)
5. SCAN relevant code        → Understand current state
6. THEN form solution        → Simple, minimal, targeted

If you skip this: You WILL make mistakes that are already documented.
If you follow this: You will produce excellent results.
```

RULE: All project files live in `proj/` — never in the project root
RULE: Validate that proj/TODO.md phase matches proj/PROJECT.md Current.phase
RULE: If proj/ does not exist, create it and initialize the project files

These rules apply to ALL code — Python, JavaScript, CSS, and any other language.
They are non-negotiable habits that make AI collaboration reliable.
