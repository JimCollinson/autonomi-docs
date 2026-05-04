# Retrieve Data from the Network

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Use `antd` to retrieve existing public data from the Autonomi Network without wallet setup. This is the simplest read-only flow through the daemon before you decide whether your application also needs uploads.

If you would rather use shell commands without running `antd`, see [Use the CLI](../cli/use-the-cli.md). If you want daemon-free Rust access, see [Build Directly in Rust](../rust/build-directly-in-rust.md).

Featured examples on this page use cURL, Python, Node.js / TypeScript, and Rust. Other SDK languages are available in the [Language Bindings](../sdk/reference/language-bindings/overview.md) section.

## Prerequisites

- `antd` installed, running, and healthy on `http://localhost:8082` (see [Start the Local Daemon](start-the-local-daemon.md))
- An existing public address to retrieve. If you do not have one yet, follow [Store Data on the Network](store-data-on-the-network.md) first.
- Optional: the runtime or toolchain for the SDK examples you want to run, such as Python, Node.js, or Rust

For private retrieval, you also need the `DataMap`. Use [Build Read-Only Features](../guides/build-read-only-features.md) if you want the broader read-only flow, including private data.

## Steps

{% stepper %}
{% step %}
### Check the daemon is healthy

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
{% endstep %}
{% step %}
### Retrieve public data from an existing address

Use a public address from another application, another developer, or a previous write. If you do not already have one, follow [Store Data on the Network](store-data-on-the-network.md) first, then come back to this page.

{% tabs %}
{% tab title="cURL" %}
```bash
ADDRESS="<public_address>"

curl "http://localhost:8082/v1/data/public/$ADDRESS"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
data = client.data_get_public("<public_address>")

print(data.decode())
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const data = await client.dataGetPublic("<public_address>");
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
    let data = client.data_get_public("<public_address>").await?;

    println!("{}", String::from_utf8_lossy(&data));
    Ok(())
}
```
{% endtab %}
{% endtabs %}
{% endstep %}
{% step %}
### Confirm the response shape

The REST API returns base64 inside JSON:

```json
{
  "data": "SGVsbG8sIEF1dG9ub21pIQ=="
}
```

The SDK bindings decode the bytes for you, so the Python, Node.js / TypeScript, and Rust examples print the retrieved content directly.

If you need to retrieve private content next, continue to [Build Read-Only Features](../guides/build-read-only-features.md) for the `DataMap` workflow.
{% endstep %}
{% endstepper %}

## What happened

`antd` accepted your read request, fetched the existing content from the network, and returned it without any wallet setup. Public retrieval only needs a known public address because the storage payment was already handled when the data was written.

## Next steps

- [Build Read-Only Features](../guides/build-read-only-features.md)
- [Store and Retrieve Data with the SDKs](how-to-guides/store-and-retrieve-data.md)
- [Store Data on the Network](store-data-on-the-network.md)
- [REST API](../sdk/reference/rest-api.md)
