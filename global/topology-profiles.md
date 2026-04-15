---
tags: [topology, profiles, project-types, architecture, mcp, cli, tui, pwa, desktop, mobile]
concepts: [topology-profiles, project-type-mapping, layer-activation, mcp-dual-placement]
requires: [global/topology.md, global/app-model.md]
feeds: [php/laravel/topology.md, js/topology-cli.md, js/topology-mcp.md, web/topology.md, rust/topology.md, mcp/app-server.md, mcp/server-build.md]
related: [global/adapter-layer.md, mcp/event-adapter.md, project-files/project-file.md]
keywords: [profile, gui, cli, tui, mcp, daemon, pwa, spa, wa, blade, desktop, mobile, server, project-type, standalone, embedded, layer-activation, web-api, ssg, build-tool, db-server]
layer: 1
binding: true
---
# Topology Profiles

> Same 6 layers, different activation — the project type determines which layers exist

---

AXIOM: The topology from global/topology.md is always the reference — profiles activate a subset
AXIOM: A layer is either fully present or entirely absent — no partial layers, no empty folders
VITAL: The project type determines which layers are active — decided once at project init
VITAL: Import rules apply only between active layers — absent layers have no folders, no files, no imports
RULE: PROJECT file declares the active profile — e.g. `topology: desktop` or `topology: mcp-standalone`
RULE: Scanner only checks import rules between layers that exist in the project

## Profile Table

| Profile | UI | Adapter | Core | PAL | Gateway | Shared | MVVM |
|---------|:--:|:-------:|:----:|:---:|:-------:|:------:|:----:|
| **desktop** (Qt, Slint, GTK) | x | x | x | x | x | x | yes |
| **mobile** (Compose, SwiftUI) | x | x | x | x | x | x | yes |
| **tui** (ratatui, Textual) | x | x | x | x | x | x | yes |
| **gui-web** (Laravel+Svelte) | x | x | x | — | x | x | yes |
| **pwa** (Svelte, React + SW) | x | x | x | — | x | x | yes |
| **wa** (SPA, no SW) | x | x | x | — | x | x | yes |
| **mcp-embedded** (`--mcp` flag) | x | x | x | x | x | x | yes |
| **mcp-standalone** (HTTP service) | x | — | x | — | x | x | no |
| **mcp-stdio** (rmcp, FastMCP) | x | — | x | — | x | x | no |
| **web-api** (Axum, FastAPI, Hono) | — | — | x | — | x | x | no |
| **daemon** (background service) | — | x | x | x | x | x | no |
| **db-server** (pgwire, custom DB) | — | x | x | x | x | x | no |
| **ws** (WebSocket server) | — | — | x | — | x | x | no |
| **cli** (args → stdout) | — | — | x | x | x | x | no |
| **ssg** (Astro, Jinja2, SvelteKit static) | x | — | x | — | x | x | no |
| **build-tool** (scanner, codegen) | — | — | x | — | x | x | no |
| **blade-admin** (thin server UI) | x | x | x | — | x | x | yes |
| **library** (crate, package) | — | — | x | — | — | x | no |

## Why Each Layer Appears or Not

### UI — present when there is a rendering surface

Desktop, mobile, TUI, PWA, WA: GUI is the human's rendering surface.
MCP (embedded + standalone + stdio): MCP tools are the AI's rendering surface.
SSG: templates are the rendering surface — they produce HTML output.
CLI: no rendering surface — args in, stdout out, exit.
Web-API: no surface — endpoints are IO (Gateway), not UI.
Daemon, db-server: no surface — they run headless.
Build-tool: no surface — runs at compile-time, produces artifacts.
Library: no surface at all — pure API.

RULE: If something presents an interface to a user (human or AI) → UI layer exists

### Adapter — present when there is live state between a UI and Core

GUI apps (desktop, mobile, TUI, PWA, WA): UI is reactive, state changes trigger re-renders. Adapter is the hub that holds AdapterState_sta and routes events between UI and Core.
MCP-embedded: shares Adapter with GUI — same events, same state, same ViewModel. This is the entire point: adding MCP to a GUI app changes nothing in Core.
MCP-standalone/stdio: request-response — no persistent UI state between calls. Tool receives request, calls Core, returns result. No Adapter needed.
CLI, build-tool, ssg: request-response — parse args/config, call Core, produce output, exit. No live state.
Web-API: request-response — each HTTP request is independent. No shared UI state.
Daemon, db-server: manage long-running state — Adapter coordinates it.

VITAL: Adapter exists because two surfaces share live state — not because the app is "complex"
RULE: If only one UI surface exists AND it is request-response → no Adapter
RULE: If multiple surfaces share state (GUI + MCP, GUI + API) → Adapter is mandatory

