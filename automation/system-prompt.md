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

Read proj/PROJECT before making any architectural decisions — it is the only source of truth.
```

## IDE Extensions

Configure IDE to inject context:
- VS Code: tasks.json + launch configuration
- Cursor: .cursorrules file
- JetBrains: Run configurations

## Project Files for Context

| File | Purpose | AI Action |
|------|---------|-----------|
| PROJECT | Architecture, state, rules — single source of truth | READ first, every session |
| TODO | Current tasks | READ before work |
| FIXES | Solved problems | READ before coding, WRITE after fixing |
| RAG | Project knowledge | READ for context, WRITE discoveries |
| DONE | Completed work | Reference for what exists |
| ISSUES | Known problems | Log here, check here |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
