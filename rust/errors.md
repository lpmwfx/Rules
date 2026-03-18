---
tags: [errors, result, thiserror]
concepts: [error-handling, result-types]
requires: [rust/types.md, global/error-flow.md]
keywords: [result, thiserror, anyhow, question-mark, exhaustive-match]
layer: 3
---
# Error Handling

> Result types — thiserror for libs, exhaustive match at every call site

---

RULE: `Result<T, E>` for fallible operations
RULE: `thiserror` for custom errors in libs and apps
RULE: `anyhow` ONLY at CLI/bin top-level (never in lib or app core)
RULE: `?` operator for propagation — never unwrap mid-function
RULE: Match error variants exhaustively — each arm has a named recovery action
RULE: See `global/error-flow.md` for taxonomy (Transient/UserError/SystemError/Bug)

```rust
// Custom error type
#[derive(Debug, thiserror::Error)]
pub enum ConfigError_x {
    #[error("File not found: {0}")]
    NotFound(PathBuf),
    #[error("Parse error: {0}")]
    Parse(#[from] toml::de::Error),
}

// Propagate with ?
pub fn load_config(path: &Path) -> Result<Config, ConfigError_x> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| ConfigError_x::NotFound(path.to_owned()))?;
    Ok(toml::from_str(&content)?)
}

// At adapter boundary — exhaustive, no wildcard
fn apply_config(result: Result<Config, ConfigError_x>, ui: &mut UIState) {
    match result {
        Ok(cfg)                         => ui.apply(cfg),
        Err(ConfigError_x::NotFound(p)) => ui.show_error(&format!("Config not found: {}", p.display())),
        Err(ConfigError_x::Parse(e))    => ui.show_error(&format!("Config invalid: {e}")),
        // No _ arm — compiler enforces all variants are handled
    }
}
```

BANNED: `unwrap()`/`expect()` outside tests
BANNED: `panic!()` for recoverable errors
BANNED: `Box<dyn Error>` (use concrete error types)
BANNED: Wildcard `_ => {}` error arm that discards without action
BANNED: `_ => eprintln!(...)` — log without recovery at a recoverable call site
