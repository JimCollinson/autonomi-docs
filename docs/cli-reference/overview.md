# CLI Overview

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: d46a73d38731a31fbd9815394fe8a2943eb38246
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

`ant` is the command-line interface for Autonomi. It gives you direct shell access to file, chunk, wallet, self-update, and node-management workflows without running `antd`.

## When to use the CLI

Use the CLI when you want:

- direct shell access for file, chunk, wallet, or node-management workflows
- shell-first automation or operational workflows
- direct control over network entry, local devnet manifests, and EVM network selection

If you want SDK ergonomics in another language, use the SDK route instead. If you want daemon-free programmatic Rust access, see [Developing in Rust](../rust-reference/overview.md).

## Network entry

The CLI needs a bootstrap source for data operations.

- On Linux, the installer writes `bootstrap_peers.toml` to `${XDG_CONFIG_HOME:-~/.config}/ant/bootstrap_peers.toml`.
- On macOS, the installer writes `bootstrap_peers.toml` to `~/Library/Application Support/ant/bootstrap_peers.toml`.
- On Windows, the installer writes `bootstrap_peers.toml` to `%APPDATA%\ant\bootstrap_peers.toml`.
- If you build `ant` from source instead of using the installer, provide your own bootstrap config or pass `--bootstrap` yourself.
- Use `--bootstrap` when you want to override the installed peer list or when the config file is missing.
- Use `--devnet-manifest` with `--allow-loopback` when you are connecting to a local devnet.

Reads do not need `SECRET_KEY`. Uploads and wallet commands do.

## Command groups

The CLI has these top-level groups:

- `ant file` for multi-chunk file upload and download
- `ant chunk` for low-level single-chunk put and get operations
- `ant wallet` for the address and token balance derived from `SECRET_KEY`
- `ant node` for node registry, lifecycle, and daemon management
- `ant update` for self-updating the installed CLI

For the complete tree and per-command flags, see the [CLI Command Reference](command-reference.md).

## Installation

Install scripts are available for Linux, macOS, and Windows, and you can also build the CLI from source.

{% tabs %}
{% tab title="Linux and macOS" %}
```bash
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/ant-client/main/install.sh | bash
```
{% endtab %}
{% tab title="Windows" %}
```powershell
irm https://raw.githubusercontent.com/WithAutonomi/ant-client/main/install.ps1 | iex
```
{% endtab %}
{% tab title="Build from source" %}
```bash
git clone https://github.com/WithAutonomi/ant-client.git
cd ant-client
cargo build --release --bin ant
```
{% endtab %}
{% endtabs %}

## Relationship to the other paths

The CLI, SDK, and native Rust paths reach the same network, but they have different shapes:

|                     | SDKs                              | CLI                            | Native Rust                  |
| ------------------- | --------------------------------- | ------------------------------ | ---------------------------- |
| Interface model     | daemon + SDK bindings             | direct CLI                     | direct Rust library          |
| Best for            | app development in many languages | shell workflows and operations | daemon-free Rust development |
| Local process model | requires `antd`                   | no daemon for data commands    | no daemon                    |
| Main entry point    | REST/gRPC via `antd`              | `ant` command                  | `ant-core` crate             |

## Upstream sources

- [ant-client](https://github.com/WithAutonomi/ant-client)

## Related pages

- [Use the CLI](../getting-started/using-ant-client.md)
- [CLI Command Reference](command-reference.md)
- [Developing in Rust](../rust-reference/overview.md)
