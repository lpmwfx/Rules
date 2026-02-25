---
tags: [rust, verification, clippy, testing]
concepts: [testing, clippy]
requires: [rust/types.md]
related: [python/testing.md, cpp/testing.md]
keywords: [clippy, cargo-test, miri]
layer: 4
---
# Verification Stack

> Gating levels — local, merge, release

---

## Install Once

```bash
rustup component add rustfmt clippy miri
cargo install cargo-deny cargo-audit cargo-nextest cargo-llvm-cov cargo-machete typos-cli
```

## Level 0 — Local Build Gate

- `cargo fmt --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test` / `cargo nextest run`

## Level 1 — Merge Gate

- `cargo deny check`
- `cargo audit`
- `cargo machete`
- `typos`

## Level 2 — Release Gate

- `cargo miri test`
- Sanitizers (ASAN/TSAN where relevant)
- `cargo llvm-cov`

## Definitions

- **Green build**: Level 0 passed
- **Green merge**: Level 0 + 1 passed
- **Green release**: Level 0 + 1 + 2 passed
