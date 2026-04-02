# ant-client Overview

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

`ant-client` is the direct Rust and CLI path to the Autonomi network. The repo currently contains `ant-core`, a headless Rust library, and `ant-cli`, the `ant` binary built on top of it.

## When to use ant-client

Use `ant-client` when you want:

- a Rust-native client without the `antd` daemon
- direct CLI access for file, chunk, wallet, or node-management workflows
- direct control over bootstrap peers, devnet manifests, and EVM network selection

For most multi-language application work, `ant-sdk` remains the easier starting point.

## Current components

| Component | What it does |
|------|------|
| `ant-core` | Direct network library for data operations, payments, local devnet helpers, and node management |
| `ant-cli` | `ant` binary for file, chunk, wallet, and node commands |

## Current CLI shape

The current merged CLI has these top-level groups:

- `ant file`
- `ant chunk`
- `ant wallet`
- `ant node`

It also accepts global flags such as:

- `--json`
- `--bootstrap`
- `--devnet-manifest`
- `--allow-loopback`
- `--timeout-secs`
- `--chunk-concurrency`
- `--log-level`
- `--evm-network`

## Installation

The current README documents install scripts for Linux, macOS, and Windows, plus source builds from the repo.

```bash
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/ant-client/main/install.sh | bash
```

## Relationship to ant-sdk

`ant-client` and `ant-sdk` reach the same network, but they have different shapes:

| | ant-sdk | ant-client |
|---|---|---|
| Interface model | daemon + SDK bindings | direct CLI + Rust library |
| Language coverage | multi-language | Rust and CLI |
| Local process model | requires `antd` | no daemon for data commands |
| Main entry point | REST/gRPC via `antd` | direct P2P connection |

## Related pages

- [Using ant-client](../getting-started/using-ant-client.md)
- [Command Reference](command-reference.md)
- [ant-core Rust Library](ant-core-library.md)
