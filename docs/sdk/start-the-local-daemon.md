# Start the Local Daemon

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: d3f5ba969b8ccf98ca0c50b661a3762aec904634
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

When you build on the Autonomi Network through the SDKs or MCP server, you use a local daemon called `antd`. It runs on your machine and gives your application a stable REST and gRPC interface to the network. This page shows you how to build it from source, start it in read-only mode, and then choose whether you need uploads or a local devnet.

Use `antd` when you want:

- SDKs in multiple languages
- a local REST or gRPC gateway
- one daemon process shared by applications, scripts, or tools

## Prerequisites

- Rust toolchain and `protoc` (Protocol Buffers compiler) to build `antd` from source
- For paid uploads on the default network: access to wallet and payment configuration. See [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md) and [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md).
- For a fully local devnet: Python 3.10+ and a sibling `ant-node` checkout if you plan to use `ant dev start`. See [Set Up a Local Network](../guides/set-up-a-local-network.md).

## Steps

### 1. Build `antd` from source

Your application code does not need to be Rust, but the supported `antd` install method in these docs is to build the daemon from the `ant-sdk` repo:

```bash
git clone https://github.com/WithAutonomi/ant-sdk.git
cd ant-sdk/antd
cargo build --release
```

`antd` currently needs `protoc` during the build. On macOS, one working setup is:

```bash
brew install protobuf
```

Verify the binary starts:

```bash
./target/release/antd --help
```

### 2. Start `antd` in read-only mode

Start with the simplest mode first:

```bash
./target/release/antd
```

This gives you a local REST and gRPC gateway for health checks, reads, and SDK connectivity without upload payment setup.

### 3. Confirm the daemon is healthy

The default REST endpoint is `http://localhost:8082`:

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

On startup, `antd` also writes a `daemon.port` file. SDKs can use that file to discover non-default ports automatically.

If you only need retrieval, continue to [Retrieve Data from the Network](retrieve-data-from-the-network.md) before you think about upload payment setup.

### 4. Enable uploads when you need them

Skip this step if you are only building read-only features.

To enable the regular write endpoints on the default network, restart `antd` with wallet and EVM settings:

```bash
AUTONOMI_WALLET_KEY="<hex_private_key>" \
EVM_RPC_URL="https://your-rpc-endpoint" \
EVM_PAYMENT_TOKEN_ADDRESS="0x..." \
EVM_PAYMENT_VAULT_ADDRESS="0x..." \
./target/release/antd
```

Use this mode for SDK calls and REST endpoints that upload data directly, such as `data_put_public` or `POST /v1/data/public`.

If your application should keep the signing key outside `antd`, omit `AUTONOMI_WALLET_KEY` and keep the EVM settings instead:

```bash
EVM_RPC_URL="https://your-rpc-endpoint" \
EVM_PAYMENT_TOKEN_ADDRESS="0x..." \
EVM_PAYMENT_VAULT_ADDRESS="0x..." \
./target/release/antd
```

This mode is for the two-phase prepare and finalize upload flow described in [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md).

### 5. Start a local devnet when you need a full local stack

If you want local services and test funds provisioned for you, use the helper from the repo root:

```bash
cd ..
pip install -e ant-dev/
ant dev start
```

`ant dev start` expects the `ant-node` repo to be cloned as a sibling of `ant-sdk`.

It starts a local Autonomi stack and provisions the payment configuration that `antd` needs for uploads on the local network.

On the first run, `ant dev start` can take longer than usual while local components compile in release mode. If it times out on a cold build, run it again after the initial compilation has completed.

## What happened

You built `antd` and started a local gateway for the Autonomi SDKs. The health check confirms that the daemon is reachable; you can keep it read-only, restart it with wallet-backed upload settings, or let a local devnet provision the upload configuration for you.

## Next steps

- [Retrieve Data from the Network](retrieve-data-from-the-network.md)
- [Store Data on the Network](store-data-on-the-network.md)
- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md)
- [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md)
- [Set Up a Local Network](../guides/set-up-a-local-network.md)
- [SDK Overview](../sdk/reference/overview.md)
- [REST API](../sdk/reference/rest-api.md)
- [Use the CLI](../cli/use-the-cli.md)
