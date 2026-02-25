---
tags: [python, ack-pattern, result-type, return-format]
concepts: [result-types, return-format, error-handling]
requires: [python/types.md]
related: [rust/errors.md, cpp/errors.md, kotlin/result-pattern.md]
keywords: [success, data, error, ack]
layer: 3
---
# ACK Pattern

> Consistent return format for all functions

---

FORMAT: `{"success": True, "data": result}`
FORMAT: `{"success": False, "error": "message"}`
RULE: ALL functions returning results use ACK format
RULE: Check `ack["success"]` before using data
