---
tags: [rules, ai-coding, standards, overview]
concepts: [coding-standards, ai-rules]
layer: 6
---
# Rules — AI Coding Standards

Shared coding standards for AI-assisted development across Python, JavaScript, CSS, C++, Rust, and Kotlin.

Used by: Claude Code, Cursor, Copilot, Codex, Mistral, and any AI coding assistant.

## Categories

| Category | Files | Topic |
|----------|-------|-------|
| [global/](global/) | 11 | Universal rules — all languages, all projects |
| [project-files/](project-files/) | 11 | Institution file specs (PROJECT, TODO, FIXES, RAG) |
| [automation/](automation/) | 5 | Session startup context injection |
| [devops/](devops/) | 4 | AI:DevOps workflow, publishing, CI/CD, packaging |
| [ipc/](ipc/) | 1 | Unix socket + JSON-RPC 2.0 contract |
| [platform-ux/](platform-ux/) | 6 | Platform UX defaults (GNOME HIG) |
| [python/](python/) | 10 | Python 3.11+ rules |
| [js/](js/) | 10 | JavaScript (TS-like-JS) rules |
| [css/](css/) | 9 | CSS rules (cascade by design) |
| [cpp/](cpp/) | 10 | C++20/23 rules (Linux/BSD) |
| [rust/](rust/) | 10 | Rust 2021 rules |
| [kotlin/](kotlin/) | 10 | Kotlin Compose + Amper rules |

## Core Idea

AI forgets between sessions. These files are persistent memory:
- AI reads them for context and coding standards
- Same patterns across all languages (Result types, closed modules, flat nesting)
- RAG + FIXES files grow over time = AI gets smarter on the project

## MCP Server

Install the companion MCP server for IDE integration:

```bash
pipx install git+https://github.com/lpmwfx/RulesMCP.git
claude mcp add -s user rules -- rules-mcp
```

## License

EUPL-1.2
