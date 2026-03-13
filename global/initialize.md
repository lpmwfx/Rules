---
tags: [initialize, project-init, setup, bootstrap, one-time, mandatory]
concepts: [project-initialization, project-setup, bootstrap]
requires: [global/startup.md]
feeds: [project-files/project-file.md, project-files/rules-file.md, project-files/todo-file.md, project-files/fixes-file.md, project-files/uiux-file.md]
related: [automation/startup-script.md, rust/init.md, csharp/init.md, slint/init.md]
keywords: [initialize, init, bootstrap, setup, new project, proj, create, initialiser]
layer: 1
---
# Project Initialization

> Run once — when proj/ does not exist or user says "initialize project"

---

VITAL: This sequence runs ONCE per project — not every session (that is startup.md)
VITAL: Do not skip steps — each step feeds the next
VITAL: After completion, run the full startup.md checklist to verify

```
PROJECT INITIALIZATION SEQUENCE:

0. INSTALL hooks      → mcp__rulestools__setup(".")
                         installs PostToolUse hook + pre-commit gate

1. DETECT languages   → rulestools detect .
                         writes proj/rulestools.toml with detected languages

1b. LANGUAGE INIT     → if a language-specific init.md exists, run it BEFORE step 3:
                         Rust       → get_rule("rust/init.md")    — installs RustScanners,
                                       creates src/state/ folder, build.rs, proj/rulestools.toml
                         Slint      → get_rule("slint/init.md")   — installs SlintScanners,
                                       creates ui/ definition folders, tokens, theme globals
                         C# / .NET  → get_rule("csharp/init.md")  — scaffolds sln, csproj,
                                       Directory.Build.props, .editorconfig, .gitignore
                         (other languages: add init.md when available)

2. FIND source doc    → look for: README.md  doc/project.md  brief.md  doc/PROJECT.md
                         if found: read it — it becomes the basis for proj/PROJECT
                         if not found: ask user for goal, stack, and structure

3. CREATE proj/PROJECT → write project state in standard format
                         see: project-files/project-file.md
                         source doc is now frozen — proj/PROJECT is the only truth

4. CREATE proj/RULES  → list active MCP rules for detected languages
                         see: project-files/rules-file.md

5. CREATE proj/TODO   → initial task list for phase 1
                         see: project-files/todo-file.md

6. CREATE proj/FIXES  → create empty — populated as issues are discovered
                         see: project-files/fixes-file.md

7. CREATE proj/UIUX   → ONLY if GUI files detected (*.slint *.tsx *.qml *.swift *.ui)
                         see: project-files/uiux-file.md
                         ask user for platform, flows, and conventions

8. VERIFY             → run startup.md checklist — all proj/ files must be readable
```

RULE: All proj/ files are created in one session — do not leave initialization partial
RULE: Ask the user before creating proj/UIUX — confirm it is a GUI project
RULE: proj/PROJECT.Current.phase must be "1" after initialization
BANNED: Skipping step 0 — hooks must be installed before any code is written
BANNED: Creating proj/ files from assumptions — always read the source doc or ask the user
BANNED: Leaving initialization partial — either complete all steps or none
