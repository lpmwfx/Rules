---
tags: [ack-pattern, result-type, return-format]
concepts: [result-types, return-format, error-handling]
requires: [python/types.md]
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


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
