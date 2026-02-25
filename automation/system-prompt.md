---
tags: [automation, system-prompt, ai-instructions]
concepts: [ai-configuration, prompt-engineering]
related: [automation/startup-script.md]
layer: 5
---
# System Prompt Injection

> Prepend context to system prompt for API-based tools

---

## Template

```
You are working on project X.

Current tasks (from TODO):
- Task 1
- Task 2

Known issues to avoid (from FIXES):
- Problem A was caused by X, fixed by Y

Language rules:
- Python: ~/.rules/Python/RULES
- JavaScript: ~/.rules/JS/RULES

Read doc/project.md before making architectural decisions.
```

## IDE Extensions

Configure IDE to inject context:
- VS Code: tasks.json + launch configuration
- Cursor: .cursorrules file
- JetBrains: Run configurations

## Project Files for Context

| File | Purpose | AI Action |
|------|---------|-----------|
| TODO | Current tasks | READ before work |
| FIXES | Solved problems | READ before coding, WRITE after fixing |
| RAG | Project knowledge | READ for context, WRITE discoveries |
| doc/project.md | Architecture | READ for big picture |
| DONE | Completed work | Reference for what exists |
| ISSUES | Known problems | Log here, check here |