### Core — always present

Every project has business logic. Even a library is Core + Shared. Core is pure — no IO, no platform, no UI.

### PAL — present when the app runs on multiple platforms

Desktop: Windows, macOS, Linux — filesystem paths, window APIs, notifications differ.
Mobile: iOS, Android — sensors, permissions, lifecycle differ.
TUI: terminal abstraction — different terminal emulators, Windows vs Unix escape codes.
CLI: often cross-platform — filesystem, paths, shell behavior differ.
MCP-embedded: inherits PAL from its host app.
MCP-standalone/stdio: single platform (typically one server OS) — no PAL.
Web-API: single server platform — no PAL.
PWA/WA/SSG: browser is the platform — Web APIs are direct, not abstracted through PAL.
Daemon, db-server: often cross-platform — PAL wraps OS differences.
Build-tool: usually single platform — no PAL.

RULE: If the app targets exactly one platform with no plan to port → skip PAL
RULE: If the app targets browser → browser IS the platform, Web APIs are direct

### Gateway — present when the app does IO

All apps except libraries touch disk, network, or external services. Gateway owns all IO: config loading, state persistence, API calls, database access.
Library: pure logic, no IO — caller provides data.

### Shared — always present (in multi-layer projects)

Cross-layer types (errors, results, enums) exist in every project with 2+ layers.

RULE: A type belongs in shared only if it is imported by 2+ layers
RULE: If a type is only used within one layer, it belongs in that layer
BANNED: `utils/`, `helpers/`, `common/` as shared — shared holds types and constants, not logic
BANNED: Functions in shared — shared holds types and constants, not logic

## MCP: The Dual-Nature Layer

MCP behaves fundamentally differently depending on whether it is embedded in an app or standalone. This is the most important distinction in the profile table.

### MCP Embedded (`--mcp` flag in a desktop/mobile/TUI app)

```
GUI (_ui)  ──events──►  Adapter (_adp)  ◄──events──  MCP tools (_ui)
                              │
                            Core (_core)
                              │
                            PAL (_pal)
                              │
                         Gateway (_gtw)
                           ├── disk IO
                           ├── network
                           └── MCP transport (stdio)
```

VITAL: MCP tools are `_ui` — parallel to GUI, same layer, same import rules
VITAL: MCP tools fire Adapter events — same `on_save`, `on_close` as GUI buttons
VITAL: MCP transport (stdio) is `_gtw` — IO infrastructure, not UI
RULE: Adding MCP to a GUI app requires zero changes to Core, PAL, or Gateway logic
RULE: MCP tools read from AdapterState_sta — same observable state as GUI
RULE: MCP tool names map to Adapter event names — they are not independent identifiers
BANNED: MCP tools calling Core directly — must route through Adapter events
BANNED: MCP tools with logic not available to GUI — same capabilities, different surface

The key insight: MCP spans two layers simultaneously in an embedded app.
The **tool handlers** are UI (`_ui`) — they define what the AI sees and can do.
The **transport** is Gateway (`_gtw`) — it handles stdio/HTTP IO.
The Adapter connects them — same hub, same events, same state as the GUI.

### MCP Standalone (independent HTTP service)

```
MCP tools (_ui)
    │
    ├── tool calls ──►  Core (_core)
    │                      │
    │                      ▼
    │                   business logic
    │
    └── auth/transport ──►  Gateway (_gtw)
                              ├── OAuth 2.1
                              ├── HTTP transport
                              └── external APIs
```

VITAL: No Adapter — tools call Core directly or delegate to Gateway
VITAL: No PAL — single deployment target
VITAL: No GUI — MCP tools are the only surface
RULE: Tool handlers are still `_ui` — they define the AI's interface
RULE: Tools are thin — validate input, call Core or Gateway, return result
RULE: Auth and transport are `_gtw` — IO infrastructure
BANNED: Business logic in tool handlers — delegate to Core modules
BANNED: Tool handlers doing direct IO (disk, network) — delegate to Gateway

The standalone MCP server is the simplest multi-layer profile:
UI (tools) → Core (logic) → Gateway (IO). Three active layers.

### MCP Stdio (rmcp, FastMCP — subprocess launched by AI client)

Same profile as standalone — UI + Core + Gateway, no Adapter, no PAL.
The only difference is transport: stdio instead of HTTP, no OAuth (client manages auth).

RULE: mcp-stdio and mcp-standalone have identical layer topology — only Gateway transport differs
RULE: mcp-stdio tools follow the same rules as mcp-standalone tools

## Profile Selection Guide

