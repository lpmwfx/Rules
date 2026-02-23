# Error Handling

> Result types — thiserror for libs, anyhow for CLI

---

RULE: `Result<T, E>` for fallible operations
RULE: `thiserror` for custom errors in libs
RULE: `anyhow` ONLY in CLI/bin boundaries
RULE: NO `unwrap()/expect()` in library code (ok in tests)
RULE: `?` operator for propagation

```rust
// Custom error type (library code)
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("File not found: {0}")]
    NotFound(PathBuf),
    #[error("Parse error: {0}")]
    Parse(#[from] toml::de::Error),
}

// Usage
pub fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| ConfigError::NotFound(path.to_owned()))?;
    let config: Config = toml::from_str(&content)?;
    Ok(config)
}
```

BANNED: `unwrap()/expect()` in library code (ok in tests)
BANNED: `panic!()` for recoverable errors
BANNED: `Box<dyn Error>` (use concrete error types)
