# CLI Overview

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->

`ant` is the command-line interface for Autonomi. It gives you direct shell access to uploads, downloads, wallet inspection, self-update, chunk operations, and node-management workflows without running the SDK daemon.

## When to use the CLI

Use the CLI when you want:

- direct CLI access for file, chunk, wallet, or node-management workflows
- direct control over bootstrap peers, devnet manifests, and EVM network selection
- shell-first automation or operational workflows

If you want SDK ergonomics in other languages, use the SDKs instead. If you want daemon-free programmatic Rust access, see [Developing in Rust](../rust-reference/overview.md).

## CLI shape

The CLI has these top-level groups:

- `ant file`
- `ant chunk`
- `ant wallet`
- `ant node`
- `ant update`

It also accepts global flags such as:

- `--json`
- `-V`, `--version`
- `--bootstrap`
- `--devnet-manifest`
- `--allow-loopback`
- `--timeout-secs`
- `--chunk-concurrency`
- `--log-level`
- `--evm-network`

## Installation

Install scripts are available for Linux, macOS, and Windows, and you can also build the CLI from source.

```bash
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/ant-client/main/install.sh | bash
```

## Relationship to the other paths

The CLI, SDK, and native Rust paths reach the same network, but they have different shapes:

| | SDKs | CLI | Native Rust |
|---|---|---|---|
| Interface model | daemon + SDK bindings | direct CLI | direct Rust library |
| Best for | app development in many languages | shell workflows and operations | daemon-free Rust development |
| Local process model | requires `antd` | no daemon for data commands | no daemon |
| Main entry point | REST/gRPC via `antd` | `ant` command | `ant-core` crate |

## Upstream sources

- [ant-client](https://github.com/WithAutonomi/ant-client)

## Related pages

- [Use the ant CLI](../getting-started/using-ant-client.md)
- [CLI Command Reference](command-reference.md)
- [Developing in Rust](../rust-reference/overview.md)
