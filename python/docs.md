---
tags: [python, docs, docstrings, google-style]
concepts: [documentation, api-surface, discoverability]
requires: [python/types.md]
feeds: [python/testing.md]
related: [rust/docs.md, cpp/docs.md, js/jsdoc.md, kotlin/docs.md, csharp/docs.md]
keywords: [google-style, docstring, Args, Returns, Raises, module-docstring]
layer: 4
---
# Documentation

> Google-style docstrings on all public API — Args, Returns, Raises

---

RULE: Google-style docstrings on all public functions and classes
RULE: Args, Returns, Raises sections required
RULE: Module docstring on every module file

```python
def parse_config(path: str, *, strict: bool = False) -> AppConfig:
    """Parse configuration file and return validated config.

    Args:
        path: Absolute path to the TOML config file.
        strict: If True, unknown keys raise an error.

    Returns:
        Validated AppConfig instance.

    Raises:
        FileNotFoundError: Config file does not exist.
        ValidationError: Config contains invalid values.
    """
```

BANNED: Undocumented public API
BANNED: Docstrings that just repeat the function name
