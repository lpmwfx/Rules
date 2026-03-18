---
tags: [constants, configuration, magic-numbers]
concepts: [named-constants, configuration, immutability]
requires: [global/config-driven.md]
feeds: [python/types.md]
keywords: [upper-case, dataclass, cfg, magic-number, hardcoded]
layer: 3
---
# Constants

> Named constants everywhere — no magic values in function bodies

---

RULE: All configurable values in `_cfg` dataclasses or constants module
RULE: `UPPER_CASE` for module-level constants
RULE: No magic numbers in function bodies — use named constants

```python
# config.py
from dataclasses import dataclass

MAX_RETRIES = 3
DEFAULT_TIMEOUT_S = 30
API_BASE_URL = "https://api.example.com/v2"

@dataclass(frozen=True)
class DbConfig_cfg:
    host: str = "localhost"
    port: int = 5432
    pool_size: int = 10
```

BANNED: Hardcoded paths, URLs, ports, timeouts in function bodies
BANNED: Magic numbers without explanation
