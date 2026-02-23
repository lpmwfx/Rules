# Dependencies and Linting

> Python 3.11+, minimal deps, strict linting

---

RULE: Python >=3.11 required
RULE: Minimal dependencies, established libraries
PREFER: httpx over requests
PREFER: ruff over black+isort+flake8
PREFER: pydantic for validation
PREFER: beartype for runtime type checking

## Linting Config (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
```
