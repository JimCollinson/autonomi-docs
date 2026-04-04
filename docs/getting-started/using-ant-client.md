# Use the ant CLI

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->

Use the `ant` CLI when you want direct command-line access to the Autonomi network without running `antd`. This path is a good fit for shell workflows, scripts, operational tasks, and developers who want to upload, download, or inspect data directly from the terminal.

## Prerequisites

- A local devnet manifest or bootstrap peer information for the network you want to use
- `SECRET_KEY` set for uploads and wallet commands
- A file to upload for the quickstart example below

If you want to build an application in another language, start with [Build with the SDKs](install.md). If you want daemon-free programmatic Rust access, see [Build in Rust with ant-core](build-directly-in-rust.md).

## Steps

For the `ant` CLI, root flags such as `--devnet-manifest`, `--allow-loopback`, and `--evm-network` come before the subcommand.

### 1. Install the CLI

On Linux or macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/ant-client/main/install.sh | bash
```

Or build from source:

```bash
git clone https://github.com/WithAutonomi/ant-client.git
cd ant-client
cargo build --release --bin ant
```

### 2. Confirm the CLI works

```bash
ant --help
SECRET_KEY=0x... ant --evm-network arbitrum-one wallet address
```

### 3. Upload a public file on a local devnet

```bash
SECRET_KEY=0x... ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file upload photo.jpg --public
```

Expected output shape:

```text
ADDRESS=<hex_address>
MODE=public
CHUNKS=<chunk_count>
TOTAL_SIZE=<bytes>
```

### 4. Download it back

```bash
ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file download <hex_address> -o photo_copy.jpg
```

### 5. Try a low-level chunk operation

```bash
echo "hello autonomi" | SECRET_KEY=0x... ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  chunk put
```

## What happened

`ant` connected directly to the network instead of talking through a local daemon. File commands handled self-encryption, payment, and DataMap management for you, while the chunk command stored a single low-level payload without file splitting.

## Next steps

- [CLI Overview](../cli-reference/overview.md)
- [CLI Command Reference](../cli-reference/command-reference.md)
- [Developing in Rust](../rust-reference/overview.md)
- [Build in Rust with ant-core](build-directly-in-rust.md)
