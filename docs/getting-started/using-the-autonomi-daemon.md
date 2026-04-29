# Using the Autonomi Daemon

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 71f9e0fbdc6189e8fa0dc12887339ac52769b1ee
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->

`antd` is the local daemon used by the SDKs and MCP server. It runs on your machine, talks to the network for you, and exposes REST and gRPC so your applications can work through a stable local API.

Use `antd` when you want:

- SDKs in multiple languages
- a local REST or gRPC gateway
- one daemon process shared by applications, scripts, or tools

## Prerequisites

- Git
- Rust toolchain
- `protoc` (Protocol Buffers compiler) available on your machine
- For write operations on the default network: a wallet private key exported as `AUTONOMI_WALLET_KEY`
- For a fully local devnet: Python 3.10+ and a sibling `ant-node` checkout if you plan to use `ant dev start`

## Steps

### 1. Build the daemon from source

The current install path for `antd` is to build it from the `ant-sdk` repo:

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

### 2. Start the daemon

For a read-only local gateway on the default network:

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

On the first run, `ant dev start` can take longer than usual while local components compile in release mode. If it times out on a cold build, run it again after the initial compilation has completed.

### 3. Confirm the gateway responds

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

If you started a local devnet, the `network` value is `local`.

### 4. Know what the daemon gives you

By default, `antd` provides:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

On startup, `antd` also writes a `daemon.port` file. SDKs can use that file to discover non-default ports automatically.

## What happened

You built `antd` and started a local gateway for the Autonomi SDKs. The health check confirms that the daemon is reachable; write endpoints stay unavailable until the daemon has wallet configuration or a local devnet helper has provisioned one.

## Next steps

- [Your First Upload with the SDKs](hello-world.md)
- [SDK Overview](../sdk-reference/overview.md)
- [REST API](../sdk-reference/rest-api.md)
- [Use the ant CLI](using-ant-client.md)