RULE: Pick the profile that matches your app's actual needs — not aspirational needs
RULE: Start minimal — add layers when the need arises, not before

| Question | Yes → | No → |
|----------|-------|------|
| Does it have a visual/tool interface? | UI layer | No UI |
| Does it have reactive state shared between surfaces? | Adapter layer | No Adapter |
| Does it run on multiple OS/platforms? | PAL layer | No PAL |
| Does it do IO (disk, network, DB)? | Gateway layer | No Gateway |
| Does it have types used by 2+ layers? | Shared layer | No Shared |

## Layer Definitions

Each layer has a dedicated definition file — read these for full rules.

| Layer | Tag | Definition | Responsibility |
|---|---|---|---|
| ui | `_ui` | [uiux/README.md](../uiux/README.md) | Declarative rendering — views, components, MCP tools |
| adapter | `_adp` | [adapter/viewmodel.md](../adapter/viewmodel.md) | Data exchange hub — transforms between core and ui/stdio/tools |
| core | `_core` | [core/design.md](../core/design.md) | Business logic — pure functions, domain rules, no IO |
| gateway | `_gtw` | [gateway/io.md](../gateway/io.md) | IO boundary — disk, network, processes, DB, MCP transport |
| pal | `_pal` | [pal/design.md](../pal/design.md) | Platform abstraction — OS, runtime, hardware interfaces |
| shared | `_x` | above | Cross-layer types — errors, result types, enums used by 2+ layers |

## Per-Profile Twins

Each profile has a concrete mapping file in its language/framework area:

| Profile | Twin file |
|---|---|
| desktop (Rust+Slint) | [rust/topology.md](../rust/topology.md) |
| gui-web (Laravel+Svelte) | [php/laravel/topology.md](../php/laravel/topology.md) |
| pwa / wa | [web/topology.md](../web/topology.md) |
| cli (Bun/Node) | [js/topology-cli.md](../js/topology-cli.md) |
| mcp-standalone (Bun) | [js/topology-mcp.md](../js/topology-mcp.md) |
| blade-admin | [php/laravel/topology.md](../php/laravel/topology.md) |

## Examples

### Desktop app with MCP (profile: desktop + mcp-embedded)
All 6 layers active. MCP tools in `src/ui/mcp/`, GUI in `src/ui/views/`.
Both fire events to `src/adapter/`. `--mcp` flag switches UI surface at startup.
*Projects: GameEditor002, rich-text-editor*

### MCP standalone HTTP (profile: mcp-standalone)
Tool handlers → business logic → auth/IO. No Adapter, no PAL.
*Projects: ai-gov (rules, scan, vcs, project, services)*

### MCP stdio server (profile: mcp-stdio)
Same as standalone — tools → Core → Gateway. Transport is stdio, not HTTP.
*Projects: gui-mcp, game-editor-mcp, audienceintelligence, carussel*

### Web API server (profile: web-api)
Endpoints → business logic → IO. No UI (endpoints are Gateway, not a rendering surface).
*Projects: mimer-api (Hono), articles-pwa (Axum), PseudoID (FastAPI)*

### Static site generator (profile: ssg)
Templates (UI) → content processing (Core) → file output + translation API (Gateway).
Templates are the rendering surface — they produce the final HTML.
*Projects: LpmathiasenCOM (Astro), EUPsID (Jinja2), NorthHeimSite (Jinja2+Babel)*

### TUI application (profile: tui)
Full stack — reactive terminal UI with Adapter state, just like a GUI.
*Projects: MistralCoder (Textual), ClaudeCLI-Wrapper (crossterm)*

### CLI tool (profile: cli)
Args → Core → stdout. PAL for cross-platform filesystem/paths.
*Projects: RulesTools CLI, codeberg-cli, Articles-on-webhost*

### Build-time tool (profile: build-tool)
Runs at compile-time, scans/generates code. Core + Gateway, no UI, no PAL.
*Projects: rulestools-scanner, rulestools-documenter, SlintScanners*

### Library (profile: library)
Pure logic, no IO. Caller provides data.
*Projects: gamepod-infra (rusqlite), piper-sys (FFI bindings)*

### Full-stack webapp (profile: gui-web)
Svelte components → Inertia/controllers (Adapter) → domain logic → DB/disk.
*Projects: articles-system (Laravel+Svelte)*

### Database server (profile: db-server)
Persistent connections, long-running state. Adapter coordinates sessions.
*Projects: tool-db (pgwire+libsql)*

RESULT: Every project maps to exactly one profile — the profile determines folder structure and active layers
REASON: No wasted layers, no missing layers — the topology fits the project exactly
