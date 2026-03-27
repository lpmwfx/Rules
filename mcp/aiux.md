---
tags: [mcp, aiux, help, manpage, pull-model, documentation, tool-design]
concepts: [ai-ux, pull-documentation, self-documenting-tools, help-manpage-pattern]
requires: [mcp/server-build.md, mcp/README.md]
related: [mcp/event-adapter.md, mcp/app-server.md]
keywords: [help, manpage, pull, push, documentation, onboarding, tool-description, man, --help, stereotypes]
layer: 3
---
# AIUX — UX for AI

> Pull-based documentation — AI asks when it needs, zero overhead when it knows

---

## The Problem

Push-model: long descriptions, verbose responses, help called automatically. Fills the context window on every call — even for an AI that already understands the system. Tokens wasted.

Pull-model: short descriptions, concise responses. AI pulls documentation when it needs it. One call to learn, then short calls forever. Information is always one call away but never forced.

RULE: Pull over push — AI requests information, server never pushes unsolicited context
RULE: Tool descriptions are short (one line) — detail lives in manpage

## Two Levels of Pull

Two stereotypes AI knows from training data:

| Level | Parameter | Stereotype | Purpose |
|---|---|---|---|
| System | `help` | `--help` | What is this MCP, what can it do, where to start |
| Tool | `manpage` | `man <command>` | Full explanation of one specific tool |

Both are optional params on every tool. When set, the tool returns documentation instead of executing. When not set, the tool runs normally. Zero overhead.

RULE: Every tool has `help` and `manpage` as optional params
RULE: `help` returns the same system overview from any tool — no wrong starting point
RULE: `manpage` returns the full explanation of that specific tool
RULE: Help takes priority over manpage — if both are set, return help

## help — System Onboarding

Every tool returns the **same** system overview when `help` is set. AI doesn't know which tool is "the right one" to call first — any tool works.

```
any_tool({ help: "1" })  →  system overview
```

### What help returns:
- What this MCP server connects to
- All tools grouped by workflow (not alphabetical)
- Defaults, organizations, repos
- Typical workflows: "to do X, call A then B"
- Auth context: who am I, what can I do

RULE: help text is one shared constant across all tools
RULE: Group tools by workflow — AI thinks in tasks, not alphabetical lists
RULE: Include concrete examples with real values — not placeholders

## manpage — Tool Documentation

Each tool has its own manpage with the full explanation:

```
write_file({ manpage: "1" })  →  full write_file documentation
```

### Manpage structure:
1. **One sentence** — what the tool does
2. **Parameters** — what they are, what they expect, examples
3. **How it works** — step-by-step internals
4. **Important** — gotchas, limitations, edge cases
5. **Related** — what to call before/after this tool
6. **Example** — realistic call with expected output

RULE: Start with one sentence — AI decides to read further or not
RULE: Include a realistic example — AI learns from concrete calls, not abstractions
RULE: Document gotchas — silent failures are invisible to AI

## Implementation

```typescript
const SYSTEM_HELP = `# MyServer MCP\n\nConnects to...\n\n## Tools\n...`;

const WRITE_FILE_MANPAGE = `# write_file\n\nCreates or updates a file...\n...`;

server.registerTool("write_file", {
  description: "Create or update a file in a repository",
  inputSchema: {
    help: z.string().optional().describe("System overview"),
    manpage: z.string().optional().describe("Full tool documentation"),
    repo: z.string().describe("Repository name"),
    // ...
  },
}, async ({ help, manpage, repo, ...rest }) => {
  if (help !== undefined) return ok(SYSTEM_HELP);
  if (manpage !== undefined) return ok(WRITE_FILE_MANPAGE);
  // ... normal execution
});
```

RULE: Use `z.string().optional()` not `z.boolean()` — MCP transports serialize booleans inconsistently
RULE: Check with `!== undefined` not truthiness — avoids string "false" issues
RULE: `SYSTEM_HELP` is one constant shared by all tools
RULE: Each tool has its own `MANPAGE` constant
RULE: `help` and `manpage` are always the first params in inputSchema
RULE: Required params are optional in schema — validated in handler after aiux check

## Response Helpers

Standard helpers for consistent response format across all tools:

```typescript
function ok(text: string) {
  return { content: [{ type: "text" as const, text }] };
}

function err(msg: string) {
  return { content: [{ type: "text" as const, text: msg }], isError: true as const };
}

function aiux(toolName: string, args: { help?: string; manpage?: string }): string | null {
  if (args.help !== undefined) return SYSTEM_HELP;
  if (args.manpage !== undefined) return MANPAGES[toolName] ?? `No manpage for ${toolName}`;
  return null;
}
```

RULE: Use `ok()` and `err()` — never construct content arrays inline
RULE: `aiux()` check is always the first line in every tool handler
RULE: Store manpages in a `MANPAGES: Record<string, string>` — one entry per tool

## Why Stereotypes Work

`--help` and `man` are universal — AI knows them from training data. No new concepts to learn. The pattern scales from 5 tools to 50 with zero additional complexity.

BANNED: Long descriptions as the primary documentation method — tokens wasted on every list_tools call
BANNED: Auto-calling help on first tool use — AI decides when to ask
BANNED: Tool-specific help that differs from the system overview — help is always the same
