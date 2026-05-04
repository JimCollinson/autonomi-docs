# How to Use the MCP Server

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
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

### 2. Prefer an explicit daemon URL

The server still attempts `daemon.port` discovery before falling back to the default REST URL.

`antd` writes `ant/sdk/daemon.port`, while `antd-mcp` reads `ant/daemon.port`. Treat `ANTD_BASE_URL` as the reliable setup path unless you have already confirmed port-file discovery works in your environment.

If no environment variable or readable port file is available, it falls back to:

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

### 4. Set the daemon URL explicitly

Set `ANTD_BASE_URL` explicitly for a reliable connection:

```bash
ANTD_BASE_URL="http://your-host:8082" antd-mcp
```

### 5. Configure Claude Desktop

Add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "antd-autonomi": {
      "command": "antd-mcp",
      "env": {
        "ANTD_BASE_URL": "http://127.0.0.1:8082"
      }
    }
  }
}
```

Adjust `ANTD_BASE_URL` if your daemon runs on a different host or port.

## Verify it worked

Your MCP client is configured correctly when it can see the `antd-autonomi` server and call a basic tool such as `check_health()` successfully.

## Common errors

**The server cannot find the daemon**: Confirm that `antd` is running, then set `ANTD_BASE_URL` explicitly.

**Import or package errors**: Make sure both `antd[rest]` and `antd-mcp` were installed into the same Python environment.

**Tool calls fail immediately**: Check the daemon first with `curl http://localhost:8082/health`.

## Next steps

- [Use MCP with AI Tools](../mcp/use-mcp-with-ai-tools.md)
- [MCP Server Reference](mcp-server-reference.md)
- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
- [REST API](../sdk/reference/rest-api.md)
