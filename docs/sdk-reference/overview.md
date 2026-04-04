# SDK Overview

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

The Autonomi SDKs center on `antd`, a local gateway daemon that exposes REST and gRPC APIs, plus language SDKs and local developer tooling around that daemon.

## Architecture

```text
Your application
    |
    |  cURL / SDK / gRPC client
    v
+-----------------------------+
|            antd             |
|   REST :8082   gRPC :50051  |
+-----------------------------+
              |
              v
           ant-core
              |
              v
       Autonomi Network
```

The repo includes these developer-facing pieces:

| Component | What it does |
|------|------|
| `antd/` | Runs the local REST and gRPC gateway daemon |
| `antd-js/`, `antd-py/`, `antd-go/`, `antd-rust/`, and other language directories | Provide language-specific clients for the daemon |
| `ant-dev/` | Starts a local development environment and example flows |
| `antd-mcp/` | Exposes the daemon surface to MCP-compatible AI tools |

## Connection model

The daemon defaults are:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

On startup, `antd` writes a `daemon.port` file with the resolved REST and gRPC ports. The default locations are:

| Platform | `daemon.port` location |
|------|------|
| Windows | `%APPDATA%\ant\daemon.port` |
| Linux | `~/.local/share/ant/daemon.port` or `$XDG_DATA_HOME/ant/daemon.port` |
| macOS | `~/Library/Application Support/ant/daemon.port` |

Current SDKs can use that file to discover non-default ports instead of hardcoding `8082`.

## Current shared surfaces

The `antd` REST surface groups into these areas:

| Group | Current routes |
|------|------|
| Health | `/health` |
| Data | `/v1/data/public`, `/v1/data/private`, `/v1/data/cost` |
| Chunks | `/v1/chunks` |
| Files and directories | `/v1/files/upload/public`, `/v1/files/download/public`, `/v1/dirs/upload/public`, `/v1/dirs/download/public`, `/v1/cost/file` |
| Wallet | `/v1/wallet/address`, `/v1/wallet/balance`, `/v1/wallet/approve` |
| External signer flow | `/v1/data/prepare`, `/v1/upload/prepare`, `/v1/upload/finalize` |

The proto directory contains `health.proto`, `data.proto`, `chunks.proto`, `files.proto`, and `events.proto`.

## Language SDKs

The repo contains language SDK directories for Go, JavaScript/TypeScript, Python, C#, Kotlin, Swift, Ruby, PHP, Dart, Lua, Elixir, Zig, Rust, C++, and Java.

Do not assume perfect parity from this page alone. The SDKs expose the same daemon surface with language-specific constructors and, in some cases, transport differences. For example:

- JavaScript examples use `createClient()` from `antd`
- Python examples use `AntdClient()` from `antd`
- some SDK READMEs document both REST and gRPC, while others are REST-only today

At this commit, the daemon and some SDK response models are not perfectly aligned for upload cost fields. For data uploads, rely on the returned address and successful retrieval first; if you need authoritative cost information, use the explicit cost endpoints.

Use the binding-specific page when you need package names, constructors, or transport details.

## Upstream sources

- [ant-sdk](https://github.com/WithAutonomi/ant-sdk)

## Related pages

- [Build with the SDKs](../getting-started/install.md)
- [Your First Upload with the SDKs](../getting-started/hello-world.md)
- [Use the Autonomi MCP Server](../how-to-guides/use-the-mcp-server.md)
- [MCP Server Reference](mcp-server.md)
- [REST API](rest-api.md)
