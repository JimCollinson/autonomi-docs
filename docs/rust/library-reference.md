# Rust Library Reference

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

`ant-core` is the native Rust library for building directly on Autonomi without the daemon.

## Install

Use `ant-core` as a local dependency from an `ant-client` checkout:

```toml
[dependencies]
ant-core = { path = "../ant-client/ant-core" }
bytes = "1"
tokio = { version = "1", features = ["full"] }
```

For same-machine devnets or local testnets, set `ClientConfig { allow_loopback: true, ..ClientConfig::default() }` before `Client::connect`. Keep the default `false` on public networks.

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
use ant_core::data::{Client, ClientConfig, EvmNetwork, Wallet};
use bytes::Bytes;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let wallet = Wallet::new_from_private_key(EvmNetwork::ArbitrumOne, "0xprivate_key...")?;
    let client = client.with_wallet(wallet);
    client.approve_token_spend().await?;

    let result = client.data_upload(Bytes::from("hello autonomi")).await?;
    let content = client.data_download(&result.data_map).await?;

    assert_eq!(content, Bytes::from("hello autonomi"));
    Ok(())
}
```

To make uploaded data publicly retrievable by address, store and later fetch the DataMap:

```rust
use ant_core::data::{Client, ClientConfig, EvmNetwork, Wallet};
use bytes::Bytes;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let wallet = Wallet::new_from_private_key(EvmNetwork::ArbitrumOne, "0xprivate_key...")?;
    let client = client.with_wallet(wallet);
    client.approve_token_spend().await?;

    let result = client.data_upload(Bytes::from("hello autonomi")).await?;

    let public_address = client.data_map_store(&result.data_map).await?;
    let public_data_map = client.data_map_fetch(&public_address).await?;
    let downloaded = client.data_download(&public_data_map).await?;

    assert_eq!(downloaded, Bytes::from("hello autonomi"));
    Ok(())
}
```

## File operations

```rust
use ant_core::data::{Client, ClientConfig, EvmNetwork, PaymentMode, Wallet};
use std::path::Path;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let wallet = Wallet::new_from_private_key(EvmNetwork::ArbitrumOne, "0xprivate_key...")?;
    let client = client.with_wallet(wallet);
    client.approve_token_spend().await?;

    let result = client.file_upload_with_mode(Path::new("photo.jpg"), PaymentMode::Merkle).await?;
    let address = client.data_map_store(&result.data_map).await?;
    let data_map = client.data_map_fetch(&address).await?;
    client.file_download(&data_map, Path::new("photo_copy.jpg")).await?;
    Ok(())
}
```

## External signer flows

The native Rust library exposes both wave-batch and Merkle-batch external payment helpers.

For wave-batch uploads, `data_prepare_upload`, `file_prepare_upload`, and `finalize_upload` prepare the upload, collect quotes, and later store the chunks after an external signer returns transaction hashes.

For Merkle batches, `prepare_merkle_batch_external` and `finalize_merkle_batch` expose the low-level batch helpers, while `finalize_upload_merkle` completes a prepared upload from the winning pool hash. Progress-aware variants such as `file_prepare_upload_with_progress`, `finalize_upload_with_progress`, and `finalize_upload_merkle_with_progress` are also available when you need UI feedback during long-running uploads.

## Key types

| Type | Description |
|------|-------------|
| `ant_core::data::Client` | Main network client |
| `ant_core::data::ClientConfig` | Separate quote and store timeouts, concurrency limits, and loopback policy |
| `ant_core::data::PaymentMode` | `Auto`, `Merkle`, or `Single` |
| `ant_core::data::DataMap` | Private retrieval map for uploaded data |
| `ant_core::data::LocalDevnet` | Local development helper |
| `ant_core::data::Wallet` | EVM wallet used for paid operations |
| `ant_core::data::PreparedUpload` | Two-phase upload state used by external-signer flows |
| `ant_core::data::ExternalPaymentInfo` | External payment details for prepared uploads |
| `ant_core::data::PreparedMerkleBatch` | Prepared Merkle batch data for external signing |

## External signer example

```rust
use ant_core::data::{Client, ClientConfig, ExternalPaymentInfo};
use bytes::Bytes;
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::connect(&["1.2.3.4:12000".parse()?], ClientConfig::default()).await?;
    let prepared = client.data_prepare_upload(Bytes::from("hello autonomi")).await?;

    match &prepared.payment_info {
        ExternalPaymentInfo::WaveBatch { payment_intent, .. } => {
            println!("Need to pay {} atto", payment_intent.total_amount);
        }
        ExternalPaymentInfo::Merkle { prepared_batch, .. } => {
            println!("Merkle depth: {}", prepared_batch.depth);
        }
    }

    let tx_hashes: HashMap<_, _> = HashMap::new();
    let _ = tx_hashes;
    Ok(())
}
```

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

The library also exports `LocalDevnet` for local development flows:

Enable the `ant-core` `devnet` feature before you use this section:

```toml
[dependencies]
ant-core = { path = "../ant-client/ant-core", features = ["devnet"] }
```

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

- [Developing in Rust](README.md)
- [Build Directly in Rust](build-directly-in-rust.md)
- [Rust SDK](../sdk/reference/language-bindings/rust.md)
