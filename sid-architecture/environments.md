---
tags: [sid, environments, compiled, interpreted, boundary, parser, medium]
concepts: [compiled-vs-interpreted, architectural-boundary, medium-draws-line, parser-as-compiler]
requires: [sid-architecture/code-free-of-mutables.md, sid-architecture/data-driven-runtime.md]
related: [sid-architecture/meta-driven-ui.md, sid-architecture/data-driven-runtime.md]
keywords: [compiled, interpreted, boundary, parser, medium, Rust, TypeScript, PWA, disk, database, HTML, JSON]
layer: 2
binding: false
status: prototype
---
# Environments

> Compiled environments have an automatic boundary. Interpreted environments require an architectural boundary. The medium often chooses for you.

---

RULE: In compiled environments the compiler automatically draws the boundary between Principle 02 and 03
RULE: In interpreted environments the architecture must create the boundary — build a parser/loader that distinguishes sources
RULE: The medium draws the boundary naturally — HTML+JS are easy on disk, JSON is easy in database
RULE: UI is always Principle 03 regardless of environment

## Compiled Environment

Rust, C++, Go, compiled Swift, Slint-to-Rust, Svelte-to-bundle.

- Everything the compiler sees = Principle 02 (baked in, locked after compile)
- Everything the engine fetches after start = Principle 03 (live data)
- Lower discipline requirement — the language enforces the boundary

## Interpreted Environment

TypeScript, JavaScript, Python, Ruby.

- No compile phase separating build-time from runtime
- Everything can technically be either
- Higher discipline requirement — you must choose per situation

## Parser as Artificial Compiler

Interpreted environments can get sharp separation via a parser:

- Engine + widget files from disk = "code" (Principle 02)
- Compositions + records from database = "data" (Principle 03)
- The parser is the border guard — enforces separation like a compiler would

## The Medium Draws the Line

- HTML and JS are easy on disk — syntax highlighting, diffing, git
- JSON is easy in database — queryable, many small changes, no deploy

Placing each thing where it is easiest falls precisely on the Principle 02/03 boundary. Not ideology — pragmatism that matches the principles.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
