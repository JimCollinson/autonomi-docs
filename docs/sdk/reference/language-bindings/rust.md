# Rust SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

The daemon-binding Rust crate in `ant-sdk` is `antd-client`. It is separate from the native Rust `ant-core` route documented elsewhere in this docs set.

## Install

```bash
cargo add antd-client
```

## Connect to the daemon

```rust
use antd_client::{Client, DEFAULT_BASE_URL, discover_daemon_url};
use std::time::Duration;

// Default REST client
let client = Client::new(DEFAULT_BASE_URL);

// Use discovered URL if available
let discovered = discover_daemon_url().unwrap_or_else(|| DEFAULT_BASE_URL.to_string());
let discovered_client = Client::new(&discovered);

// Custom timeout
let slow_client = Client::with_timeout(DEFAULT_BASE_URL, Duration::from_secs(30));
```

For gRPC, the current crate also exports `GrpcClient` and `DEFAULT_GRPC_ENDPOINT`.

## Store and retrieve data

For upload examples in this section, start `antd` in a write-enabled mode first. On the default network, that means wallet plus EVM payment configuration. On a local devnet, `ant dev start` provisions that for you.

```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);

    let health = client.health().await?;
    assert!(health.ok);

    let result = client.data_put_public(b"Hello from Rust!", None).await?;
    println!("{}", result.address);

    let data = client.data_get_public(&result.address).await?;
    println!("{}", String::from_utf8_lossy(&data));
    Ok(())
}
```

## Type mappings

| Autonomi type | Rust type |
|------|------|
| `HealthStatus` | `antd_client::HealthStatus` |
| `PutResult` | `antd_client::PutResult` |
| `WalletAddress` | `antd_client::WalletAddress` |
| `WalletBalance` | `antd_client::WalletBalance` |
| `PrepareUploadResult` | `antd_client::PrepareUploadResult` |
| `FinalizeUploadResult` | `antd_client::FinalizeUploadResult` |
| Raw data | `Vec<u8>` or `&[u8]` |

## Error handling

```rust
use antd_client::{AntdError, Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() {
    let client = Client::new(DEFAULT_BASE_URL);

    match client.data_get_public("some_address").await {
        Ok(data) => println!("{}", data.len()),
        Err(AntdError::NotFound(message)) => println!("{message}"),
        Err(AntdError::Payment(message)) => println!("{message}"),
        Err(error) => println!("{error}"),
    }
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md). For the native Rust interface, see [Developing in Rust](../../../rust/README.md).
