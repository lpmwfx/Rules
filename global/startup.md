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

0. VERIFY index.yaml      → python tools/index_generator.py --verify (if exists)
1. READ doc/project.md    → Understand architecture (WHY things exist)
2. READ TODO              → Current task (WHAT to do)
3. READ FIXES             → Known problems (DON'T repeat mistakes)
4. SCAN relevant code     → Understand current state
5. THEN form solution     → Simple, minimal, targeted

If you skip this: You WILL make mistakes that are already documented.
If you follow this: You will produce excellent results.
```

These rules apply to ALL code — Python, JavaScript, CSS, and any other language.
They are non-negotiable habits that make AI collaboration reliable.
