# Startup Script

> Run a script when session starts — output becomes AI context

---

## Bash Startup Script

```bash
#!/bin/bash
# startup-context.sh - Run at session start

echo "=== PROJECT CONTEXT ==="

# Current tasks
if [[ -f "TODO" ]]; then
    echo "TODO (current tasks):"
    head -30 TODO | sed 's/^/  /'
fi

# Known mistakes to avoid
if [[ -f "FIXES" ]]; then
    echo "FIXES (avoid these mistakes):"
    head -20 FIXES | sed 's/^/  /'
fi

# Architecture reminder
if [[ -f "doc/project.md" ]]; then
    echo "READ doc/project.md for architecture"
fi

# Detect languages and show relevant rules
if [[ -f "pyproject.toml" ]] || find . -maxdepth 3 -name "*.py" -type f | head -1 | grep -q .; then
    echo "PYTHON detected - see ~/.rules/Python/RULES"
fi

if [[ -f "package.json" ]] || find . -maxdepth 3 -name "*.js" -type f | head -1 | grep -q .; then
    echo "JAVASCRIPT detected - see ~/.rules/JS/RULES"
fi

if find . -maxdepth 4 -name "*.css" -type f | head -1 | grep -q .; then
    echo "CSS detected - see ~/.rules/CSS/RULES"
fi

echo "=== WORKFLOW: doc/project.md → FIXES → TODO → code → test ==="
```
