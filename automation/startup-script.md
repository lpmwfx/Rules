---
tags: [automation, startup-script, bash, context-injection]
concepts: [automation, context-injection]
requires: [global/startup.md]
feeds: [automation/language-detection.md]
related: [automation/system-prompt.md]
keywords: [bash, startup-hook, project-context]
layer: 5
---
# Startup Script

> Run a script when session starts — output becomes AI context

---

## Bash Startup Script

```bash
#!/bin/bash
# startup-context.sh - Run at session start

echo "=== PROJECT CONTEXT ==="

# Bootstrap: if proj/PROJECT missing, consolidate source document into it
if [[ ! -f "proj/PROJECT" ]]; then
    mkdir -p proj
    SOURCE=""
    for candidate in doc/project.md doc/PROJECT.md README.md brief.md; do
        if [[ -f "$candidate" ]]; then SOURCE="$candidate"; break; fi
    done
    if [[ -n "$SOURCE" ]]; then
        echo "ACTION REQUIRED: proj/PROJECT does not exist."
        echo "  Source found: $SOURCE"
        echo "  Read $SOURCE and write everything into proj/PROJECT (standard format)."
        echo "  After init, $SOURCE is frozen — proj/PROJECT is the only source of truth."
    else
        echo "ACTION REQUIRED: proj/PROJECT does not exist and no source document found."
        echo "  Ask the user for project goal, stack, and structure, then create proj/PROJECT."
    fi
    echo ""
fi

# Architecture — proj/PROJECT is the only source of truth
if [[ -f "proj/PROJECT" ]]; then
    echo "PROJECT (architecture + state):"
    head -40 proj/PROJECT | sed 's/^/  /'
fi

# Active rules + project conventions — load MCP rules listed here
if [[ -f "proj/RULES" ]]; then
    echo "RULES (active MCP rules + project conventions):"
    cat proj/RULES | sed 's/^/  /'
fi

# UI/UX source of truth — mandatory for all GUI projects
if [[ -f "proj/UIUX" ]]; then
    echo "UIUX (platform, architecture, flows, conventions):"
    cat proj/UIUX | sed 's/^/  /'
elif find src/ -name "*.slint" -o -name "*.ui" -o -name "*.tsx" -o -name "*.qml" \
     -o -name "*.swift" 2>/dev/null | head -1 | grep -q .; then
    echo "WARNING: GUI files detected but proj/UIUX does not exist."
    echo "  Create proj/UIUX before doing any UI work — see project-files/uiux-file.md"
fi

# Current tasks
if [[ -f "proj/TODO" ]]; then
    echo "TODO (current tasks):"
    head -30 proj/TODO | sed 's/^/  /'
fi

# Known mistakes to avoid
if [[ -f "proj/FIXES" ]]; then
    echo "FIXES (avoid these mistakes):"
    head -20 proj/FIXES | sed 's/^/  /'
fi

# Detect languages and show relevant rules
if [[ -f "pyproject.toml" ]] || find . -maxdepth 3 -name "*.py" -type f | head -1 | grep -q .; then
    echo "PYTHON detected - load: python/README.md"
fi

if [[ -f "package.json" ]] || find . -maxdepth 3 -name "*.js" -type f | head -1 | grep -q .; then
    echo "JAVASCRIPT detected - load: js/README.md"
fi

if find . -maxdepth 4 -name "*.css" -type f | head -1 | grep -q .; then
    echo "CSS detected - load: css/README.md"
fi

if find . -maxdepth 3 -name "*.rs" -type f | head -1 | grep -q .; then
    echo "RUST detected - load: rust/README.md"
fi

if find . -maxdepth 3 -name "*.php" -type f | head -1 | grep -q .; then
    echo "PHP detected - load: php/README.md"
fi

if [[ -f "*.sln" ]] || find . -maxdepth 3 -name "*.csproj" -o -name "*.sln" -type f 2>/dev/null | head -1 | grep -q .; then
    echo "CSHARP detected - load: csharp/README.md"
    echo "  If initializing new project: get_rule(\"csharp/init.md\")"
fi

echo "=== WORKFLOW: proj/PROJECT → proj/FIXES → proj/TODO → code → test ==="

# Scan for oversized files — AI must split these before adding new code
echo ""
echo "=== OVERSIZED FILES (must split before adding code) ==="
LIMITS=(
  "py:250" "ts:250" "tsx:100" "js:250" "jsx:100"
  "css:150" "scss:150" "kt:200" "swift:200"
  "rs:300" "cpp:350" "c:350" "cs:300"
)
FOUND=0
for entry in "${LIMITS[@]}"; do
  ext="${entry%%:*}"
  limit="${entry##*:}"
  while IFS= read -r f; do
    lines=$(wc -l < "$f")
    if (( lines >= limit )); then
      echo "  OVERSIZED ($lines lines, limit $limit): $f"
      FOUND=1
    fi
  done < <(find src/ -name "*.$ext" -type f 2>/dev/null)
done
if (( FOUND == 0 )); then
  echo "  OK — no oversized files found"
fi
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
