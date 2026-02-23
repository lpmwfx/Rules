# ACK Pattern

> Consistent return format for all functions

---

FORMAT: `{"success": True, "data": result}`
FORMAT: `{"success": False, "error": "message"}`
RULE: ALL functions returning results use ACK format
RULE: Check `ack["success"]` before using data
