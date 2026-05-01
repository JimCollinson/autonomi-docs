# Store Data on the Network

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

Use `antd` to store a small public payload on the Autonomi Network and read it back again so you can see how the daemon-backed SDK workflow handles writes.

## Prerequisites

- `antd` installed and running on `http://localhost:8082` (see [Start the Local Daemon](start-the-local-daemon.md))
- A write-enabled daemon. On the default network, restart `antd` with wallet configuration before you continue. On a local devnet, `ant dev start` provisions the upload settings for you. See [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md) for the default-network setup.
- Optional: the runtime or toolchain for the SDK examples you want to run, such as Python, Node.js, or Rust

If you would rather use shell commands or direct Rust instead, see [Use the CLI](../cli/use-the-cli.md) and [Build Directly in Rust](../rust/build-directly-in-rust.md). If your application should keep the signing key outside `antd`, start with [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md) instead of this guide.

If you only need retrieval and do not need uploads yet, start with [Retrieve Data from the Network](retrieve-data-from-the-network.md).

Featured examples on this page use cURL, Python, Node.js / TypeScript, and Rust. Other SDK languages are available in the [Language Bindings](../sdk/reference/language-bindings/overview.md) section.

## Steps

### 1. Check the daemon is healthy

{% tabs %}
{% tab title="cURL" %}
```bash
curl http://localhost:8082/health
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
status = client.health()

print(status.network)
print(status.ok)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const status = await client.health();
  console.log(status.network);
  console.log(status.ok);
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
    let status = client.health().await?;

    println!("{}", status.network);
    println!("{}", status.ok);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

Expected REST response:

```json
{
  "status": "ok",
  "network": "default"
}
```

### 2. Store a public payload

Public uploads are still paid writes. If `antd` is running on the default network, make sure you restarted it with wallet configuration before you continue. If `antd` is running on a local devnet, `ant dev start` already provisioned the payment settings.

The REST API expects binary data as base64 inside JSON.

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

Expected REST response shape:

```json
{
  "address": "<64_hex_address>",
  "chunks_stored": <chunk_count>,
  "payment_mode_used": "auto"
}
```

Save the returned address.

### 3. Retrieve the payload

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

Expected REST response shape:

```json
{
  "data": "SGVsbG8sIEF1dG9ub21pIQ=="
}
```

The REST `data` field is base64-encoded. The Python, Node.js / TypeScript, and Rust SDKs decode it for you.

### 4. Verify the round-trip

{% tabs %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
original = b"Hello, Autonomi!"
result = client.data_put_public(original)
retrieved = client.data_get_public(result.address)

assert retrieved == original
print(result.address)
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import assert from "node:assert/strict";
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const original = Buffer.from("Hello, Autonomi!");
  const result = await client.dataPutPublic(original);
  const retrieved = await client.dataGetPublic(result.address);

  assert.deepEqual(retrieved, original);
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
    let original = b"Hello, Autonomi!";
    let result = client.data_put_public(original, None).await?;
    let retrieved = client.data_get_public(&result.address).await?;

    assert_eq!(retrieved, original);
    println!("{}", result.address);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

## What happened

`antd` accepted your payload, self-encrypted it into chunks, stored those chunks on the network, and returned the public address used to fetch it again. That address is content-addressed: if you uploaded different bytes, you would get a different address. The REST API represents binary payloads as base64 inside JSON, while the Python, Node.js / TypeScript, and Rust SDKs decode those values back into bytes for you.

## Next steps

- [Retrieve Data from the Network](retrieve-data-from-the-network.md)
- [Store and Retrieve Data with the SDKs](how-to-guides/store-and-retrieve-data.md)
- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md)
- [REST API](../sdk/reference/rest-api.md)
- [SDK Overview](../sdk/reference/overview.md)
