# Tool Configurations

> Implementation examples for specific AI tools

---

## Claude Code

```json
// ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "/path/to/startup-context.sh"
      }]
    }]
  }
}
```

## Cursor

```
// .cursorrules (in project root)
Read TODO for current tasks.
Read FIXES before coding.
Read doc/project.md for architecture.
Follow rules in ~/.rules/
```

## Aider

```bash
# .aider.conf.yml
read:
  - TODO
  - FIXES
  - doc/project.md
```

## Continue.dev

```json
// config.json
{
  "contextProviders": [{
    "name": "file",
    "params": { "files": ["TODO", "FIXES", "doc/project.md"] }
  }]
}
```

## OpenAI API / Anthropic API

```python
# Prepend to system prompt
context = ""
if os.path.exists("TODO"):
    context += f"TODO:\n{open('TODO').read()[:2000]}\n"
if os.path.exists("FIXES"):
    context += f"FIXES:\n{open('FIXES').read()[:2000]}\n"

system_prompt = context + base_system_prompt
```
