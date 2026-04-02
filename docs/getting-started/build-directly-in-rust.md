# Build Directly in Rust

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Use this path when you want native, daemon-free Rust access to the Autonomi network through `ant-core`. It is the most direct programmatic route for applications that want to control networking, uploads, and payments in Rust.

## Prerequisites

- Rust toolchain
- A local checkout of `ant-client`
- A new or existing Rust application

If you want a local REST or gRPC gateway instead, start with [Build with the SDKs](install.md). If you want shell access instead of writing Rust code, see [Use the ant CLI](using-ant-client.md).

## Steps

### 1. Create a Rust app and add `ant-core`

```bash
git clone https://github.com/WithAutonomi/ant-client.git
cargo new autonomi-rust-app
cd autonomi-rust-app
```

Update `Cargo.toml`:

```toml
[dependencies]
ant-core = { path = "../ant-client/ant-core" }
bytes = "1"
tokio = { version = "1", features = ["full"] }
```

### 2. Start a local devnet and upload data directly from Rust

Replace `src/main.rs` with:

```rust
use ant_core::data::LocalDevnet;
use bytes::Bytes;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut devnet = LocalDevnet::start_minimal().await?;
    let client = devnet.create_funded_client().await?;

    let original = Bytes::from("Hello from Rust!");
    let result = client.data_upload(original.clone()).await?;
    let downloaded = client.data_download(&result.data_map).await?;

    assert_eq!(downloaded, original);
    println!("Stored {} chunks", result.chunks_stored);

    devnet.shutdown().await?;
    Ok(())
}
```

### 3. Run the app

```bash
cargo run
```

This example starts a local Autonomi development network, creates a funded Rust client, uploads a payload, downloads it again, and shuts the devnet down.

## What happened

Your Rust application talked to the network through `ant-core` directly, without `antd` or a CLI wrapper. `ant-core` started a local devnet, created a funded client, handled self-encryption and payment, and gave you direct access to the upload and download results in Rust.

## Next steps

- [ant-core Rust Library](../cli-reference/ant-core-library.md)
- [Use the ant CLI](using-ant-client.md)
- [Payment Model](../core-concepts/payment-model.md)
