# Workflow and Validation

> The complete workflow from session start to phase completion

---

## Workflow

```
1. Start session
   → Read PROJECT (understand state)
   → Read TODO (know current tasks)
   → Check FIXES (avoid past mistakes)

2. Work on task
   → Update TODO task status to in_progress
   → Code, test, verify

3. Complete task
   → Update TODO task status to done
   → If problem solved → add to FIXES
   → If learned something → add to RAG

4. Complete phase (all tasks done)
   → Move TODO content to DONE
   → Update PROJECT (done: + new phase:)
   → Create new TODO for next phase
```

## Validation

AI should verify:

```
TODO.phase == PROJECT.phase      # Must match
TODO.id == PROJECT.id            # Must match
TODO.id in PROJECT.planned       # Must exist
All done tasks → ready for DONE  # Phase complete check
```

RULE: If validation fails → STOP and ask user
