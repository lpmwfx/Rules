---
tags: [modules, imports, encapsulation]
concepts: [module-structure, re-export, encapsulation]
requires: [global/module-tree.md, global/topology.md]
feeds: [python/structure.md]
keywords: [init-py, relative-import, circular-import, star-import]
layer: 3
---
# Modules

> One module per file — `__init__.py` re-exports only, no logic

---

RULE: One module per file — one focused responsibility
RULE: `__init__.py` is a re-export hub — no logic
RULE: Relative imports within package, absolute imports across packages
RULE: Private by default — prefix `_` for internal functions

```python
# mypackage/__init__.py — re-export hub only
from .core import process_data
from .models import UserModel

# mypackage/core.py — internal relative import
from .models import UserModel
from .helpers import _validate    # private helper

# cross-package — absolute import
from other_package.api import fetch
```

BANNED: Circular imports
BANNED: Star imports (`from module import *`)
BANNED: Logic in `__init__.py`
