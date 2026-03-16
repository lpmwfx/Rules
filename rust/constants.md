---
tags: [rust, constants, no-hardcoding, zero-literals, states, no-literals, rustscanners]
concepts: [zero-literals, named-values, state-files, data-driven, rust-build-scan]
requires: [global/config-driven.md, rust/types.md]
feeds: [rust/naming.md, rust/init.md]
related: [slint/states.md, uiux/tokens.md, global/topology.md, rust/init.md]
keywords: [const, static, magic-number, duration, timeout, literal, state, state-folder, zero-literal, rustscanners, build-scan, cargo-scan]
layer: 3
---
# Rust Zero Literals — All Values Named

> All hard values live in `state/` modules or `_cfg` structs. Function bodies contain zero literals.

---

VITAL: ANY literal in a function body is hardcoding — `2 + 2` has TWO violations
VITAL: Literals live ONLY in definition files — `state/` modules, `const`, or `_cfg` structs
VITAL: One state file per concern — format is open (`.rs`, `.toml`, `.json`, `.yaml`)
RULE: Only `0` and `1` are allowed bare in function bodies (indexing, ranges, arithmetic)
RULE: `2` in `a = b + 2` is a violation — use `a = b + STEP` from state module
RULE: `0.5` in `x * 0.5` is a violation — use `x * HALF` from state module
RULE: Every Duration, capacity, URL, threshold, factor is a named reference
BANNED: ANY integer ≥ 2 in function bodies — use named value from `state/` or `_cfg`
BANNED: ANY float except `0.0`/`1.0` in function bodies — use named value
BANNED: `Duration::from_secs(30)` — use `Duration::from_secs(CONNECT_TIMEOUT_SECS)`
BANNED: `Vec::with_capacity(1024)` — use `Vec::with_capacity(BUF_SIZE)`
BANNED: `"https://..."` / `"http://..."` outside state/const — URLs are named values
BANNED: `if retries > 3` — use `if retries > MAX_RETRIES`

## Create-Before-Use Workflow

VITAL: Named constants do not pre-exist — YOU create them as you write code.
VITAL: When you need a value, define the const FIRST, then reference it.

```
Before writing ANY literal number, path, URL, or duration in Rust:

1. IDENTIFY where the value belongs:
   - Buffer size, capacity, divisor → state/sizes.rs     (const)
   - Timeout, interval, delay       → state/durations.rs (const)
   - Max count, threshold, limit    → state/limits.rs    (const)
   - File path, extension           → state/paths.rs     (const)
   - URL, endpoint                  → state/urls.rs      (const or _cfg)
   - Runtime-changeable value       → _cfg struct        (loaded by Gateway)

2. SEARCH the target module for an existing const
   - Need 1024? → search sizes for "BUF_SIZE" or "CAPACITY"
   - Need 30?   → search durations for "TIMEOUT" or limits for "MAX_RETRIES"

3. Const EXISTS → reference it:  sizes::BUF_SIZE

4. Const does NOT EXIST →
   a. OPEN the state module (e.g. src/state/sizes.rs)
   b. ADD:  pub const BUF_SIZE: usize = 1024;
   c. SAVE the file
   d. THEN use sizes::BUF_SIZE in your function

5. NEVER write the literal in the function body — not even temporarily
```

RULE: The developer creates constants — state/ modules start minimal
RULE: "No const for this value" means "create it now" — not "use the literal"
RULE: If the state/ folder does not exist yet, create it (see rust/init.md)

## Rust Exemptions (6 total)

Six constructs where bare literals are required or idiomatic:

| Construct | Reason | Example |
|-----------|--------|---------|
| `0` and `1` | Universal index/range/arithmetic | `arr[0]`, `0..n`, `x + 1` |
| `const`/`static` definitions | That IS the named value | `const STEP: usize = 2;` |
| Test code (`#[test]`/`#[cfg(test)]`) | Tests need specific values | `assert_eq!(result, 42)` |
| Format/log macro strings | Compile-time templates | `format!("count: {}")` |
| Derive/attribute macros | Compile-time metadata | `#[derive(Debug)]` |
| Enum variant definitions | These ARE the named values | `enum State { Active = 1 }` |

RULE: These six are the ONLY allowed literals. The scanner exempts them automatically.

## State Folder

One file per concern. Format is project-specific — `.rs` with `const`, `.toml`, `.json`, `.yaml` all valid.

```
src/state/      or    config/state/
├── sizes.*              ← buffer sizes, capacity hints, divisors
├── durations.*          ← timeouts, retry delays, intervals
├── limits.*             ← max counts, thresholds, retry limits
├── paths.*              ← file names, config paths, extensions
└── urls.*               ← API endpoints, service URLs
```

RULE: Gateway loads non-Rust formats → `_cfg` struct. Rust `const` files are used directly.

## Where Values Live

| Value type | Source | Access pattern |
|------------|--------|----------------|
| Runtime thresholds/limits | Config → `_cfg` | `cfg.max_items` |
| Compile-time sizes/factors | `state/` (any format) | `sizes::BUF_SIZE` or `cfg.buf_size` |
| Timeouts/durations | `state/` (any format) | `CONNECT_TIMEOUT_SECS` or `cfg.timeout` |
| URLs/endpoints | `state/` or `_cfg` | `urls::API_BASE` or `cfg.api_url` |
| File paths/names | `state/` | `paths::CONFIG_FILE` |

RULE: "Is this value changeable without recompile?" → config `_cfg`. Otherwise → `state/` module.

RESULT: Every value has a named source — function bodies are pure expressions with zero literals
REASON: The scanner catches ANY literal ≥ 2 in function bodies as ERROR — enforceable architecture
