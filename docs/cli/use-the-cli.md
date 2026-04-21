# Using the Autonomi CLI

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: d46a73d38731a31fbd9815394fe8a2943eb38246
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

Install `ant`, confirm it works, retrieve public data from the network, and then move into uploads or local devnet testing when you need them. Choose the CLI when you want shell-first workflows without needing to run the local daemon, [`antd`](../sdk/start-the-local-daemon.md), first.

The CLI can be a good fit when you want:

- direct shell access to file, chunk, wallet, or node-management workflows
- shell-first automation or operational workflows
- direct control over bootstrap peers, local devnet manifests, and EVM network selection

## Prerequisites

- `curl` or PowerShell to run the installer, or a Rust toolchain if you prefer to build from source
- `SECRET_KEY` for the upload step and for wallet commands. You do not need it for the first download step.
- A local file to upload later in the guide, unless you use the sample `greeting.txt` command in the upload step.

If you want SDK ergonomics in another language, see [Build with the SDKs](../sdk/install.md) and [Start the Local Daemon](../sdk/start-the-local-daemon.md). If you want daemon-free programmatic Rust access, see [Build Directly in Rust](../rust/build-directly-in-rust.md).

## Steps

{% stepper %}
{% step %}
### Install the CLI

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

The installer also writes `bootstrap_peers.toml` into the standard `ant` config directory, so public-network reads usually work without extra `--bootstrap` flags.

If you build `ant` from source instead, provide your own bootstrap config or pass `--bootstrap` yourself for data commands.
{% endstep %}
{% step %}
### Confirm the CLI works

```bash
ant --help
```

For the `ant` CLI, root flags such as `--bootstrap`, `--devnet-manifest`, `--allow-loopback`, and `--evm-network` come before the subcommand.

The CLI needs a bootstrap source for data operations. The installer usually provides one through `bootstrap_peers.toml`. Use `--bootstrap` to override it, or use `--devnet-manifest` together with `--allow-loopback` for a local devnet.
{% endstep %}
{% step %}
### Retrieve a public file from the network

This example downloads a public JPEG of Lucky the dog.

```bash
ant file download 711c7e20006ff3e0ac6c1f3063286a0c1a3e4c409642e8c526173fa60bb7078a -o lucky.jpg
```

`-o lucky.jpg` chooses the local filename for the downloaded copy. The address identifies the content on the network, not the original filename.
{% endstep %}
{% step %}
### Store a file on the default network

Set `SECRET_KEY`, create a small local file, and then upload it on the default network.

```bash
printf "hello autonomi\n" > greeting.txt
export SECRET_KEY="0x<hex_private_key>"
ant file upload greeting.txt --public
```

Expected output includes a public address you can share with other readers, plus the stored chunk count, file size, and total cost.
{% endstep %}
{% step %}
### Optional: Use a local devnet for isolated testing

If you already have a devnet manifest, pass it before the subcommand:

```bash
SECRET_KEY="0x<hex_private_key>" ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file upload lucky.jpg --public
```

Use this mode when you want local nodes and a local EVM chain instead of the public network. For the full setup, see [Set Up a Local Network](../guides/set-up-a-local-network.md).
{% endstep %}
{% endstepper %}

## What happened

You installed `ant`, used the configured bootstrap source to reach the Autonomi Network, and downloaded public content directly from the terminal. When you added `SECRET_KEY`, the same CLI handled self-encryption, upload payment, and DataMap management for file writes.

## Next steps

- [CLI Command Reference](command-reference.md)
- [Set Up a Local Network](../guides/set-up-a-local-network.md)
- [Build Directly in Rust](../rust/build-directly-in-rust.md)
