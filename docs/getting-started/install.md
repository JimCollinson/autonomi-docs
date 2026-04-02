# Install antd

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This page gets the `antd` daemon built locally and confirms its REST API is reachable. By the end, you will have the current merged daemon running and know what is required for read-only versus write operations.

## Prerequisites

- Git
- Rust toolchain
- For write operations on the default network: a wallet private key exported as `AUTONOMI_WALLET_KEY`
- For a fully local devnet: Python 3.10+ and a sibling `ant-node` checkout if you plan to use `ant dev start`

## Steps

### 1. Build the daemon from source

`antd` currently lives in the `ant-sdk` repo. Build it from source:

```bash
git clone https://github.com/WithAutonomi/ant-sdk.git
cd ant-sdk/antd
cargo build --release
```

Verify the binary starts:

```bash
./target/release/antd --help
```

### 2. Start the daemon

For a read-only daemon on the default network:

```bash
./target/release/antd
```

To enable write endpoints on the default network, restart it with a wallet key:

```bash
AUTONOMI_WALLET_KEY="<hex_private_key>" ./target/release/antd
```

If you want a local devnet instead, use the helper from the repo root:

```bash
cd ..
pip install -e ant-dev/
ant dev start
```

`ant dev start` expects the `ant-node` repo to be cloned as a sibling of `ant-sdk`.

### 3. Confirm the daemon responds

The current default REST endpoint is `http://localhost:8082`:

```bash
curl http://localhost:8082/health
```

Expected response:

```json
{
  "status": "ok",
  "network": "default"
}
```

If you started a local devnet, the `network` value is `local`.

### 4. Note the connection defaults

The current merged daemon defaults are:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

On startup, `antd` also writes a `daemon.port` file. SDKs can use that file to discover non-default ports automatically.

## What happened

You built the current merged `antd` daemon from the `ant-sdk` repo and started its local REST/gRPC gateway. The health check confirms the daemon is reachable; write endpoints stay unavailable until the daemon has wallet configuration or a local devnet helper has provisioned one.

## Next steps

- [Your First Upload](hello-world.md)
- [ant-sdk Overview](../sdk-reference/overview.md)
- [REST API](../sdk-reference/rest-api.md)
