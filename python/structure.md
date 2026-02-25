---
tags: [python, structure, modules, flat]
concepts: [file-organization, architecture]
requires: [global/consistency.md]
related: [js/modules.md, rust/modules.md]
keywords: [flat-structure, init-py, max-lines]
layer: 3
---
# File and Module Structure

> pyproject.toml for config, micro-service architecture

---

RULE: `pyproject.toml` for all config (no setup.py, no requirements.txt)
RULE: Micro-service architecture — each service has own pyproject.toml
RULE: Module docstring first — explains what module does
RULE: Private helpers (`_func`) defined before public functions
RULE: Max 20 lines per function body
RULE: Max 200-350 lines per file — split by function/responsibility if larger

## Project Structure

```
service_name/
service_name/__init__.py      # version + brief docstring
service_name/__main__.py      # entry point
service_name/core.py          # main logic
service_name/db.py            # database layer
tests/
tests/conftest.py             # fixtures
tests/test_*.py               # test files
pyproject.toml                # unified config
```
