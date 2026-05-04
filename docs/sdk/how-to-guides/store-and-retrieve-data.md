# Store and Retrieve Data with the SDKs

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

In this guide, you use `antd`, the local daemon used by the SDKs, to store public data, private data, files, and directories through language SDKs.

If you want direct shell access instead, see [Use the CLI](../../cli/use-the-cli.md). If you want direct programmatic Rust access without the daemon, see [Build Directly in Rust](../../rust/build-directly-in-rust.md).

Featured examples on this page use cURL, Python, Node.js / TypeScript, and Rust. Other SDK languages are available in the [Language Bindings](../reference/language-bindings/overview.md) section.

## Prerequisites

- `antd` running on `http://localhost:8082` (see [Start the Local Daemon](../start-the-local-daemon.md))
- For the write examples on this page, a write-enabled daemon. On the default network, restart `antd` with wallet configuration first. On a local devnet, `ant dev start` provisions that for you. See [Prepare a Wallet for Uploads](../../guides/prepare-a-wallet-for-uploads.md) for the default-network setup.
- Optional: the runtime or toolchain for the SDK examples you want to run, such as Python, Node.js, or Rust

The read examples work with any running daemon if you already have an address or DataMap. The write examples on this page require the write-enabled setup above.

## Steps

### 1. Store public data

{% tabs %}
{% tab title="cURL" %}
```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.data_put_public(b"Hello, Autonomi!")

print(result.address)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.dataPutPublic(Buffer.from("Hello, Autonomi!"));
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let result = client.data_put_public(b"Hello, Autonomi!", None).await?;

    println!("{}", result.address);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

### 2. Retrieve public data

{% tabs %}
{% tab title="cURL" %}
```bash
curl http://localhost:8082/v1/data/public/<address>
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
data = client.data_get_public("<address>")

print(data.decode())
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const data = await client.dataGetPublic("<address>");
  console.log(data.toString());
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let data = client.data_get_public("<address>").await?;

    println!("{}", String::from_utf8_lossy(&data));
    Ok(())
}
```
{% endtab %}
{% endtabs %}

The REST response uses base64 in the `data` field. The Python, Node.js / TypeScript, and Rust SDKs decode it back into bytes.

### 3. Store private data

Private uploads return a serialized DataMap instead of a public address.

{% tabs %}
{% tab title="cURL" %}
```bash
DATA_B64=$(printf 'Secret message' | base64)

curl -X POST http://localhost:8082/v1/data/private \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```
Expected response shape:

```json
{
  "data_map": "<hex_encoded_datamap>",
  "chunks_stored": <chunk_count>,
  "payment_mode_used": "auto"
}
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.data_put_private(b"Secret message")

data_map = result.address
print(data_map)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.dataPutPrivate(Buffer.from("Secret message"));
  const dataMap = result.address;
  console.log(dataMap);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let result = client.data_put_private(b"Secret message", None).await?;

    let data_map = result.address;
    println!("{}", data_map);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

In the Python, Node.js / TypeScript, and Rust SDKs, the returned private `data_map` is surfaced through `PutResult.address`.

### 4. Retrieve private data

{% tabs %}
{% tab title="cURL" %}
```bash
curl "http://localhost:8082/v1/data/private?data_map=<hex_encoded_datamap>"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
data = client.data_get_private("<hex_encoded_datamap>")

print(data.decode())
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const data = await client.dataGetPrivate("<hex_encoded_datamap>");
  console.log(data.toString());
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let data = client.data_get_private("<hex_encoded_datamap>").await?;

    println!("{}", String::from_utf8_lossy(&data));
    Ok(())
}
```
{% endtab %}
{% endtabs %}

### 5. Upload and download a file

These endpoints work on paths visible to the machine running `antd`.

{% tabs %}
{% tab title="cURL" %}
```bash
curl -X POST http://localhost:8082/v1/files/upload/public \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/document.pdf"}'

curl -X POST http://localhost:8082/v1/files/download/public \
  -H "Content-Type: application/json" \
  -d '{"address":"<64_hex_address>","dest_path":"/absolute/path/to/downloaded-document.pdf"}'
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.file_upload_public("/absolute/path/to/document.pdf")
client.file_download_public(result.address, "/absolute/path/to/downloaded-document.pdf")

print(result.address)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.fileUploadPublic("/absolute/path/to/document.pdf");
  await client.fileDownloadPublic(result.address, "/absolute/path/to/downloaded-document.pdf");
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let result = client
        .file_upload_public("/absolute/path/to/document.pdf", None)
        .await?;
    client
        .file_download_public(&result.address, "/absolute/path/to/downloaded-document.pdf")
        .await?;

    println!("{}", result.address);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

### 6. Upload and download a directory

{% tabs %}
{% tab title="cURL" %}
```bash
curl -X POST http://localhost:8082/v1/dirs/upload/public \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/my-folder"}'

curl -X POST http://localhost:8082/v1/dirs/download/public \
  -H "Content-Type: application/json" \
  -d '{"address":"<64_hex_address>","dest_path":"/absolute/path/to/output-folder"}'
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.dir_upload_public("/absolute/path/to/my-folder")
client.dir_download_public(result.address, "/absolute/path/to/output-folder")

print(result.address)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.dirUploadPublic("/absolute/path/to/my-folder");
  await client.dirDownloadPublic(result.address, "/absolute/path/to/output-folder");
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let result = client
        .dir_upload_public("/absolute/path/to/my-folder", None)
        .await?;
    client
        .dir_download_public(&result.address, "/absolute/path/to/output-folder")
        .await?;

    println!("{}", result.address);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

## Verify it worked

For raw data, compare the retrieved bytes to the original payload. For files and directories, compare the downloaded output on disk with the original local source before you uploaded it.

## Common errors

**400 Bad Request**: Check base64 encoding, address length, and local path values.

**402 Payment Required**: Fund the configured wallet or switch to a local devnet with test funds.

**503 Service Unavailable**: The daemon does not have wallet configuration. Restart it with `AUTONOMI_WALLET_KEY` or let `ant dev start` provision a local environment.

## Next steps

- [Store Data on the Network](../store-data-on-the-network.md)
- [Prepare a Wallet for Uploads](../../guides/prepare-a-wallet-for-uploads.md)
- [REST API](../reference/rest-api.md)
- [SDK Overview](../reference/overview.md)
- [Start the Local Daemon](../start-the-local-daemon.md)
