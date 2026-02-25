---
tags: [automation, session, overview]
concepts: [automation, session-management]
related: [automation/startup-script.md, automation/system-prompt.md, automation/language-detection.md, automation/tool-configs.md, automation/maintenance.md]
layer: 6
---
# AI Session Automation

> Making AI coding assistants context-aware from session start

---

Works with any AI tool (Claude, Cursor, Copilot, Codex, Mistral, etc.)

## The Problem

AI starts every session blind:
- No knowledge of current project
- No memory of past mistakes
- No awareness of coding standards
- Guesses instead of knowing

Result: Repeated mistakes, scope creep, inconsistent code.

## The Solution

Inject project context BEFORE AI responds to first message.

## Files

| File | Topic |
|------|-------|
| [startup-script.md](startup-script.md) | Bash startup context injection |
| [system-prompt.md](system-prompt.md) | API system prompt injection |
| [language-detection.md](language-detection.md) | Language detection patterns |
| [tool-configs.md](tool-configs.md) | Claude/Cursor/Aider/Continue configs |
| [maintenance.md](maintenance.md) | Keeping files updated |
