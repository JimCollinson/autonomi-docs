# ant-core Rust Library

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

`ant-core` is the headless Rust library that powers the `ant` CLI and exposes direct Autonomi network operations without a daemon.

## Install

The current repo README documents `ant-core` as a local dependency from an `ant-client` checkout:

```toml
[dependencies]
ant-core = { path = "../ant-client/ant-core" }
bytes = "1"
tokio = { version = "1", features = ["full"] }
```

## Connect to the network

```rust
use ant_core::data::{Client, ClientConfig};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let _ = client;
    Ok(())
}
```

To enable paid operations, attach a wallet:

```rust
use ant_core::data::{Client, ClientConfig, EvmNetwork, Wallet};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let wallet = Wallet::new_from_private_key(EvmNetwork::ArbitrumOne, "0xprivate_key...")?;
    let client = client.with_wallet(wallet);
    client.approve_token_spend().await?;
    Ok(())
}
```

## Store and retrieve data

```rust
use ant_core::data::{Client, ClientConfig};
use bytes::Bytes;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;

    let result = client.data_upload(Bytes::from("hello autonomi")).await?;
    let content = client.data_download(&result.data_map).await?;

    assert_eq!(content, Bytes::from("hello autonomi"));
    Ok(())
}
```

To make uploaded data publicly retrievable by address, store and later fetch the DataMap:

```rust
let public_address = client.data_map_store(&result.data_map).await?;
let public_data_map = client.data_map_fetch(&public_address).await?;
let downloaded = client.data_download(&public_data_map).await?;
```

## File operations

```rust
use ant_core::data::{Client, ClientConfig, PaymentMode};
use std::path::Path;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;

    let result = client.file_upload_with_mode(Path::new("photo.jpg"), PaymentMode::Merkle).await?;
    let address = client.data_map_store(&result.data_map).await?;
    let data_map = client.data_map_fetch(&address).await?;
    client.file_download(&data_map, Path::new("photo_copy.jpg")).await?;
    Ok(())
}
```

## Key types

| Type | Description |
|------|-------------|
| `ant_core::data::Client` | Main network client |
| `ant_core::data::ClientConfig` | Network timeout and concurrency settings |
| `ant_core::data::PaymentMode` | `Auto`, `Merkle`, or `Single` |
| `ant_core::data::DataMap` | Private retrieval map for uploaded data |
| `ant_core::data::LocalDevnet` | Local development helper |
| `ant_core::data::Wallet` | EVM wallet used for paid operations |

## Error handling

```rust
use ant_core::data::{Client, ClientConfig, Error};
use bytes::Bytes;

#[tokio::main]
async fn main() {
    let client = Client::connect(&["1.2.3.4:12000".parse().unwrap()], ClientConfig::default())
        .await
        .unwrap();

    match client.data_upload(Bytes::from("hello")).await {
        Ok(result) => println!("{}", result.chunks_stored),
        Err(Error::Payment(message)) => println!("{message}"),
        Err(Error::InsufficientPeers(message)) => println!("{message}"),
        Err(error) => println!("{error}"),
    }
}
```

## Local development

The current merged library also exports `LocalDevnet` for local development flows:

```rust
use ant_core::data::LocalDevnet;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut devnet = LocalDevnet::start_minimal().await?;
    let client = devnet.create_funded_client().await?;
    let _ = client;
    devnet.shutdown().await?;
    Ok(())
}
```

## Related pages

- [ant-client Overview](overview.md)
- [Command Reference](command-reference.md)
- [Rust SDK](../sdk-reference/language-bindings/rust.md)
