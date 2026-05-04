# Use MCP with AI Tools

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Use MCP when you want an AI tool such as Claude Desktop, Claude Code, or another MCP-compatible client to store and retrieve data on Autonomi through structured tools instead of direct HTTP requests. This setup still uses `antd` under the hood, but the MCP server handles the bridge between your AI client and the daemon.

## Prerequisites

- Python 3.10+
- An MCP-compatible client such as Claude Desktop or Claude Code
- `antd` built and running on your machine (see [Start the Local Daemon](../sdk/start-the-local-daemon.md))

## Steps

### 1. Start the local daemon

The MCP server talks to `antd`, so start there first:

```bash
./target/release/antd
```

Run that command from the `ant-sdk/antd` build directory, or use `antd` if the binary is already on your `PATH`.

If you have not built `antd` yet, follow [Build with the SDKs](../sdk/install.md) and [Start the Local Daemon](../sdk/start-the-local-daemon.md) first.

### 2. Install the MCP server

From the `ant-sdk` repo root:

```bash
pip install "antd[rest]"
pip install -e antd-mcp/
```

### 3. Configure your AI client

For Claude Desktop, add `antd-mcp` to `claude_desktop_config.json`:

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

### 4. Continue with the full MCP setup

Use the full setup guide next. It covers daemon discovery, SSE mode, and overrides such as `ANTD_BASE_URL`.

## What happened

Your AI client talks to `antd-mcp`, and the MCP server calls `antd` on your behalf.

## Next steps

- [Use the Autonomi MCP Server](../mcp/use-the-autonomi-mcp-server.md)
- [MCP Server Reference](mcp-server-reference.md)
- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
