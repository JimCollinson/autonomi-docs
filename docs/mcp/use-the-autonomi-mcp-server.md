# How to Use the MCP Server

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

Use this guide when you want to install and configure the Autonomi MCP server against a running `antd` instance. It is the deeper setup guide for AI clients that talk to Autonomi through MCP tools instead of raw HTTP requests.

## Prerequisites

- `antd` running on your machine or reachable at a known base URL (see [Start the Local Daemon](../sdk/start-the-local-daemon.md))
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

- [Use MCP with AI Tools](../mcp/use-mcp-with-ai-tools.md)
- [MCP Server Reference](mcp-server-reference.md)
- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
- [REST API](../sdk/reference/rest-api.md)
