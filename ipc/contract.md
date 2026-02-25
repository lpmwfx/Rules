---
tags: [ipc, contract, json-rpc, protocol]
concepts: [protocol, json-rpc, contract]
related: [global/validation.md]
keywords: [json-rpc, schema, versioning]
layer: 5
---
# IPC Contract — Unix Socket + JSON-RPC 2.0

> Shared by all service layers (Python, Node.js, Rust)

---

## Transport

- **Default:** Unix domain socket
- **Alternative:** TCP socket (loopback or LAN)
- **Encoding:** UTF-8 JSON
- **Framing:** One JSON object per line (newline-delimited JSON)

RULE: Bind to `127.0.0.1` by default; expose to LAN only when required
RULE: Use firewall rules to restrict inbound connections
RULE: Add authentication if exposed beyond localhost
RULE: Consider TLS or SSH tunneling for remote access

## Protocol

- **JSON-RPC 2.0** for all requests and responses
- **MCP** (optional) is an additional control plane over the same JSON-RPC transport

## Message Shapes

### Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "workspace/open",
  "params": { "path": "/home/user/project" }
}
```

### Response (success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { "success": true, "data": { "workspace_id": "w1" } }
}
```

### Response (failure)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { "success": false, "error": "message" }
}
```

### Error (protocol-level)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32601, "message": "Method not found", "data": {} }
}
```

### Notification (no response)

```json
{
  "jsonrpc": "2.0",
  "method": "telemetry/event",
  "params": { "name": "open", "ts": 1738854000 }
}
```

## Result Contract (ACK Pattern)

RULE: All application-level results must follow ACK pattern
- Success: `{ "success": true, "data": ... }`
- Failure: `{ "success": false, "error": "message" }`

RULE: Do not mix error styles inside `result`; protocol errors go to `error`

## MCP Usage

RULE: MCP endpoints are still JSON-RPC over Unix sockets
RULE: MCP methods must follow the same ACK result pattern

## Framing Notes

RULE: Each JSON-RPC message is a single line
RULE: The receiver must ignore blank lines
RULE: Messages must not contain unescaped newlines
