---
tags: [global, tooling, scripts, definitions, dev-environment]
concepts: [tools-vs-scripts, ownership, dev-tooling]
requires: [global/module-tree.md]
feeds: [global/initialize.md, js/project-structure.md, devops/packaging.md, project-files/install-file.md]
keywords: [tool, script, bun, node, vite, eslint, tsc, composer, build, dev-server, task-runner, automation]
layer: 1
---
# Tools and Scripts

> Tools are dependencies you configure — scripts are code you own

---

## Definitions

**Tool** — an external program installed and configured but not written by you. Vite, ESLint, tsc, Composer, Bun, Cargo, PHPStan. You depend on it. Updates come from upstream.

**Script** — code you write to automate project tasks. Build scripts, deploy scripts, data migration, code generation, index builders, test helpers. You own it. Changes come from you.

RULE: Tools are dependencies — scripts are owned code. The distinction determines where they live and how they are managed.

## Where They Live

| Type | Location | Managed by |
|------|----------|------------|
| Tool | `package.json`, `composer.json`, `Cargo.toml` | Package manager |
| Script | `tools/` directory at project root | You |
| Tool config | Project root (`.eslintrc`, `vite.config.ts`, `tsconfig.json`) | You |
| Script entry | `package.json` scripts section, `Makefile`, `composer scripts` | You |

RULE: Scripts belong in `tools/` — not scattered in project root or `src/`
RULE: Tool configuration lives in project root — one config file per tool
BANNED: Scripts outside `tools/` (except `package.json` scripts entries that call tools)
BANNED: Tool source code copied into the project — install it as a dependency

## Runtime

Bun is the default runtime — native TypeScript execution, no compile step, fast startup. All owned code (scripts, tools, servers) runs on Bun.

Node is slow for JS/TS and requires a build step for TypeScript. It is only used when a framework tool requires it (Vite, SvelteKit, Next.js).

A project can use both runtimes when they serve different roles. The boundary must be structural — defined by config, not by accident.

RULE: Bun is the default runtime for all owned JS/TS code
RULE: Node is only accepted for framework tooling that requires it
RULE: When both runtimes exist in a project, the boundary is structural — each part declares its runtime in config (`package.json` engine, script shebang, or runner config)
RULE: Owned scripts always use Bun — even in projects where framework tooling uses Node

```
# Example: Laravel + Inertia + Svelte project
tools/                  ← Bun (owned scripts)
  deploy.ts             ← bun run tools/deploy.ts
  generate-types.ts     ← bun run tools/generate-types.ts
vite.config.ts          ← Node (framework requires it)
package.json            ← scripts section declares which runner per task
```

## Runtime Declaration

AI assistants are structural — they follow declarations, not preferences. When runtime is ambiguous, AI guesses. Guesses cause wrong runner, wrong flags, wrong behavior. Every executable file must declare its runtime so no interpretation is needed.

Three levels of declaration:

### 1. Shebang — file declares its own runtime

```typescript
#!/usr/bin/env bun
// tools/deploy.ts — self-declaring, no ambiguity
```

```bash
chmod +x tools/deploy.ts
./tools/deploy.ts     # runs with Bun, always
```

### 2. Bin entries — project registers commands with bound runtime

```json
{
  "bin": {
    "deploy": "./tools/deploy.ts",
    "gen-types": "./tools/generate-types.ts"
  }
}
```

```bash
bun link              # registers as global commands
deploy                # runs tools/deploy.ts with Bun — from anywhere
```

### 3. Package.json scripts — explicit runner per task

```json
{
  "scripts": {
    "deploy": "bun tools/deploy.ts",
    "gen-types": "bun tools/generate-types.ts",
    "dev": "vite",
    "build": "vite build"
  }
}
```

Runner is visible in the command — `bun tools/...` vs `vite` (Node).

RULE: Every owned script must have a shebang declaring its runtime
RULE: Use bin entries to expose project scripts as named commands
RULE: Package.json scripts must use explicit runner prefix (`bun`, `node`, or tool name) — never bare `ts` files without runner

BANNED: Running owned scripts on Node when Bun can run them
BANNED: Adding a TypeScript build step when Bun runs .ts directly
BANNED: Implicit runtime choice — if both runtimes exist, every entry point must declare which one
BANNED: Bare script paths in package.json without explicit runner (ambiguous to AI and humans)

## Script Conventions

```
tools/
├── build-register.py     # Index generator
├── deploy.ts             # Deploy automation (Bun)
├── migrate-data.ts       # One-off migration
└── generate-types.ts     # Code generation
```

Scripts are first-class project code — same quality standards as `src/`. They are exempt from print restrictions and nesting limits (see [initialize.md](initialize.md)).

RULE: Scripts follow the same naming and module conventions as project code
RULE: One script, one job — no multi-purpose script files
