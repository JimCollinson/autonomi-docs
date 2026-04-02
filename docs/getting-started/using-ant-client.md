# Using ant-client (Rust / CLI)

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Use `ant-client` when you want direct Rust or CLI access to the Autonomi network without running `antd`.

## Prerequisites

- A local devnet manifest or bootstrap peer information for the network you want to use
- `SECRET_KEY` set for uploads and wallet commands
- A file to upload for the quickstart example below

## Steps

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
SECRET_KEY=0x... ant wallet address --evm-network arbitrum-one
```

### 3. Upload a public file on a local devnet

```bash
SECRET_KEY=0x... ant file upload photo.jpg --public \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local
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
ant file download <hex_address> -o photo_copy.jpg \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local
```

### 5. Try a low-level chunk operation

```bash
echo "hello autonomi" | SECRET_KEY=0x... ant chunk put \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local
```

## What happened

`ant` connected directly to the network instead of talking through a local daemon. File commands handled self-encryption, payment, and DataMap management, while the chunk command stored a single low-level payload without file splitting.

## Next steps

- [ant-client Overview](../cli-reference/overview.md)
- [Command Reference](../cli-reference/command-reference.md)
- [ant-core Rust Library](../cli-reference/ant-core-library.md)
