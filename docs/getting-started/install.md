# Build with the SDKs

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Use this path when you want to build on Autonomi through language SDKs and a local daemon. `antd` runs on your machine, talks to the network for you, and exposes REST and gRPC so your application can work through a stable local API.

This is usually the best starting point if you are building in Python, JavaScript, TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, or another SDK language.

## Prerequisites

- Git
- Rust toolchain
- For write operations on the default network: a wallet private key exported as `AUTONOMI_WALLET_KEY`
- For a fully local devnet: Python 3.10+ and a sibling `ant-node` checkout if you plan to use `ant dev start`

## Steps

### 1. Build the daemon from source

Install `antd` from the `ant-sdk` repo:

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

### 3. Confirm the gateway responds

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

### 4. Know what this path gives you

By default, `antd` provides:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

On startup, `antd` also writes a `daemon.port` file. SDKs can use that file to discover non-default ports automatically.

This path is useful when you want:

- a single local process that multiple apps or tools can share
- SDK ergonomics in non-Rust languages
- a stable local REST or gRPC interface instead of direct P2P networking in your app

## What happened

You built `antd` and started a local gateway for the Autonomi SDKs. The health check confirms that the daemon is reachable; write endpoints stay unavailable until the daemon has wallet configuration or a local devnet helper has provisioned one.

## Next steps

- [Your First Upload with the SDKs](hello-world.md)
- [ant-sdk Overview](../sdk-reference/overview.md)
- [REST API](../sdk-reference/rest-api.md)
- [Use the ant CLI](using-ant-client.md)
