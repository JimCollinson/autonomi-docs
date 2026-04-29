# Use the Autonomi MCP Server

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 71f9e0fbdc6189e8fa0dc12887339ac52769b1ee
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->

Use the Autonomi MCP server when you want an MCP-compatible client such as Claude Desktop or Claude Code to call the `antd` daemon through structured tools instead of raw HTTP requests.

## Prerequisites

- `antd` running on your machine or reachable at a known base URL (see [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md))
- Python 3.10+
- A local checkout of `ant-sdk`
- `antd` Python SDK installed with REST support

## Steps

### 1. Install the MCP server

From the `ant-sdk` repo root:

```bash
pip install "antd[rest]"
pip install -e antd-mcp/
```

The `antd-mcp` package installs a command named `antd-mcp`.

### 2. Let it discover the daemon automatically

By default, the server looks for the `daemon.port` file written by `antd` on startup. If discovery succeeds, it connects to the REST endpoint listed there.

If no environment variable or port file is available, it falls back to:

```text
http://127.0.0.1:8082
```

### 3. Run the MCP server

For Claude Desktop and other stdio-based clients:

```bash
antd-mcp
```

For web-based clients that want SSE transport:

```bash
antd-mcp --sse
```

### 4. Override the daemon URL when needed

If the daemon is not discoverable through `daemon.port`, set `ANTD_BASE_URL` explicitly:

```bash
ANTD_BASE_URL="http://your-host:8082" antd-mcp
```

### 5. Configure Claude Desktop

Add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "antd-autonomi": {
      "command": "antd-mcp"
    }
  }
}
```

If you need to override discovery, add an `env` block with `ANTD_BASE_URL`.

## Verify it worked

Your MCP client is configured correctly when it can see the `antd-autonomi` server and call a basic tool such as `check_health()` successfully.

## Common errors

**The server cannot find the daemon**: Confirm that `antd` is running and that `daemon.port` exists, or set `ANTD_BASE_URL` explicitly.

**Import or package errors**: Make sure both `antd[rest]` and `antd-mcp` were installed into the same Python environment.

**Tool calls fail immediately**: Check the daemon first with `curl http://localhost:8082/health`.

## Next steps

- [MCP Server Reference](../sdk-reference/mcp-server.md)
- [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md)
- [REST API](../sdk-reference/rest-api.md)
