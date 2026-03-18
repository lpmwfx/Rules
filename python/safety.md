---
tags: [python, safety, security, input-validation]
concepts: [code-injection, subprocess-safety, deserialization]
requires: [python/types.md, global/validation.md]
related: [rust/safety.md, js/safety.md, cpp/safety.md, kotlin/safety.md, csharp/safety.md]
keywords: [eval, exec, subprocess, pickle, shell-injection, sanitize]
layer: 4
---
# Safety & Security

> No eval, no shell=True, no untrusted pickle — sanitize at boundaries

---

RULE: Never use `eval()` or `exec()` — use `ast.literal_eval()` if needed
RULE: `subprocess` with list args, never `shell=True`
RULE: `pickle` only for trusted data — use JSON for untrusted
RULE: Input sanitization at system boundaries

```python
import subprocess, ast, json

# Safe subprocess — list args, no shell
result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True, text=True, check=True,
)

# Safe literal parsing
value = ast.literal_eval("{'key': 42}")   # OK — no code execution

# Safe deserialization of untrusted input
data = json.loads(user_input)             # OK — no arbitrary objects
```

BANNED: `eval()`, `exec()`
BANNED: `subprocess.call(cmd, shell=True)`
BANNED: `pickle.loads()` on untrusted data
BANNED: `os.system()` — use `subprocess.run()`
